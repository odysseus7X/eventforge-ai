from typing import Dict, Any
import pandas as pd
import os

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.models.schemas import ConferenceInput, VenueAgentOutput, Venue
from eventforge.utils.logging import get_logger
from eventforge.tools.web_search import search_venues_structured

logger = get_logger(__name__)


class VenueAgent(BaseAgent):

    def __init__(self):
        super().__init__("venue_agent")

        # ---- AUTO-DETECT DELIMITER ----
        self.venues_df = pd.read_csv("data/venues.csv", sep="\t")

        # ---- CLEAN COLUMN NAMES ----
        self.venues_df.columns = (
            self.venues_df.columns
            .str.strip()
            .str.lower()
        )

        logger.info(f"Loaded venues from: data/venues.csv")
        logger.info(f"Columns: {self.venues_df.columns.tolist()}")

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("VenueAgent started")

            # ---- INPUT ----
            input_data = ConferenceInput(**state["input"])

            df = self.venues_df.copy()

            # ---- CLEAN DATA ----
            for col in ["city", "country"]:
                if col not in df.columns:
                    raise ValueError(f"Missing column: {col}")
                df[col] = df[col].astype(str).str.strip().str.lower()

            geo = input_data.geography.strip().lower()
            audience = max(input_data.audience_size, 1)
            budget = input_data.budget_constraint

            # ---- GEO FILTER (CITY OR COUNTRY) ----
            df_filtered = df[
                (df["city"] == geo) |
                (df["country"] == geo)
            ]

            fallback_needed = False

            # ---- GEO FILTER ----
            df_geo = df[
                (df["city"] == geo) |
                (df["country"] == geo)
            ]

            if df_geo.empty:
                logger.warning("No geo match")
                fallback_needed = True
            else:
                df_filtered = df_geo

                # ---- BUDGET FILTER ----
                df_filtered = df_filtered[
                    df_filtered["price_per_day"] <= budget
                ]

                if df_filtered.empty:
                    logger.warning("No venues within budget")
                    fallback_needed = True


            # ---- SCORING ----
            if not df_filtered.empty:

                def score(row):
                    capacity_score = min(row["capacity"] / audience, 1.5)
                    price_score = 1 / (row["price_per_day"] + 1)
                    budget_fit = 1 - (row["price_per_day"] / (budget + 1))

                    return (
                        0.5 * capacity_score +
                        0.3 * budget_fit +
                        0.2 * price_score
                    )

                df_filtered["score"] = df_filtered.apply(score, axis=1)
                df_filtered = df_filtered.sort_values(by="score", ascending=False).head(5)

            venues = []

            # ---- NORMAL OUTPUT ----
            if not df_filtered.empty:
                venues = [
                    Venue(
                        id=str(row["id"]),
                        name=str(row["name"]),
                        geography=f"{row['city']}, {row['country']}",
                        capacity=int(row["capacity"]),
                        price_per_day=float(row["price_per_day"]),
                        score=float(row["score"]),
                    )
                    for _, row in df_filtered.iterrows()
                ]

            # ---- FALLBACK (TAVILY) ----
            if not venues:
                logger.warning("No venues found → using Tavily search")

                query = f"{input_data.category} conference venues in {input_data.geography}"
                search_results = await search_venues_structured(query)

                state["shared_memory"]["venue_search"] = search_results

                venues = [
                    Venue(
                        id=f"web_{i}",
                        name=r.get("name", "Unknown Venue"),
                        geography=input_data.geography,
                        capacity=0,
                        price_per_day=0,
                        score=0.5
                    )
                    for i, r in enumerate(search_results)
                ]

            logger.info("VenueAgent completed successfully")

            return self._success(VenueAgentOutput(venues=venues))

        except Exception as e:
            import traceback
            traceback.print_exc()
            logger.exception("VenueAgent failed")
            return self._fail(e)

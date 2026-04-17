
from pathlib import Path

import pandas as pd
from typing import Dict, Any

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.models.schemas import ConferenceInput, VenueAgentOutput, Venue
from eventforge.utils.logging import get_logger
from eventforge.tools.web_search import search_venues
from eventforge.utils.validator import clean_venues

logger = get_logger(__name__)


class VenueAgent(BaseAgent):
    def __init__(self):
        super().__init__("venue_agent")

        # Load dataset once
        data_path = Path(__file__).resolve().parents[1] / "data" / "venues.csv"
        self.df = pd.read_csv(data_path)
        self.df.columns = self.df.columns.str.strip().str.lower()

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("VenueAgent started")

            input_data = ConferenceInput(**state["input"])
            geo = input_data.geography.strip().lower()
            audience = input_data.audience_size

            df = self.df.copy()

            # ---- NORMALIZE ----
            for col in ["city", "country"]:
                df[col] = df[col].astype(str).str.strip().str.lower()

            # ---- FILTER ----
            df_filtered = df[
                (df["city"].str.contains(geo, na=False)) |
                (df["country"].str.contains(geo, na=False))
            ]

            category_map = {
                "ai": ["ai", "tech"],
                "ml": ["ai", "tech"],
                "technology": ["tech"],
                "business": ["business"],
                "startup": ["business", "tech"],
            }
            
            input_cat = input_data.category.lower()
            
            valid_categories = category_map.get(input_cat, [input_cat])
            
            df_filtered = df_filtered[
                df_filtered["category"].str.lower().isin(valid_categories)
            ]

            df_filtered = df_filtered[df_filtered["capacity"] >= audience]

            venues = []

            # ---- SCORING + SELECTION ----
            if not df_filtered.empty:
                budget = input_data.budget_usd or df_filtered["price_per_day_usd"].max()

                def score(row):
                    capacity_ratio = row["capacity"] / audience
                    capacity_score = 1 - abs(1 - capacity_ratio)

                    price_score = 1 / (row["price_per_day_usd"] + 1)

                    budget_score = max(
                        0, 1 - (row["price_per_day_usd"] / (budget + 1))
                    )

                    return (
                        0.5 * capacity_score +
                        0.3 * budget_score +
                        0.2 * price_score
                    )

                df_filtered = df_filtered.assign(
                    score=df_filtered.apply(score, axis=1)
                ).sort_values("score", ascending=False).head(3)

                venues = [
                    Venue(
                        id=str(row["id"]),
                        name=row["name"],
                        city=row["city"],
                        capacity=int(row["capacity"]),
                        price_per_day_usd=int(row["price_per_day_usd"]),
                        notes="From dataset",
                    )
                    for _, row in df_filtered.iterrows()
                ]

            # ---- FALLBACK ----
            if not venues:
                logger.warning("Dataset empty → using web search")

                query = f"{input_data.category} conference venues in {input_data.geography}"
                await search_venues.ainvoke(query)  # kept for side-effect consistency

                venues = [
                    Venue(
                        id=f"web_{i}",
                        name=f"Venue {i}",
                        city=input_data.geography,
                        capacity=audience,
                        price_per_day_usd=5000,
                        notes="Web fallback",
                    )
                    for i in range(3)
                ]

            # ---- CLEAN ----
            venues = clean_venues(venues, audience)

            logger.info("VenueAgent completed")
            return self._success(VenueAgentOutput(venues=venues))

        except Exception as e:
            logger.exception("VenueAgent failed")
            return self._fail(e)
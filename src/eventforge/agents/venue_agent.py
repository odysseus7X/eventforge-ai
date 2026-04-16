from typing import Dict, Any
import pandas as pd

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.models.schemas import ConferenceInput, VenueAgentOutput, Venue
from eventforge.utils.logging import get_logger

logger = get_logger(__name__)


class VenueAgent(BaseAgent):

    def __init__(self):
        super().__init__("venue_agent")

        # load dataset once
        self.venues_df = pd.read_csv("data/venues.csv", sep="\t")

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("VenueAgent started")

            input_data = ConferenceInput(**state["input"])

            df = self.venues_df.copy()

            # ---- FILTER BY GEOGRAPHY ----
            df = df[df["country"].str.lower() == input_data.geography.lower()]

            # fallback if empty
            if df.empty:
                df = self.venues_df.copy()

            # ---- SCORE VENUES ----
            def score(row):
                capacity_score = min(row["capacity"] / input_data.audience_size, 1.5)
                price_score = 1 / (row["price_per_day"] + 1)
                return 0.7 * capacity_score + 0.3 * price_score

            df["score"] = df.apply(score, axis=1)

            # ---- SORT ----
            df = df.sort_values(by="score", ascending=False).head(5)

            # ---- FORMAT OUTPUT ----
            venues = [
                Venue(
                    id=row["id"],
                    name=row["name"],
                    city=row["city"],
                    country=row["country"],
                    capacity=int(row["capacity"]),
                    price_per_day=float(row["price_per_day"]),
                    score=float(row["score"]),
                )
                for _, row in df.iterrows()
            ]

            result = VenueAgentOutput(venues=venues)

            logger.info("VenueAgent completed successfully")

            return self._success(result)

        except Exception as e:
            import traceback
            traceback.print_exc() 
            logger.exception("VenueAgent failed")
            return self._fail(e)
        
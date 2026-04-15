from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.utils.logging import get_logger
from eventforge.models.schemas import (
    ConferenceInput,
    PricingAgentOutput
)
from eventforge.utils.llm_client import get_llm

logger = get_logger(__name__)


class PricingAgent(BaseAgent):

    def __init__(self):
        super().__init__("pricing_agent")

        self.llm = get_llm().with_structured_output(
            PricingAgentOutput,
            method="json_schema",
            strict=True
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an expert in conference pricing and revenue optimization."),

            ("user",
             """
            Conference Details:
            Category: {category}
            Geography: {geography}
            Audience Size: {audience_size}

            Venue Info:
            {venue_summary}

            TASK:
            - Create 3 pricing tiers (basic, standard, premium)
            - Assign UNIQUE id to each tier
            - Set realistic ticket prices
            - Estimate expected conversions per tier
            - Estimate total attendance
            - Estimate total revenue
            """)
        ])

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("PricingAgent started")

            input_data = ConferenceInput(**state["input"])

            # 🔥 dependency: must read venue output
            venue_data = state["outputs"]["venue_agent"]

            venue_summary = str(venue_data)

            chain = self.prompt | self.llm

            result = await chain.ainvoke({
                "category": input_data.category,
                "geography": input_data.geography,
                "audience_size": input_data.audience_size,
                "venue_summary": venue_summary
            })

            logger.info("PricingAgent completed")

            return self._success(result)

        except Exception as e:
            logger.exception("PricingAgent failed")
            return self._fail(e)
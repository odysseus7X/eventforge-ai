from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.utils.logging import get_logger
from eventforge.models.schemas import ConferenceInput, VenueAgentOutput
from eventforge.utils.llm_client import get_llm
from eventforge.tools.web_search import search_venues

logger = get_logger(__name__)


class VenueAgent(BaseAgent):

    def __init__(self):
        super().__init__("venue_agent")

        self.llm = get_llm().with_structured_output(
            VenueAgentOutput, method="json_schema", strict=True
        )

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an expert event planner. Select suitable venues."),
                (
                    "user",
                    """
            Conference Details:
            Category: {category}
            Geography: {geography}
            Audience Size: {audience_size}

            Search Results:
            {search_results}

            TASK:
            - Select top 3 venues
            - Assign UNIQUE id
            - Ensure capacity >= audience size
            - Provide price per day estimate
            - Add notes
            """,
                ),
            ]
        )

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("VenueAgent started")

            input_data = ConferenceInput(**state["input"])

            query = f"{input_data.category} conference venues in {input_data.geography}"
            search_results = await search_venues.ainvoke(query)

            chain = self.prompt | self.llm

            result = await chain.ainvoke(
                {
                    "category": input_data.category,
                    "geography": input_data.geography,
                    "audience_size": input_data.audience_size,
                    "search_results": search_results,
                }
            )

            return self._success(result)

        except Exception as e:
            logger.exception("VenueAgent failed")
            return self._fail(e)

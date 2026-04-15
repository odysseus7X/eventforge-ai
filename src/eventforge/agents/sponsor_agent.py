from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.utils.logging import get_logger
from eventforge.models.schemas import ConferenceInput, SponsorAgentOutput
from eventforge.utils.llm_client import get_llm
from eventforge.tools.web_search import search_sponsors

logger = get_logger(__name__)


class SponsorAgent(BaseAgent):

    def __init__(self):
        super().__init__("sponsor_agent")

        # ✅ CORRECT: structured output at model level
        self.llm = get_llm().with_structured_output(
            SponsorAgentOutput,
            method="json_schema",
            strict=True
        )

        # ✅ CLEAN PROMPT (NO JSON SCHEMA HERE)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system",
             "You are an expert conference strategist. "
             "Generate high-quality sponsor recommendations."),

            ("user",
             """
            Conference Details:
            Category: {category}
            Geography: {geography}
            Audience Size: {audience_size}

            Search Results:
            {search_results}

            TASK:
            - Select top 5 sponsors
            - Assign a UNIQUE id (string, short, no spaces)
            - Provide industry
            - Assign relevance_score (0-1)
            - Give reason
            - Generate outreach email
            """)
        ])

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("SponsorAgent started")

            # ---- INPUT ----
            input_data = ConferenceInput(**state["input"])
            logger.debug(f"Input: {input_data.model_dump()}")

            # ---- TOOL ----
            query = f"{input_data.category} conference sponsors in {input_data.geography}"
            search_results = await search_sponsors.ainvoke(query)

            state["shared_memory"]["sponsor_search"] = search_results

            # ---- CHAIN ----
            chain = self.prompt | self.llm

            logger.info("Calling LLM...")

            result: SponsorAgentOutput = await chain.ainvoke({
                "category": input_data.category,
                "geography": input_data.geography,
                "audience_size": input_data.audience_size,
                "search_results": search_results
            })

            logger.info("LLM returned and parsed successfully")

            return self._success(result)

        except Exception as e:
            logger.exception("SponsorAgent failed")
            return self._fail(e)
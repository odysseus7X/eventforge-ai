from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.utils.grounding import build_grounded_context
from eventforge.utils.logging import get_logger
from eventforge.models.schemas import ConferenceInput, SpeakerAgentOutput
from eventforge.utils.llm_client import get_llm
from eventforge.tools.web_search import search_speakers

logger = get_logger(__name__)


class SpeakerAgent(BaseAgent):

    def __init__(self):
        super().__init__("speaker_agent")

        # ✅ structured output (same as sponsor)
        self.llm = get_llm().with_structured_output(
            SpeakerAgentOutput, method="json_schema", strict=True
        )

        # ✅ clean prompt (no schema embedded)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert conference curator. "
                    "Select high-quality speakers relevant to the conference theme.",
                ),
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
            - Select top 5 speakers
            - Assign a UNIQUE id (string, short, no spaces)
            - Provide full name
            - Provide title and company
            - Assign influence_score (0-1)
            - Suggest a talk topic relevant to the conference
            - Provide a short bio summary (2-3 lines)

            IMPORTANT:
            - DO NOT include global CEOs (Google, OpenAI, Meta, etc.)
            - Prefer regionally relevant speakers
            - Match audience size and event scale
            """,
                ),
            ]
        )

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("SpeakerAgent started")

            # ---- INPUT ----
            input_data = ConferenceInput(**state["input"])
            logger.debug(f"Input: {input_data.model_dump()}")

            # ---- TOOL ----
            query = (
                f"{input_data.category} conference speakers in {input_data.geography}"
            )
            search_results = await search_speakers.ainvoke(query)

            context = self._ground(
                search_results,
                extra="""
            - Prefer regionally relevant speakers
            - Match conference scale
            """,
            )

            state["shared_memory"]["speaker_search"] = search_results

            # ---- CHAIN ----
            chain = self.prompt | self.llm

            logger.info("Calling LLM...")

            result: SpeakerAgentOutput = await chain.ainvoke(
                {
                    "category": input_data.category,
                    "geography": input_data.geography,
                    "audience_size": input_data.audience_size,
                    "search_results": context,
                }
            )

            logger.info("LLM returned and parsed successfully")

            return self._success(result)

        except Exception as e:
            logger.exception("SpeakerAgent failed")
            return self._fail(e)

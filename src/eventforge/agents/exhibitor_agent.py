from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.models.schemas import ConferenceInput, ExhibitorAgentOutput
from eventforge.utils.llm_client import get_llm
from eventforge.tools.web_search import search_exhibitors
from eventforge.utils.logging import get_logger

logger = get_logger(__name__)


class ExhibitorAgent(BaseAgent):

    def __init__(self):
        super().__init__("exhibitor_agent")

        self.llm = get_llm().with_structured_output(
            ExhibitorAgentOutput,
            method="json_schema",
            strict=True
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an expert in conference exhibitor planning."),

            ("user", 
             """
            Conference Details:
            Category: {category}
            Geography: {geography}

            Search Results:
            {search_results}

            TASK:
            - Select top 5 exhibitors
            - Assign UNIQUE id
            - Categorize each as: startup / enterprise / tools
            - Provide short description
            - Only include real companies
            - Avoid invalid or noisy names

            STRICT RULES:
            - Only include real companies or organizations
            - DO NOT generate random or unknown names
            - If unsure, skip the entry
            - Prefer companies mentioned in search results
            """)
        ])

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("ExhibitorAgent started")

            input_data = ConferenceInput(**state["input"])

            query = f"{input_data.category} conference exhibitors in {input_data.geography}"
            search_results = await search_exhibitors.ainvoke(query)

            chain = self.prompt | self.llm

            result = await chain.ainvoke({
                "category": input_data.category,
                "geography": input_data.geography,
                "search_results": search_results
            })

            return self._success(result)

        except Exception as e:
            logger.exception("ExhibitorAgent failed")
            return self._fail(e)
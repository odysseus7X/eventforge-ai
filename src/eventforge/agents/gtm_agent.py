from typing import Dict, Any

from langchain_core.prompts import ChatPromptTemplate

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.models.schemas import ConferenceInput, GTMAgentOutput
from eventforge.utils.llm_client import get_llm
from eventforge.tools.web_search import search_communities
from eventforge.utils.logging import get_logger

logger = get_logger(__name__)


class GTMAgent(BaseAgent):

    def __init__(self):
        super().__init__("gtm_agent")

        self.llm = get_llm().with_structured_output(
            GTMAgentOutput,
            method="json_schema",
            strict=True
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an expert in event marketing and growth strategy. "
             "You specialize in launching conferences with high attendance using targeted community outreach."),
        
            ("user", 
             """
            Conference Details:
            Category: {category}
            Geography: {geography}
        
            Search Results:
            {search_results}
        
            TASK:
            Identify the best communities to promote this conference.
        
            REQUIREMENTS:
            - Select 4–6 HIGH-QUALITY communities
            - Prefer REAL and ACTIVE communities (LinkedIn groups, Meetup groups, Twitter/X audiences, professional forums)
            - Avoid fake or generic communities
            - Ensure communities are relevant to BOTH:
                - conference category
                - geography (local/regional relevance preferred)
        
            For each community:
            - Assign UNIQUE id (short, no spaces)
            - Provide:
                - community_name
                - platform (LinkedIn / Meetup / Twitter / Discord / etc.)
                - niche (what audience they represent)
                - why this community is relevant (1 line reasoning)
                - priority_order (1 = highest priority)
        
            PROMOTION STRATEGY:
            - Generate a tailored promotion message for EACH community
            - Message should:
                - match the platform tone (LinkedIn = professional, Discord = casual, etc.)
                - be concise (2-3 lines max)
                - include a clear call-to-action
        
            CONSTRAINTS:
            - Avoid unrealistic or global-only communities unless justified
            - Prefer communities with strong engagement potential
            - Ensure diversity across platforms (not all from same platform)
        
            OUTPUT:
            - List of communities (ranked by priority_order)
            - A short GTM summary including:
                - rollout strategy (which communities to target first)
                - reasoning behind prioritization
                - expected impact
            """)
        ])

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        try:
            logger.info("GTMAgent started")

            input_data = ConferenceInput(**state["input"])

            query = f"{input_data.category} communities in {input_data.geography}"
            search_results = await search_communities.ainvoke(query)

            chain = self.prompt | self.llm

            result = await chain.ainvoke(
                {
                    "category": input_data.category,
                    "geography": input_data.geography,
                    "search_results": search_results,
                }
            )

            return self._success(result)

        except Exception as e:
            logger.exception("GTMAgent failed")
            return self._fail(e)

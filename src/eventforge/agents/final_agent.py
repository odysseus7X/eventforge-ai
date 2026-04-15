from typing import Dict, Any

from eventforge.agents.base.base_agent import BaseAgent
from eventforge.models.schemas import ConferencePlan


class FinalAgent(BaseAgent):

    def __init__(self):
        super().__init__("final_agent")

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        return self._success(
            ConferencePlan(
                input=state["input"],
                sponsors=state["outputs"]["sponsor_agent"],
                speakers=state["outputs"]["speaker_agent"],
                venues=state["outputs"]["venue_agent"],
                pricing=state["outputs"]["pricing_agent"],
            )
        )

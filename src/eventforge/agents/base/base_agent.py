from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseAgent(ABC):
    """
    Base class for LangGraph agents.

    IMPORTANT:
    - DO NOT mutate state
    - RETURN partial updates only
    """

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Must:
        - read from state
        - return partial update dict
        """
        pass

    def _success(self, output: Any) -> Dict[str, Any]:
        """
        Return ONLY updates (LangGraph will merge)
        """
        return {
            "outputs": {self.name: output},
            "agent_meta": {self.name: {"status": "completed", "error": None}},
        }

    def _fail(self, error: Exception) -> Dict[str, Any]:
        return {
            "agent_meta": {self.name: {"status": "failed", "error": str(error)}},
            "errors": [f"{self.name}: {str(error)}"],
        }

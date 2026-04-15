from typing import Dict, Any
from eventforge.agents.base.base_agent import BaseAgent


def agent_node(agent: BaseAgent):
    """
    Wraps agent.run into a LangGraph-compatible node.
    """

    def node_fn(state: Dict[str, Any]) -> Dict[str, Any]:
        state["agent_meta"][agent.name] = {"status": "running"}
        return agent.run(state)

    return node_fn
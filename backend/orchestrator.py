from langgraph.graph import StateGraph, END
from backend.state import ConferenceState

def build_graph() -> StateGraph:
    """
    Defines the LangGraph execution graph.
    
    Execution order:
        1. sponsor, speaker, exhibitor, venue, pricing, gtm  ← parallel
        2. ops                                                ← after all above
        3. END

    Returns compiled graph ready to invoke.
    Called by: run_conference_planner() only
    """
    ...

async def run_conference_planner(
    input_data: dict
) -> dict:
    """
    Main entry point for the entire system.
    Called by main.py with raw user input dict.

    Args:
        input_data: {
            "category": str,
            "geography": str,
            "audience_size": int,
            "budget_usd": int | None,
            "duration_days": int
        }

    Steps:
        1. Parse input_data into ConferenceInput
        2. Build initial ConferenceState with conference_input set,
           all agent output fields as None, errors as []
        3. Invoke compiled graph with initial state
        4. Collect all agent outputs from final state
        5. Build and return ConferencePlan as dict

    Returns:
        ConferencePlan.model_dump() — full JSON-serializable result

    Called by: main.py
    """
    ...
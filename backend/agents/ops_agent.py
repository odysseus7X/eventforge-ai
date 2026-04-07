from backend.state import ConferenceState

async def run_ops_agent(state: ConferenceState) -> dict:
    """
    Reads:  state["speakers"], state["venues"], state["conference_input"]
    Writes: {"agenda": OpsAgentOutput}

    Runs AFTER all other agents complete — needs their outputs.

    Steps:
        1. Pull speakers list from state["speakers"].speakers
        2. Pull venue/room info from state["venues"].venues
        3. Pull duration_days from state["conference_input"]
        4. Call call_llm(..., response_model=OpsAgentOutput)
           Give Claude all speakers + rooms + days,
           ask it to build a full schedule as AgendaSlot list
        5. Run check_conflicts(result.agenda) — pure Python, no LLM
        6. Return {"agenda": result}

    Most important agent for judges — builds the visible schedule.
    """
    ...

def check_conflicts(agenda: list) -> list[str]:
    """
    Pure Python. No LLM involved.
    Checks the generated agenda for:
        - Same room booked at same time
        - Same speaker in two places at once

    Args:
        agenda: list of AgendaSlot objects

    Returns:
        list of conflict description strings, empty list if clean

    Called by: run_ops_agent() after LLM generates the schedule
    """
    ...
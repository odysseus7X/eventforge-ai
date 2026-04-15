import operator
from typing import Dict, Any, Optional, Annotated
from typing_extensions import TypedDict
from eventforge.models.schemas import ConferenceInput

class ConferenceState(TypedDict):
    # immutable input
    input: ConferenceInput

    # agent outputs (merged across nodes)
    outputs: Annotated[Dict[str, Any], lambda a, b: {**a, **b}]

    # execution metadata per agent
    agent_meta: Annotated[Dict[str, Any], lambda a, b: {**a, **b}]

    # optional shared scratchpad
    shared_memory: Annotated[Dict[str, Any], lambda a, b: {**a, **b}]

    # logs and errors (append-only)
    logs: Annotated[list[str], operator.add]
    errors: Annotated[list[str], operator.add]
from typing import Optional
from typing_extensions import TypedDict
from backend.models.schemas import (
    ConferenceInput, SponsorAgentOutput, SpeakerAgentOutput,
    ExhibitorAgentOutput, VenueAgentOutput, PricingAgentOutput,
    GTMAgentOutput, OpsAgentOutput
)

class ConferenceState(TypedDict):
    """
    The shared whiteboard flowing through the LangGraph graph.
    Each agent reads what it needs and writes its own output key.

    conference_input:  set once at start, never modified
    All other fields:  None until the corresponding agent runs
    errors:            any agent can append here if something fails
    """
    #input
    conference_input: ConferenceInput

    #agent tracking
    sponsors:   Optional[SponsorAgentOutput]
    speakers:   Optional[SpeakerAgentOutput]
    exhibitors: Optional[ExhibitorAgentOutput]
    venues:     Optional[VenueAgentOutput]
    pricing:    Optional[PricingAgentOutput]
    gtm:        Optional[GTMAgentOutput]
    agenda:     Optional[OpsAgentOutput]

    #errors
    errors:     list[str]
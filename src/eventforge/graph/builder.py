from langgraph.graph import StateGraph, START, END

from eventforge.agents.exhibitor_agent import ExhibitorAgent
from eventforge.agents.gtm_agent import GTMAgent
from eventforge.agents.ops_agent import EventOpsAgent
from eventforge.agents.pricing_agent import PricingAgent
from eventforge.agents.venue_agent import VenueAgent
from eventforge.models.state import ConferenceState
from eventforge.agents.sponsor_agent import SponsorAgent
from eventforge.agents.speaker_agent import SpeakerAgent
from eventforge.agents.final_agent import FinalAgent


async def join_node(state: ConferenceState) -> dict:
    """Barrier node: waits for all upstream nodes."""
    return {}


def build_graph():
    graph = StateGraph(ConferenceState)

    sponsor = SponsorAgent()
    speaker = SpeakerAgent()
    venue = VenueAgent()
    pricing = PricingAgent()
    exhibitor = ExhibitorAgent()
    gtm = GTMAgent()
    ops = EventOpsAgent()
    final = FinalAgent()

    # ---- Nodes ----
    graph.add_node("sponsor_agent", sponsor.run)
    graph.add_node("speaker_agent", speaker.run)
    graph.add_node("venue_agent", venue.run)
    graph.add_node("pricing_agent", pricing.run)
    graph.add_node("ops_agent", ops.run)
    graph.add_node("exhibitor_agent", exhibitor.run)
    graph.add_node("gtm_agent", gtm.run)

    graph.add_node("final_agent", final.run)

    # ---- parallel start ----
    graph.add_edge(START, "sponsor_agent")
    graph.add_edge(START, "speaker_agent")
    graph.add_edge(START, "venue_agent")
    graph.add_edge(START, "exhibitor_agent")
    graph.add_edge(START, "gtm_agent")

    # ---- dependency ----
    graph.add_edge("venue_agent", "pricing_agent")
    graph.add_edge(["speaker_agent", "venue_agent"], "ops_agent")

    # ---- final join ----
    graph.add_edge(
        ["sponsor_agent", "pricing_agent", "ops_agent", "exhibitor_agent", "gtm_agent"],
        "final_agent",
    )
    # ---- End ----
    graph.add_edge("final_agent", END)

    return graph.compile()

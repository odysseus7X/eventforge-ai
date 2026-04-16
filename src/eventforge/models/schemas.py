from pydantic import BaseModel
from typing import Optional, List, Dict


# ── INPUT ──────────────────────────────────────
class ConferenceInput(BaseModel):
    category: str
    geography: str
    audience_size: int
    budget_constraint: float
    duration_days: int

# ── COMMON MIXINS ──────────────────────────────
class ScoredItem(BaseModel):
    confidence: float = 0.8   # model confidence


# ── AGENT OUTPUTS ───────────────────────────────

class Sponsor(ScoredItem):
    id: str
    name: str
    industry: str
    relevance_score: float
    reason: str
    outreach_email: str


class SponsorAgentOutput(BaseModel):
    sponsors: List[Sponsor]


class Speaker(BaseModel):
    id: str
    name: str
    title: str
    company: str
    influence_score: float
    suggested_topic: str
    bio_summary: str

class SpeakerAgentOutput(BaseModel):
    speakers: list[Speaker]


# class Exhibitor(ScoredItem):
#     id: str
#     name: str
#     category: str
#     description: str


# class ExhibitorAgentOutput(BaseModel):
#     exhibitors: List[Exhibitor]


class Venue(BaseModel):
    id: str
    name: str
    geography: str
    capacity: int
    price_per_day: float
    score: float

class VenueAgentOutput(BaseModel):
    venues: List[Venue]


class PricingTier(BaseModel):
    id: str
    name: str
    price_usd: int
    expected_conversions: int


class PricingAgentOutput(BaseModel):
    tiers: List[PricingTier]
    predicted_attendance: int
    predicted_revenue_usd: int


# class CommunityPromotion(ScoredItem):
#     id: str
#     community_name: str
#     platform: str
#     niche: str
#     message_draft: str
#     recommended_post_date: str


# class GTMAgentOutput(BaseModel):
#     promotions: List[CommunityPromotion]
#     gtm_summary: str


# class AgendaSlot(BaseModel):
#     slot_id: str
#     day: int
#     start_time: str
#     end_time: str
#     session_title: str
#     speaker_id: str  
#     room: str


# class OpsAgentOutput(BaseModel):
#     agenda: List[AgendaSlot]
#     conflicts_detected: List[str]
#     rooms_used: List[str]


# ── FINAL OUTPUT (FLEXIBLE) ─────────────────────

class ConferencePlan(BaseModel):
    input: ConferenceInput
    sponsors: SponsorAgentOutput
    speakers: SpeakerAgentOutput
    venues: VenueAgentOutput
    pricing: PricingAgentOutput
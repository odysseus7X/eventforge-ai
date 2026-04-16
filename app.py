"""
EventForge AI — Streamlit UI
==============================
Run from project root:
    streamlit run app.py

Logging goes to the terminal (stdout) as configured by setup_logging().
The UI never suppresses or redirects logs.
"""

from __future__ import annotations

import asyncio
from typing import Any

import streamlit as st

# ── Logging bootstrap (must happen before any eventforge import) ──────────────
from eventforge.utils.logging import get_logger, setup_logging

setup_logging()  # configures root logger → StreamHandler → terminal
logger = get_logger(__name__)

# ── EventForge imports ────────────────────────────────────────────────────────
from eventforge.graph.builder import build_graph

# ─────────────────────────────────────────────────────────────────────────────
# Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EventForge AI",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# Stylesheet (FIXED CLEAN VERSION)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

/* Base */
html, body {
    background: #f5f2eb;
    color: #1a1a1a;
    font-family: 'IBM Plex Sans', sans-serif;
}
.stApp { background: #f5f2eb; }


/* Hide chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Typography */
.ef-wordmark {
    font-family: 'Playfair Display';
    font-size: 3rem;
    font-weight: 900;
    color: #1a1a1a;
}
.ef-sub {
    font-family: 'IBM Plex Mono';
    font-size: 0.68rem;
    color: #7a6a55;
}

/* Inputs */
.stTextInput input,
.stNumberInput input,
input {
    background: #ffffff !important;
    color: #1a1a1a !important;
    border: 1px solid #c8bfaa !important;
}

/* Buttons */
.stButton > button {
    background: #1a1a1a !important;
    color: #ffffff !important;
}

/* Pipeline rows (THIS WAS BROKEN) */
.pipeline-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0;
    border-bottom: 1px solid #e0d8c8;
    font-size: 0.8rem;
    color: #1a1a1a !important;
}
.pip-name { color: #1a1a1a !important; }
.pip-state { color: #5a5040 !important; }

/* Cards */
.item-card {
    border: 1px solid #ece4d4;
    background: #faf8f4;
    padding: 0.75rem 1rem;
    color: #1a1a1a !important;
}

/* Names */
.item-name {
    font-family: 'Playfair Display';
    font-weight: 700;
    color: #1a1a1a !important;
}

/* Meta */
.item-meta {
    color: #5a5040 !important;
}

/* Body text (FIXED invisible paragraphs) */
.item-body {
    color: #1a1a1a !important;
}

/* Emails / long text */
.email-pre {
    color: #2a2a2a !important;
    font-size: 0.75rem;
    background: #f0ece4;
    padding: 0.4rem;
    border-radius: 4px;
}

/* Badges */
.badge {
    display: inline-block;
    font-size: 0.7rem;
    padding: 2px 6px;
    border-radius: 4px;
    margin-right: 4px;
}
.badge-green { background: #e8f5e8; color: #2a7a2a !important; }
.badge-gold { background: #f5efe0; color: #8a6a2a !important; }
.badge-gray { background: #eee; color: #555 !important; }
.badge-blue { background: #e8eefc; color: #2a4a8a !important; }

/* Metrics (fix $14,300 etc) */
label[data-testid="stWidgetLabel"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #3a3228 !important;   /* darker, visible */
    font-weight: 500;
}
            
/* 🔥 FIX METRICS (Attendance, Revenue, Baseline Price) */
[data-testid="stMetricValue"] {
    color: #1a1a1a !important;
    font-weight: 800;
}

[data-testid="stMetricLabel"] {
    color: #5a5040 !important;
}

/* 🔥 FIX GTM SUMMARY TEXT */
.gtm-summary {
    color: #1a1a1a !important;
    background: #faf8f3;
    border: 1px solid #ece4d4;
    padding: 0.75rem 1rem;
    border-radius: 4px;
    font-size: 0.9rem;
    line-height: 1.6;
}

/* 🔥 SAFETY: fix markdown containers */
.stMarkdown, .stMarkdown * {
    color: #1a1a1a;
}

/* also catch edge cases */
div[data-testid="stWidgetLabel"] {
    color: #3a3228 !important;
}

/* Pricing */
.price-card {
    background: #faf8f4;
    border: 1px solid #ece4d4;
}
.price-value {
    color: #2a7a2a !important;
}

/* Tabs fix (THIS WAS MAJOR ISSUE) */
button[data-baseweb="tab"] {
    color: #5a5040 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #1a1a1a !important;
    font-weight: 600;
}

/* Dataframe text */
.stDataFrame {
    color: #1a1a1a !important;
}

</style>
""", unsafe_allow_html=True)
# ─────────────────────────────────────────────────────────────────────────────
# Session state bootstrap
# ─────────────────────────────────────────────────────────────────────────────
_DEFAULTS: dict[str, Any] = {
    "running": False,
    "done": False,
    "result": None,
    "error": None,
    "agent_statuses": {},
    "_state_input": None,
}
for _k, _v in _DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ─────────────────────────────────────────────────────────────────────────────
# Agent pipeline topology
# ─────────────────────────────────────────────────────────────────────────────
AGENTS: list[tuple[str, str]] = [
    ("sponsor_agent", "Sponsor Agent"),
    ("speaker_agent", "Speaker Agent"),
    ("venue_agent", "Venue Agent"),
    ("exhibitor_agent", "Exhibitor Agent"),
    ("gtm_agent", "GTM Agent"),
    ("pricing_agent", "Pricing Agent"),
    ("ops_agent", "Event Ops Agent"),
    ("final_agent", "Final Synthesis"),
]
PARALLEL_START = {
    "sponsor_agent",
    "speaker_agent",
    "venue_agent",
    "exhibitor_agent",
    "gtm_agent",
}
# When a node finishes → which downstream nodes become runnable
UNLOCKS: dict[str, list[str]] = {
    "venue_agent": ["pricing_agent", "ops_agent"],
    "speaker_agent": ["ops_agent"],
    "pricing_agent": [],
    "ops_agent": [],
    "sponsor_agent": [],
    "exhibitor_agent": [],
    "gtm_agent": [],
}


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline runner — streams LangGraph, updates statuses, returns final state
# ─────────────────────────────────────────────────────────────────────────────

def render_pipeline_graph():
    s = st.session_state.agent_statuses

    def stl(k):
        return STATE_LABELS.get(s.get(k, "pending"))

    st.markdown(f"""
    <div style="
        padding:1rem;
        background:#faf8f3;
        border:1px solid #e0d8c8;
        border-radius:4px;
        font-family:'IBM Plex Mono', monospace;
        font-size:0.75rem;
        line-height:1.8;
        color:#3a3228;
    ">
    <b style="font-size:0.7rem;letter-spacing:0.1em;color:#8a6a2a;">
    EXECUTION GRAPH
    </b><br><br>

    START<br>
    ├── Sponsor ────────────────┐ <span style="color:#7a6a55;">({stl("sponsor_agent")})</span><br>
    ├── Speaker ───┐            │ <span style="color:#7a6a55;">({stl("speaker_agent")})</span><br>
    ├── Venue ──┬──┴──▶ Ops ────┼──▶ Final ─▶ END<br>
    │           │               │ <span style="color:#7a6a55;">({stl("ops_agent")})</span> <span style="color:#7a6a55;">({stl("final_agent")})</span><br>
    │           └──▶ Pricing ───┤ <span style="color:#7a6a55;">({stl("pricing_agent")})</span><br>
    ├── Exhibitor ──────────────┤ <span style="color:#7a6a55;">({stl("exhibitor_agent")})</span><br>
    └── GTM ────────────────────┘ <span style="color:#7a6a55;">({stl("gtm_agent")})</span><br>

    </div>
    """, unsafe_allow_html=True)


async def run_pipeline(state_input: dict, graph_placeholder) -> dict:
    graph = build_graph()

    accumulated: dict[str, Any] = {
        "outputs": {},
        "agent_meta": {},
        "shared_memory": {},
        "logs": [],
        "errors": [],
    }

    # initialize parallel agents
    for ak in PARALLEL_START:
        st.session_state.agent_statuses[ak] = "running"

    # 🔥 render initial state
    with graph_placeholder:
        render_pipeline_graph()

    async for chunk in graph.astream(state_input, stream_mode="updates"):
        for node_name, patch in chunk.items():

            # mark done
            st.session_state.agent_statuses[node_name] = "done"

            # ---- merge state ----
            for k, v in patch.items():
                if isinstance(v, dict) and isinstance(accumulated.get(k), dict):
                    accumulated[k] = {**accumulated[k], **v}
                elif isinstance(v, list) and isinstance(accumulated.get(k), list):
                    accumulated[k] = accumulated[k] + v
                else:
                    accumulated[k] = v

            # ---- unlock downstream ----
            for downstream in UNLOCKS.get(node_name, []):
                if st.session_state.agent_statuses.get(downstream, "pending") == "pending":
                    st.session_state.agent_statuses[downstream] = "running"

            # 🔥 LIVE UI UPDATE (this is the key fix)
            with graph_placeholder:
                render_pipeline_graph()

    return accumulated


# ─────────────────────────────────────────────────────────────────────────────
# Pipeline widget renderer
# ─────────────────────────────────────────────────────────────────────────────
STATE_LABELS = {
    "pending": "— waiting",
    "running": "⟳ running",
    "done": "✓ done",
    "failed": "✗ failed",
}


# ─────────────────────────────────────────────────────────────────────────────
# Output renderers
# ─────────────────────────────────────────────────────────────────────────────
def _badge(text: str, kind: str = "gray") -> str:
    return f'<span class="badge badge-{kind}">{text}</span>'


def render_sponsors(out) -> None:
    sponsors = getattr(out, "sponsors", [])
    if not sponsors:
        st.info("No sponsor data.")
        return
    for s in sponsors:
        score = getattr(s, "relevance_score", 0)
        color = "green" if score >= 0.7 else "gold" if score >= 0.4 else "gray"
        st.markdown(
            f'<div class="item-card">'
            f'<div class="item-name">{s.name}</div>'
            f'<div class="item-meta">Industry: {s.industry}</div>'
            f'{_badge(f"relevance {score:.0%}", color)}'
            f'<div class="item-body">{s.reason}</div>'
            f'<div class="email-pre">{s.outreach_email}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


def render_speakers(out) -> None:
    speakers = getattr(out, "speakers", [])
    if not speakers:
        st.info("No speaker data.")
        return
    for sp in speakers:
        infl = getattr(sp, "influence_score", 0)
        ic = "green" if infl >= 0.7 else "gold" if infl >= 0.4 else "gray"
        bio = (sp.bio_summary or "")[:300]
        bio_suffix = "…" if len(sp.bio_summary or "") > 300 else ""
        st.markdown(
            f'<div class="item-card">'
            f'<div class="item-name">{sp.name}</div>'
            f'<div class="item-meta">{sp.title} — {sp.company}</div>'
            f'{_badge(f"influence {infl:.0%}", ic)}'
            f'{_badge(sp.suggested_topic, "blue")}'
            f'<div class="item-body">{bio}{bio_suffix}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


def render_venues(out) -> None:
    venues = getattr(out, "venues", [])
    if not venues:
        st.info("No venue data.")
        return
    for v in venues:
        st.markdown(
            f'<div class="item-card">'
            f'<div class="item-name">{v.name}</div>'
            f'<div class="item-meta">📍 {v.city}</div>'
            f'{_badge(f"cap {v.capacity:,}", "blue")}'
            f'{_badge(f"${v.price_per_day_usd:,}/day", "gold")}'
            f'<div class="item-body">{v.notes}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


def render_exhibitors(out) -> None:
    exhibitors = getattr(out, "exhibitors", [])
    if not exhibitors:
        st.info("No exhibitor data.")
        return
    for e in exhibitors:
        conf = getattr(e, "confidence", None)
        conf_html = _badge(f"{conf:.0%}", "gray") if conf is not None else ""
        st.markdown(
            f'<div class="item-card">'
            f'<div class="item-name">{e.name}</div>'
            f'<div class="item-meta">Category: {e.category}</div>'
            f"{conf_html}"
            f'<div class="item-body">{e.description}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


def render_pricing(out) -> None:
    tiers = getattr(out, "tiers", [])
    attendance = getattr(out, "predicted_attendance", 0)
    revenue = getattr(out, "predicted_revenue_usd", 0)
    baseline = getattr(out, "baseline_price_usd", None)

    # Clean metrics row
    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Attendance", f"{attendance:,}")
    with c2:
        st.metric("Revenue", f"${revenue:,}")
    with c3:
        if baseline:
            st.metric("Baseline Price", f"${baseline:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tier cards
    for t in tiers:
        st.markdown(
            f"""
            <div class="price-card">
                <div>
                    <div class="item-name">{t.name}</div>
                    <div class="item-meta">
                        {t.expected_conversions:,} conversions
                    </div>
                </div>
                <div class="price-value">
                    ${t.price_usd:,}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_ops(out) -> None:
    schedule = getattr(out, "schedule", [])
    conflicts = getattr(out, "conflicts", [])
    rooms = getattr(out, "rooms", [])

    if conflicts:
        st.markdown("**⚠️ Conflicts detected**")
        for c in conflicts:
            st.markdown(
                f'<div class="conflict-badge">{c}</div>', unsafe_allow_html=True
            )

    if not schedule:
        st.info("No schedule data.")
        return

    rows = [
        {
            "Time": f"{slot.start} – {slot.end}",
            "Speaker": slot.speaker,
            "Topic": slot.topic,
            "Room": slot.room,
            "Capacity": slot.room_capacity,
        }
        for slot in schedule
    ]
    st.dataframe(rows, use_container_width=True, hide_index=True)

    if rooms:
        st.markdown("<br>**Rooms**", unsafe_allow_html=True)
        for r in rooms:
            st.markdown(
                f'<div class="item-card"><div class="item-body">{r}</div></div>',
                unsafe_allow_html=True,
            )


def render_gtm(out) -> None:
    summary = getattr(out, "gtm_summary", "")
    promotions = getattr(out, "promotions", [])

    if summary:
        st.markdown(f'<div class="gtm-summary">{summary}</div>', unsafe_allow_html=True)

    if not promotions:
        st.info("No GTM data.")
        return

    for p in promotions:
        conf = getattr(p, "confidence", None)
        conf_html = _badge(f"{conf:.0%}", "gray") if conf is not None else ""
        st.markdown(
            f'<div class="item-card">'
            f'<div class="item-name">{p.community_name}</div>'
            f'<div class="item-meta">Platform: {p.platform} · Niche: {p.niche}</div>'
            f'{_badge(p.recommended_post_date, "blue")}{conf_html}'
            f'<div class="email-pre">{p.message_draft}</div>'
            f"</div>",
            unsafe_allow_html=True,
        )


def render_results(final) -> None:
    tabs = st.tabs(
        [
            "🤝 Sponsors",
            "🎤 Speakers",
            "🏛️ Venues",
            "🧩 Exhibitors",
            "💰 Pricing",
            "📅 Schedule",
            "📣 GTM",
        ]
    )
    with tabs[0]:
        render_sponsors(final.sponsors)
    with tabs[1]:
        render_speakers(final.speakers)
    with tabs[2]:
        render_venues(final.venues)
    with tabs[3]:
        render_exhibitors(final.exhibitors)
    with tabs[4]:
        render_pricing(final.pricing)
    with tabs[5]:
        render_ops(final.ops)
    with tabs[6]:
        render_gtm(final.gtm)


# ─────────────────────────────────────────────────────────────────────────────
# Reset
# ─────────────────────────────────────────────────────────────────────────────
def reset() -> None:
    for k in list(st.session_state.keys()):
        del st.session_state[k]


# ─────────────────────────────────────────────────────────────────────────────
# Page layout
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="ef-wordmark">EventForge AI</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="ef-sub">Agentic Conference Intelligence · IIT Roorkee HighPrep 2026</div>',
    unsafe_allow_html=True,
)
st.markdown('<hr class="ef-rule">', unsafe_allow_html=True)

left_col, right_col = st.columns([2, 1], gap="large")

# ── RIGHT: pipeline status panel ─────────────────────────────────────────────
with right_col:
    st.markdown(
        '<div class="section-label">Agent Pipeline</div>', unsafe_allow_html=True
    )
    graph_placeholder = st.empty()
    with graph_placeholder:
        render_pipeline_graph()

    if not st.session_state.running and not st.session_state.done:
        st.markdown(
            '<div style="margin-top:1.2rem;padding:0.9rem 1rem;background:#faf8f3;'
            "border:1px solid #e0d8c8;border-radius:3px;font-family:'IBM Plex Mono',monospace;"
            'font-size:0.68rem;color:#9a8a6a;line-height:1.9;">'
            '<div style="color:#8a6a2a;margin-bottom:0.4rem;font-size:0.65rem;'
            'letter-spacing:0.15em;text-transform:uppercase;">Execution Topology</div>'
            "START<br>"
            "├── Sponsor ────────────────────┐<br>"
            "├── Speaker ───┐                │<br>"
            "├── Venue ──┬──┴─▶ Ops Agent    ├──▶ Final ──▶ END<br>"
            "│           └──▶ Pricing ───────┤<br>"
            "├── Exhibitor ───────────────────┤<br>"
            "└── GTM ─────────────────────────┘"
            "</div>",
            unsafe_allow_html=True,
        )

# ── LEFT: form / running / results ───────────────────────────────────────────
with left_col:

    # ── FORM ──────────────────────────────────────────────────────────────────
    if not st.session_state.running and not st.session_state.done:
        st.markdown(
            '<div class="section-label">Event Details</div>', unsafe_allow_html=True
        )

        with st.form("event_form"):
            category = st.text_input(
                "Conference Category",
                placeholder="e.g. AI & Machine Learning, FinTech, Climate Tech…",
            )
            geography = st.text_input(
                "Geography",
                placeholder="e.g. India, Europe, San Francisco, Singapore…",
            )
            audience_size = st.number_input(
                "Target Audience Size", min_value=1, value=500, step=50
            )
            col_a, col_b = st.columns(2)
            with col_a:
                duration_days = st.number_input(
                    "Duration (days)", min_value=1, max_value=10, value=1, step=1
                )
            with col_b:
                budget_usd = st.number_input(
                    "Budget USD (0 = unspecified)", min_value=0, value=0, step=5000
                )
            submitted = st.form_submit_button(
                "Run EventForge →", use_container_width=True
            )

        if submitted:
            if not category.strip():
                st.error("Please enter a conference category.")
            elif not geography.strip():
                st.error("Please enter a geography.")
            else:
                st.session_state._state_input = {
                    "input": {
                        "category": category.strip(),
                        "geography": geography.strip(),
                        "audience_size": int(audience_size),
                        "duration_days": int(duration_days),
                        "budget_usd": int(budget_usd) if budget_usd else None,
                    },
                    "outputs": {},
                    "agent_meta": {},
                    "shared_memory": {},
                    "logs": [],
                    "errors": [],
                }
                st.session_state.agent_statuses = {k: "pending" for k, _ in AGENTS}
                st.session_state.running = True
                st.session_state.done = False
                st.session_state.result = None
                st.session_state.error = None
                st.rerun()

    # ── RUNNING ───────────────────────────────────────────────────────────────
    elif st.session_state.running and not st.session_state.done:
        inp = st.session_state._state_input["input"]
        st.markdown(
            f'<div style="padding:0.8rem 1rem;background:#faf8f3;border:1px solid #e0d8c8;'
            f"border-radius:3px;font-family:'IBM Plex Mono',monospace;font-size:0.78rem;"
            f'color:#5a5040;margin-bottom:1rem;">'
            f'▶ <strong style="color:#1a1a1a;">{inp["category"]}</strong>'
            f' · {inp["geography"]} · {inp["audience_size"]:,} attendees'
            f"</div>",
            unsafe_allow_html=True,
        )

        with st.spinner("Agents are running… check the pipeline panel →"):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                logger.info("UI: starting pipeline run")
                final_state = loop.run_until_complete(
                    run_pipeline(st.session_state._state_input, graph_placeholder)
                )
                logger.info("UI: pipeline complete")
                st.session_state.result = final_state
                # Safety net: mark any stuck agents done
                for k, _ in AGENTS:
                    if st.session_state.agent_statuses.get(k) in ("pending", "running"):
                        st.session_state.agent_statuses[k] = "done"
            except Exception as exc:
                logger.exception("UI: pipeline failed")
                st.session_state.error = str(exc)
                for k, _ in AGENTS:
                    if st.session_state.agent_statuses.get(k) == "running":
                        st.session_state.agent_statuses[k] = "failed"
            finally:
                loop.close()
                st.session_state.running = False
                st.session_state.done = True

        st.rerun()

    # ── DONE ──────────────────────────────────────────────────────────────────
    elif st.session_state.done:
        inp = st.session_state._state_input["input"]

        col_status, col_btn = st.columns([3, 1])
        with col_status:
            st.markdown(
                f'<div style="padding:0.7rem 1rem;background:#f0f8f0;border:1px solid #7aaa7a;'
                f"border-radius:3px;font-family:'IBM Plex Mono',monospace;font-size:0.78rem;\">"
                f'<span style="color:#2a7a2a;font-weight:600;">✓ Pipeline complete</span>&nbsp;&nbsp;'
                f'<span style="color:#5a5040;">{inp["category"]} · {inp["geography"]} '
                f'· {inp["audience_size"]:,} attendees</span>'
                f"</div>",
                unsafe_allow_html=True,
            )
        with col_btn:
            if st.button("↩ New Query"):
                reset()
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.session_state.error:
            st.error(f"Pipeline error:\n\n{st.session_state.error}")
        else:
            outputs = st.session_state.result.get("outputs", {})
            final = outputs.get("final_agent")
            if final is None:
                st.warning(
                    "Pipeline finished but no final_agent output found. Check terminal logs."
                )
            else:
                render_results(final)

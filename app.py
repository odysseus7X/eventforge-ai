"""
EventForge AI — Streamlit Demo UI
Chatbot-style input collection → live agent progress → rich output display.
Run: streamlit run app.py
"""

import asyncio
import streamlit as st
import time
import sys
import os

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EventForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0a0a0f;
    color: #e8e4d9;
}

.stApp {
    background: #0a0a0f;
}

/* Hide default streamlit stuff */
#MainMenu, footer, header { visibility: hidden; }

/* Title */
.ef-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.8rem;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #f0e6c8 0%, #d4a853 50%, #e8c87a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
    line-height: 1.1;
}

.ef-subtitle {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #5a5a6e;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.3rem;
    margin-bottom: 2rem;
}

/* Chat bubble - bot */
.chat-bot {
    background: #141420;
    border: 1px solid #2a2a3e;
    border-left: 3px solid #d4a853;
    border-radius: 0 12px 12px 12px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.88rem;
    max-width: 72%;
    color: #c8c4b8;
    position: relative;
}

.chat-bot::before {
    content: '⚡ EventForge';
    display: block;
    font-size: 0.65rem;
    color: #d4a853;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
    font-weight: 500;
}

/* Chat bubble - user */
.chat-user {
    background: #1a1a2e;
    border: 1px solid #3a3a52;
    border-right: 3px solid #7c6aff;
    border-radius: 12px 0 12px 12px;
    padding: 0.9rem 1.2rem;
    margin: 0.6rem 0 0.6rem auto;
    font-size: 0.88rem;
    max-width: 60%;
    color: #c8c4b8;
    text-align: right;
    position: relative;
}

.chat-user::after {
    content: 'You';
    display: block;
    font-size: 0.65rem;
    color: #7c6aff;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.4rem;
    font-weight: 500;
}

/* Agent status cards */
.agent-card {
    background: #0f0f1a;
    border: 1px solid #2a2a3e;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin: 0.3rem 0;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    font-size: 0.82rem;
    transition: all 0.3s ease;
}

.agent-card.running {
    border-color: #d4a853;
    background: #141410;
    box-shadow: 0 0 12px rgba(212, 168, 83, 0.1);
}

.agent-card.done {
    border-color: #3a7a4a;
    background: #0f140f;
}

.agent-card.pending {
    opacity: 0.4;
}

.status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}

.dot-pending { background: #444; }
.dot-running { background: #d4a853; animation: pulse 1s infinite; }
.dot-done    { background: #4caf50; }
.dot-failed  { background: #e05252; }

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}

/* Output cards */
.output-section {
    background: #0f0f1a;
    border: 1px solid #2a2a3e;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 1rem;
}

.output-section-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #d4a853;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid #2a2a3e;
    padding-bottom: 0.5rem;
}

.item-card {
    background: #141420;
    border: 1px solid #222235;
    border-radius: 6px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.6rem;
    font-size: 0.8rem;
}

.item-name {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 0.9rem;
    color: #e8e4d9;
    margin-bottom: 0.3rem;
}

.item-meta {
    color: #6a6a80;
    font-size: 0.75rem;
    margin-bottom: 0.2rem;
}

.score-badge {
    display: inline-block;
    background: #1e1e0a;
    border: 1px solid #d4a853;
    color: #d4a853;
    border-radius: 4px;
    padding: 0.1rem 0.4rem;
    font-size: 0.7rem;
    margin-right: 0.4rem;
}

.price-badge {
    display: inline-block;
    background: #0a1e0a;
    border: 1px solid #4caf50;
    color: #4caf50;
    border-radius: 4px;
    padding: 0.1rem 0.4rem;
    font-size: 0.7rem;
}

/* Divider */
.ef-divider {
    border: none;
    border-top: 1px solid #1e1e2e;
    margin: 1.5rem 0;
}

/* Email block */
.email-block {
    background: #0a0a14;
    border: 1px solid #1e1e35;
    border-radius: 4px;
    padding: 0.6rem 0.8rem;
    font-size: 0.72rem;
    color: #7a7a9a;
    margin-top: 0.4rem;
    font-style: italic;
    line-height: 1.5;
}

/* Revenue highlight */
.revenue-highlight {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4caf50, #8bc34a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Input area styling */
.stTextInput > div > div > input {
    background: #141420 !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 8px !important;
    color: #e8e4d9 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.88rem !important;
}

.stNumberInput > div > div > input {
    background: #141420 !important;
    border: 1px solid #2a2a3e !important;
    color: #e8e4d9 !important;
    font-family: 'DM Mono', monospace !important;
}

.stSelectbox > div > div {
    background: #141420 !important;
    border: 1px solid #2a2a3e !important;
    color: #e8e4d9 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #d4a853, #b8872a) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-size: 0.8rem !important;
    padding: 0.5rem 1.5rem !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #e8c87a, #d4a853) !important;
    transform: translateY(-1px);
}
</style>
""", unsafe_allow_html=True)

# ── State init ─────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "step": 0,            # which question we're on
        "answers": {},        # collected answers
        "chat_log": [],       # list of (role, text)
        "pipeline_done": False,
        "result": None,
        "agent_statuses": {},
        "pipeline_started": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── Questions config ───────────────────────────────────────────────────────────
QUESTIONS = [
    {
        "key": "category",
        "bot": "👋 Welcome to **EventForge AI**! Let's plan your conference.\n\nFirst — what's the **category or theme** of your event?",
        "placeholder": "e.g. AI & Machine Learning, FinTech, SaaS, Healthcare...",
        "type": "text",
    },
    {
        "key": "geography",
        "bot": "Great choice! Now, what **geography** are you targeting — where will attendees primarily be from?",
        "placeholder": "e.g. San Francisco, India, Europe, Global...",
        "type": "text",
    },
    {
        "key": "audience_size",
        "bot": "Perfect. What's the **expected audience size** for your event?",
        "placeholder": "e.g. 500",
        "type": "number",
    },
    {
        "key": "duration_days",
        "bot": "How many **days** will the conference run?",
        "type": "select",
        "options": [1, 2, 3, 4, 5],
    },
    {
        "key": "budget_usd",
        "bot": "Finally — what's your **budget** (USD)? Enter 0 to skip.",
        "placeholder": "e.g. 50000",
        "type": "number",
    },
]

# ── Helpers ────────────────────────────────────────────────────────────────────
def bot_bubble(text):
    st.markdown(f'<div class="chat-bot">{text}</div>', unsafe_allow_html=True)

def user_bubble(text):
    col1, col2 = st.columns([1, 3])
    with col2:
        st.markdown(f'<div class="chat-user">{text}</div>', unsafe_allow_html=True)

def render_chat_log():
    for role, text in st.session_state.chat_log:
        if role == "bot":
            bot_bubble(text)
        else:
            user_bubble(text)

def agent_status_html(name, status, elapsed=None):
    dot_class = f"dot-{status}"
    card_class = f"agent-card {status}"
    label = {
        "pending": "Waiting...",
        "running": "Running" + (" · " + elapsed if elapsed else ""),
        "done": "✓ Done" + (" · " + elapsed if elapsed else ""),
        "failed": "✗ Failed",
    }.get(status, status)
    return f"""
    <div class="{card_class}">
        <span class="status-dot {dot_class}"></span>
        <span style="font-family:'Syne',sans-serif;font-weight:600;color:#c8c4b8;">{name}</span>
        <span style="color:#5a5a6e;margin-left:auto;font-size:0.75rem;">{label}</span>
    </div>
    """

# ── Header ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="ef-title">⚡ EventForge AI</div>', unsafe_allow_html=True)
st.markdown('<div class="ef-subtitle">Agentic Conference Intelligence Platform</div>', unsafe_allow_html=True)

col_chat, col_status = st.columns([3, 2], gap="large")

# ── LEFT: Chat ──────────────────────────────────────────────────────────────────
with col_chat:

    # If pipeline is done, show results
    if st.session_state.pipeline_done and st.session_state.result:
        render_chat_log()
        st.markdown('<hr class="ef-divider">', unsafe_allow_html=True)

        result = st.session_state.result
        outputs = result.get("outputs", {})

        final = outputs.get("final_agent")
        if final is None:
            st.error("Pipeline completed but no final output found. Check agent logs.")
        else:
            # ── Sponsors ──────────────────────────────────────────────────────
            sponsors_out = final.sponsors
            sponsors = sponsors_out.sponsors if hasattr(sponsors_out, "sponsors") else []
            st.markdown('<div class="output-section">', unsafe_allow_html=True)
            st.markdown('<div class="output-section-title">🤝 Recommended Sponsors</div>', unsafe_allow_html=True)
            for s in sponsors:
                relevance = getattr(s, "relevance_score", 0)
                st.markdown(f"""
                <div class="item-card">
                    <div class="item-name">{s.name}</div>
                    <div class="item-meta">Industry: {s.industry}</div>
                    <span class="score-badge">relevance {relevance:.0%}</span>
                    <div style="color:#8a8a9a;font-size:0.78rem;margin-top:0.4rem;">{s.reason}</div>
                    <div class="email-block">📧 {s.outreach_email[:280]}{'...' if len(s.outreach_email)>280 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Speakers ──────────────────────────────────────────────────────
            speakers_out = final.speakers
            speakers = speakers_out.speakers if hasattr(speakers_out, "speakers") else []
            st.markdown('<div class="output-section">', unsafe_allow_html=True)
            st.markdown('<div class="output-section-title">🎤 Suggested Speakers</div>', unsafe_allow_html=True)
            for sp in speakers:
                infl = getattr(sp, "influence_score", 0)
                st.markdown(f"""
                <div class="item-card">
                    <div class="item-name">{sp.name}</div>
                    <div class="item-meta">{sp.title} @ {sp.company}</div>
                    <span class="score-badge">influence {infl:.0%}</span>
                    <div style="color:#8a8a9a;font-size:0.78rem;margin-top:0.4rem;">Topic: <em>{sp.suggested_topic}</em></div>
                    <div style="color:#6a6a80;font-size:0.75rem;margin-top:0.3rem;">{sp.bio_summary[:200]}{'...' if len(sp.bio_summary)>200 else ''}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Venues ────────────────────────────────────────────────────────
            venues_out = final.venues
            venues = venues_out.venues if hasattr(venues_out, "venues") else []
            st.markdown('<div class="output-section">', unsafe_allow_html=True)
            st.markdown('<div class="output-section-title">🏛️ Venue Options</div>', unsafe_allow_html=True)
            for v in venues:
                st.markdown(f"""
                <div class="item-card">
                    <div class="item-name">{v.name}</div>
                    <div class="item-meta">📍 {v.city} &nbsp;|&nbsp; 👥 Capacity: {v.capacity:,} &nbsp;|&nbsp; 💵 ${v.price_per_day_usd:,}/day</div>
                    <div style="color:#8a8a9a;font-size:0.78rem;margin-top:0.3rem;">{v.notes}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ── Pricing ───────────────────────────────────────────────────────
            pricing_out = final.pricing
            tiers = pricing_out.tiers if hasattr(pricing_out, "tiers") else []
            predicted_attendance = getattr(pricing_out, "predicted_attendance", "—")
            predicted_revenue = getattr(pricing_out, "predicted_revenue_usd", 0)
            st.markdown('<div class="output-section">', unsafe_allow_html=True)
            st.markdown('<div class="output-section-title">💰 Ticket Pricing Strategy</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display:flex;gap:2rem;margin-bottom:1rem;">
                <div>
                    <div style="font-size:0.7rem;color:#5a5a6e;letter-spacing:0.1em;text-transform:uppercase;">Predicted Attendance</div>
                    <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:#c8c4b8;">{predicted_attendance:,}</div>
                </div>
                <div>
                    <div style="font-size:0.7rem;color:#5a5a6e;letter-spacing:0.1em;text-transform:uppercase;">Predicted Revenue</div>
                    <div class="revenue-highlight">${predicted_revenue:,}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            for t in tiers:
                st.markdown(f"""
                <div class="item-card" style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div class="item-name">{t.name}</div>
                        <div class="item-meta">Expected conversions: {t.expected_conversions}</div>
                    </div>
                    <span class="price-badge" style="font-size:0.9rem;padding:0.3rem 0.7rem;">${t.price_usd:,}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🔄 Plan Another Event"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    # If pipeline is running, show chat log + spinner
    elif st.session_state.pipeline_started:
        render_chat_log()
        bot_bubble("🔍 Agents are working on your conference plan. Check the live status →")

    # Otherwise, show chat + input form
    else:
        render_chat_log()

        step = st.session_state.step
        if step < len(QUESTIONS):
            q = QUESTIONS[step]

            # Show bot question if not already in chat_log
            if not st.session_state.chat_log or st.session_state.chat_log[-1] != ("bot", q["bot"]):
                st.session_state.chat_log.append(("bot", q["bot"]))
                st.rerun()

            # Input widget
            with st.form(key=f"form_{step}", clear_on_submit=True):
                if q["type"] == "text":
                    val = st.text_input("", placeholder=q.get("placeholder", ""), label_visibility="collapsed")
                elif q["type"] == "number":
                    val = st.number_input("", min_value=0, value=0, label_visibility="collapsed")
                elif q["type"] == "select":
                    val = st.selectbox("", q["options"], label_visibility="collapsed")

                submitted = st.form_submit_button("→ Send")
                if submitted:
                    if q["type"] == "text" and not str(val).strip():
                        st.warning("Please enter a value.")
                    else:
                        display_val = str(val) if q["type"] != "number" else f"{int(val):,}"
                        st.session_state.chat_log.append(("user", display_val))
                        st.session_state.answers[q["key"]] = val
                        st.session_state.step += 1
                        st.rerun()

        else:
            # All questions answered — show summary and launch button
            a = st.session_state.answers
            bot_bubble(f"""
            ✅ Got everything! Here's your event summary:<br><br>
            <strong>Category:</strong> {a['category']}<br>
            <strong>Geography:</strong> {a['geography']}<br>
            <strong>Audience Size:</strong> {int(a['audience_size']):,}<br>
            <strong>Duration:</strong> {a['duration_days']} day(s)<br>
            <strong>Budget:</strong> {'$' + f"{int(a['budget_usd']):,}" if a['budget_usd'] else 'Not specified'}
            """)

            if st.button("⚡ Launch EventForge Agents"):
                st.session_state.pipeline_started = True
                st.rerun()

# ── RIGHT: Agent Live Status + Pipeline ────────────────────────────────────────
with col_status:
    st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#5a5a6e;margin-bottom:0.8rem;">Agent Pipeline</div>', unsafe_allow_html=True)

    AGENTS = [
        ("sponsor_agent",  "Sponsor Agent"),
        ("speaker_agent",  "Speaker Agent"),
        ("venue_agent",    "Venue Agent"),
        ("pricing_agent",  "Pricing Agent"),
        ("final_agent",    "Final Synthesis"),
    ]

    agent_statuses = st.session_state.agent_statuses
    agent_placeholders = {}
    for key, label in AGENTS:
        status = agent_statuses.get(key, "pending")
        ph = st.empty()
        ph.markdown(agent_status_html(label, status), unsafe_allow_html=True)
        agent_placeholders[key] = (ph, label)

    # ── Run the pipeline ONCE ─────────────────────────────────────────────────
    if st.session_state.pipeline_started and not st.session_state.pipeline_done:
        # Guard: don't re-run if already done
        import threading

        a = st.session_state.answers
        state_input = {
            "input": {
                "category": a["category"],
                "geography": a["geography"],
                "audience_size": int(a["audience_size"]),
                "duration_days": int(a["duration_days"]),
                "budget_usd": int(a["budget_usd"]) if a.get("budget_usd") else None,
            },
            "outputs": {},
            "agent_meta": {},
            "shared_memory": {},
            "logs": [],
            "errors": [],
        }

        # ── Async runner with live status updates ─────────────────────────────
        async def run_pipeline_with_status():
            # Import here to avoid issues if path not set
            try:
                from eventforge.graph.builder import build_graph
            except ImportError as e:
                return {"_error": str(e)}

            graph = build_graph()

            # We'll stream events from the graph
            start_times = {}
            finished_agents = set()

            # Update statuses via session state
            def set_status(agent_key, status, elapsed=None):
                st.session_state.agent_statuses[agent_key] = status

            # Use astream_events for live updates
            try:
                async for event in graph.astream_events(state_input, version="v2"):
                    kind = event.get("event")
                    name = event.get("name", "")

                    # Map node names to our agent keys
                    agent_key = name if name in dict(AGENTS) else None

                    if kind == "on_chain_start" and agent_key:
                        start_times[agent_key] = time.time()
                        st.session_state.agent_statuses[agent_key] = "running"

                    elif kind == "on_chain_end" and agent_key:
                        elapsed = time.time() - start_times.get(agent_key, time.time())
                        st.session_state.agent_statuses[agent_key] = "done"
                        finished_agents.add(agent_key)

                # After stream ends, get the final result by re-invoking (same graph, same state)
                # Actually astream_events doesn't return the final state easily.
                # So we invoke separately, but ONLY after streaming is done.
                result = await graph.ainvoke(state_input)
                return result

            except Exception as e:
                return {"_error": str(e)}

        # We need a different approach: use astream to get state updates + final result
        # to avoid double LLM calls. Let's use astream with stream_mode="updates".
        async def run_pipeline_streaming():
            try:
                from eventforge.graph.builder import build_graph
            except ImportError as e:
                return None, str(e)

            graph = build_graph()
            start_times = {}
            final_state = {}

            try:
                # Mark parallel starters as running immediately
                for ak in ["sponsor_agent", "speaker_agent", "venue_agent"]:
                    st.session_state.agent_statuses[ak] = "running"
                    start_times[ak] = time.time()

                async for chunk in graph.astream(state_input, stream_mode="updates"):
                    # chunk is {node_name: node_output_dict}
                    for node_name, node_output in chunk.items():
                        if node_name in dict(AGENTS):
                            elapsed = time.time() - start_times.get(node_name, time.time())
                            st.session_state.agent_statuses[node_name] = "done"
                            # Mark next agents as running based on graph topology
                            if node_name == "venue_agent":
                                st.session_state.agent_statuses["pricing_agent"] = "running"
                                start_times["pricing_agent"] = time.time()
                            if node_name == "pricing_agent":
                                st.session_state.agent_statuses["final_agent"] = "running"
                                start_times["final_agent"] = time.time()
                        # Accumulate state
                        final_state.update(node_output)

                return final_state, None

            except Exception as e:
                import traceback
                return None, traceback.format_exc()

        # Run the async pipeline
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        status_text = st.empty()
        status_text.markdown('<div style="color:#d4a853;font-size:0.8rem;margin-top:1rem;">⏳ Pipeline running...</div>', unsafe_allow_html=True)

        final_state, error = loop.run_until_complete(run_pipeline_streaming())
        loop.close()

        if error:
            st.session_state.pipeline_done = True
            st.session_state.result = {"_error": error}
            status_text.markdown(f'<div style="color:#e05252;font-size:0.8rem;margin-top:1rem;">❌ Pipeline failed</div>', unsafe_allow_html=True)
        else:
            st.session_state.pipeline_done = True
            st.session_state.result = {"outputs": final_state.get("outputs", {})}
            status_text.markdown('<div style="color:#4caf50;font-size:0.8rem;margin-top:1rem;">✅ Pipeline complete!</div>', unsafe_allow_html=True)

        # Update all agent placeholders to final statuses
        for key, (ph, label) in agent_placeholders.items():
            status = st.session_state.agent_statuses.get(key, "done")
            ph.markdown(agent_status_html(label, status), unsafe_allow_html=True)

        time.sleep(0.5)
        st.rerun()

    # Show graph topology hint
    if not st.session_state.pipeline_started:
        st.markdown("""
        <div style="margin-top:2rem;padding:1rem;background:#0f0f1a;border:1px solid #1e1e2e;border-radius:8px;font-size:0.75rem;color:#4a4a60;line-height:1.8;">
        <div style="color:#3a3a50;margin-bottom:0.5rem;font-family:'Syne',sans-serif;font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;">Execution Graph</div>
        START<br>
        ├── Sponsor Agent ─────┐<br>
        ├── Speaker Agent ─────┤→ Final Synthesis → END<br>
        └── Venue Agent → Pricing Agent ──┘<br>
        <br>
        <div style="color:#3a3a50;">Parallel execution with dependency resolution</div>
        </div>
        """, unsafe_allow_html=True)

    # Error display
    if st.session_state.pipeline_done and st.session_state.result and st.session_state.result.get("_error"):
        st.markdown(f"""
        <div style="background:#1a0a0a;border:1px solid #e05252;border-radius:8px;padding:1rem;margin-top:1rem;font-size:0.75rem;color:#e05252;font-family:'DM Mono',monospace;white-space:pre-wrap;">
{st.session_state.result['_error']}
        </div>
        """, unsafe_allow_html=True)
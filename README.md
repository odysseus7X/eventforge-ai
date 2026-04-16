# 🚀 EventForge AI

**EventForge AI** is a multi-agent AI system that automates and optimizes end-to-end event planning — from sponsors and speakers to venue selection and pricing.

---

## ✨ Overview

Planning a conference involves multiple complex decisions across sponsorships, speakers, venues, and pricing. EventForge AI simplifies this by orchestrating **specialized AI agents** that collaborate to generate a complete, data-driven event plan in seconds.

---

## 🧠 Architecture

```text
.
├── app.py                  # (optional UI entry point)
├── docs/                   # engineering notes
├── notebooks/              # experimentation (pricing, etc.)
├── pyproject.toml
│
└── src/eventforge/
    ├── main.py             # CLI entry point
    │
    ├── graph/              # LangGraph DAG builder
    │   ├── nodes.py        # Wraps agent.run into a LangGraph-compatible node
    │   └── builder.py
    │
    ├── agents/             # all agent implementations
    │   ├── base/           # BaseAgent abstraction
    │   ├── sponsor_agent.py
    │   ├── speaker_agent.py
    │   ├── venue_agent.py
    │   ├── pricing_agent.py
    │   └── final_agent.py
    │
    ├── models/             # schemas + state definitions
    │   ├── schemas.py      # input/output validation (Pydantic models)
    │   └── state.py        # shared execution state for graph
    │
    ├── data/               # datasets & static knowledge base
    │   ├── venues.csv      # venue listings
    │   └── events.csv      # example event inputs
    │
    ├── tools/              # external tools (web search, APIs)
    │
    ├── utils/              # shared utilities
    │   ├── llm_client.py   # LLM interface wrapper
    │   ├── logging.py      # logging & debugging
    │   └── validator.py
  
```
---

## 🧠 Key Features

- 🤖 **Multi-Agent System**
  - Sponsor Agent → Finds potential sponsors  
  - Speaker Agent → Recommends speakers  
  - Venue Agent → Suggests venues  
  - Pricing Agent → Generates pricing tiers  
  - Final Agent → Combines all outputs  

- ⚡ Fast, automated decision-making  
- 📊 Structured and explainable outputs  
- 🔄 Modular and extensible design  

---

## ⚙️ How It Works

1. User provides event details (type, budget, attendees, location)  
2. Agents run in parallel to solve specific tasks  
3. Outputs are aggregated into a final event plan  

---

## 📥 Input

- Event type  
- Expected attendees  
- Budget constraints  
- Location  

---

## 📤 Output

A complete AI-generated event plan including:

- 💰 Pricing strategy  
- 🏟️ Venue recommendations  
- 🎤 Speaker suggestions  
- 🤝 Sponsorship opportunities  

---

## ⚙️ Tech Stack

- LangChain / Agent frameworks  
- Pydantic  
- Async execution  

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <repo-url>
cd eventforge-ai
```

### 2. Install Dependencies
```bash
pip install -e .
```

### 3. Set up environment variables
```bash
API_KEY=your_api_key_here
TAVILY_API_KEY=your_tavily_key
OPENAI_API_KEY=your_llm_key
```

### 4. Run the application


-🖥️ Streamlit UI
```bash
streamlit run app.py
```

-💻CLI (terminal execution)
```bash
python src/eventforge/main.py
```


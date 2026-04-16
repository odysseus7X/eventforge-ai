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
├── src/eventforge/
│   ├── agents/             # all agent implementations
│   │   ├── base/           # BaseAgent abstraction
│   │   ├── sponsor_agent.py
│   │   ├── speaker_agent.py
│   │   ├── venue_agent.py
│   │   ├── pricing_agent.py
│   │   └── final_agent.py
│   │
│   ├── graph/              # LangGraph DAG builder
│   │   └── builder.py
│   │
│   ├── models/             # schemas + state definitions
│   │   ├── schemas.py
│   │   └── state.py
│   │
│   ├── tools/              # external tools (web search, etc.)
│   │
│   ├── utils/              # logging, LLM client
│   │
│   └── main.py             # CLI entry point
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
- Preferences  

---

## 📤 Output

A complete AI-generated event plan including:

- 💰 Pricing strategy  
- 🏟️ Venue recommendations  
- 🎤 Speaker suggestions  
- 🤝 Sponsorship opportunities  
- 📄 Final consolidated report  

---

## ⚙️ Tech Stack

- Python  
- LangChain / Agent frameworks  
- Pydantic  
- Async execution  

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <repo-url>
cd eventforge-ai

## Architecture

We built a multi-agent system using LangGraph.

### Key Concepts
- Parallel agent execution (Sponsor, Speaker, Venue)
- Dependency-based execution (Pricing depends on Venue)
- DAG-based orchestration using LangGraph
- Structured outputs using Pydantic schemas

### Workflow

START
 → [Sponsor, Speaker, Venue] (parallel)
 → Pricing (depends on Venue)
 → Join (synchronization barrier)
 → Final aggregation

### Features
- Async execution
- Modular agent design
- Extensible architecture for additional agents
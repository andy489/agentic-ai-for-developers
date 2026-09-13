# 05 — Developing Multi-agent Systems

Designing systems where multiple specialized agents collaborate, negotiate, and are coordinated to solve tasks — built with LangGraph. Covers multi-agent topologies (network, supervisor, hierarchical, swarm), human-in-the-loop workflows, negotiation strategies (auctions, Contract Net), and game theory applied to LLM agents.

## Notebook

- [multi-agent-systems-notes.ipynb](multi-agent-systems-notes.ipynb) — Course notes and runnable examples across three parts:

| Part | Topic |
|---|---|
| Part 1 — Fundamental Concepts | Agents & MAS, key attributes, MAS architecture, topologies (network / supervisor / hierarchical), LangGraph components, negotiation (auctions, Contract Net, argumentation) |
| Part 2 — Advanced Scenarios | Organizational structures, swarm-style architecture, teams, hierarchies ("Dressing Right for the Weather") |
| Part 3 — Game Theory | Kinds of games, complete vs. incomplete information, Prisoner's Dilemma, payoff matrix, dominant strategy, Nash equilibrium, game-theoretic strategies for LLM agents |

## Demos

### Demo 1 — Fundamental Concepts (`demos/demo-1/`)

Coordination and human-in-the-loop patterns with a supervisor routing between specialized workers.

| Notebook | Topic |
|---|---|
| `src/cnp.ipynb` | Contract Net Protocol — lift controller routes the closest elevator to a requesting floor |
| `src/dressing_planner.ipynb` | Supervisor coordinating weather-reporting and dressing-planner workers |
| `src/dressing_planner_supervisor.ipynb` | Supervisor variant of the dressing planner |
| `src/dressing_planner_HIL.ipynb` | Adds a human-response worker for human-in-the-loop routing |
| `src/social_media_post_HIL.ipynb` | AI writer drafts posts; a human approves/edits/rejects via interrupt/resume points |

See [demos/demo-1/demo-1-resources.ipynb](demos/demo-1/demo-1-resources.ipynb) for reference links.

### Demo 2 — Advanced Scenarios & Game Theory (`demos/demo-2/`)

Teams, hierarchies, swarm and network topologies, plus game-theoretic scenarios.

| Notebook | Topic |
|---|---|
| `src/dressing_planner_team.ipynb` | Supervisor coordinating a team of dressing-planner agents |
| `src/dressing_planner_weather_reporter.ipynb` | Team of weather reporter, dressing planner, and image generator |
| `src/hierarchical_architecture.ipynb` | Network, supervisor, and hierarchical (supervisor-of-supervisors) architectures |
| `src/flight_support_swarm_architecture.ipynb` | Swarm — Viktor (flight) and Walter (luggage) agents hand off to each other |
| `src/train_braking_network_architecture.ipynb` | Network topology (many-to-many agent connections) |
| `src/prisoners_dilemma.ipynb` | Two agents choose cooperate/defect; dominant strategy and Nash equilibrium |
| `src/weather_flood_vs_hurricane_game.ipynb` | Auction game theory — bidders compete for flood/hurricane reporting tasks |
| `src/weather_flood_vs_hurricane_game_human_review.ipynb` | Auction variant with a human-review interrupt on the final report |

See [demos/demo-2/demo-2-resources.ipynb](demos/demo-2/demo-2-resources.ipynb) for reference links.

## Setup

The demos load environment variables from a `.env` file in the notebook's working directory (`demos/demo-1/src/` or `demos/demo-2/src/`). Create one with your keys:

```
OPENAI_API_KEY="..."
OPENAI_MODEL="gpt-4o-mini"
LANGSMITH_TRACING="true"
LANGSMITH_API_KEY="..."
OPENWEATHER_API_KEY="..."
```

Each notebook installs its own packages via a `%pip install` cell (LangGraph plus `langgraph-supervisor` or `langgraph-swarm` as needed), so no separate `requirements.txt` is required.

## Requirements

- `OPENAI_API_KEY` and `OPENAI_MODEL` — required for all LLM calls
- `LANGSMITH_API_KEY` / `LANGSMITH_TRACING` — optional, enables LangSmith tracing
- `OPENWEATHER_API_KEY` — required only for the weather-reporting demos

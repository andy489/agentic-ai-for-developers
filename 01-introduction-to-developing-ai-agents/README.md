# 01 — Introduction to Developing AI Agents

An introduction to AI agent concepts and hands-on projects built with [CrewAI](https://docs.crewai.com/).

## Notebooks

- [01 — Introduction to Developing AI Agents](01-introduction-to-developing-AI-agents.ipynb) — PEAS framework, agent types, LangGraph demos
- [02 — Customer Feedback Analysis with CrewAI](02-customer-feedback-analysis-with-crewai.ipynb) — CrewAI walkthrough

## Projects

### feedback-analysis-crew

A two-agent CrewAI crew that analyzes customer feedback for an online shop.

| Agent | Role |
|---|---|
| `sentiment_analyst` | Classifies feedback as positive / negative / neutral with a percentage breakdown |
| `theme_analyst` | Identifies the top 5 recurring themes (e.g. Shipping Speed, Product Quality) |

Agents run sequentially — the theme analyst receives sentiment results as context.

```bash
cd feedback-analysis-crew
cp .env.example .env   # set OPENAI_API_KEY
poetry install
poetry run feedback-analysis-crew
```

### returns-refunds-flow

A three-step CrewAI Flow that routes customer return requests through approval or rejection.

```
validate → route_decision ─┬─ approved → RefundCrew   (return instructions)
                            └─ rejected → DenialCrew   (empathetic denial)
```

| Crew | Agent | Role |
|---|---|---|
| `ValidationCrew` | `return_validator` | Checks eligibility against shop policy |
| `RefundCrew` | `refund_processor` | Generates step-by-step return instructions |
| `DenialCrew` | `denial_agent` | Writes an empathetic denial with alternative offers |

```bash
cd returns-refunds-flow
cp .env.example .env   # set OPENAI_API_KEY
poetry install
poetry run returns-refunds-flow
```

## Requirements

- Python 3.10–3.13
- [Poetry](https://python-poetry.org/)
- `OPENAI_API_KEY` set in `.env` inside each project

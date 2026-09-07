# Agentic AI for Developers

Hands-on course material for building AI agents with [CrewAI](https://docs.crewai.com/).

## Structure

```
introduction-to-developing-ai-agents/
├── 01-introduction-to-developing-AI-agents.ipynb   # Core concepts & agent types
├── 02-customer-feedback-analysis-with-crewai.ipynb # CrewAI walkthrough notebook
├── assets/                                          # Diagrams used in notebooks
├── feedback-analysis-crew/                          # CrewAI crew project
└── returns-refunds-flow/                            # CrewAI Flow project
```

## Projects

### feedback-analysis-crew

A two-agent CrewAI crew that analyzes customer feedback for an online shop.

| Agent | Role |
|---|---|
| `sentiment_analyst` | Classifies feedback as positive / negative / neutral and produces a percentage breakdown |
| `theme_analyst` | Identifies the top 5 recurring themes (e.g. Shipping Speed, Product Quality) |

The agents run sequentially — the theme analyst receives the sentiment results as context before producing its report.

**Run:**
```bash
cd introduction-to-developing-ai-agents/feedback-analysis-crew
poetry install
poetry run feedback-analysis-crew
```

### returns-refunds-flow

A three-step CrewAI Flow that processes customer return requests using a router to branch between approval and rejection paths.

```
validate → route_decision ─┬─ approved → RefundCrew   (return instructions)
                            └─ rejected → DenialCrew   (empathetic denial)
```

| Crew | Agents |
|---|---|
| `ValidationCrew` | `return_validator` — checks eligibility against shop policy |
| `RefundCrew` | `refund_processor` — generates step-by-step return instructions |
| `DenialCrew` | `denial_agent` — writes an empathetic denial with alternative offers |

**Run:**
```bash
cd introduction-to-developing-ai-agents/returns-refunds-flow
poetry install
poetry run returns-refunds-flow
```

## Requirements

- Python 3.10 – 3.13
- [Poetry](https://python-poetry.org/)
- An `OPENAI_API_KEY` (or compatible LLM key) — copy `.env.example` to `.env` inside each project and fill in your key

## Setup

```bash
# clone
git clone https://github.com/andy489/Agentic-AI-for-Developers.git
cd Agentic-AI-for-Developers

# install deps for a project
cd introduction-to-developing-ai-agents/feedback-analysis-crew
cp .env.example .env   # add your API key
poetry install
```

# Agentic AI for Developers

Hands-on course material for building AI agents with [CrewAI](https://docs.crewai.com/) and [Spring AI](https://docs.spring.io/spring-ai/reference/).

## Structure

```
01-introduction-to-developing-ai-agents/
├── 01-introduction-to-developing-AI-agents.ipynb   # Core concepts & agent types
├── 02-customer-feedback-analysis-with-crewai.ipynb # CrewAI walkthrough notebook
├── assets/                                          # Diagrams used in notebooks
├── feedback-analysis-crew/                          # CrewAI crew project
└── returns-refunds-flow/                            # CrewAI Flow project

02-frameworks-for-developing-llm-agents/
└── spring-ai-chaperone/                             # Spring Boot + Spring AI chat app
```

## Notebooks

### Introduction to Developing AI Agents

- [01 — Introduction to Developing AI Agents](01-introduction-to-developing-ai-agents/01-introduction-to-developing-AI-agents.ipynb)
- [02 — Customer Feedback Analysis with CrewAI](01-introduction-to-developing-ai-agents/02-customer-feedback-analysis-with-crewai.ipynb)

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
cd 01-introduction-to-developing-ai-agents/feedback-analysis-crew
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
cd 01-introduction-to-developing-ai-agents/returns-refunds-flow
poetry install
poetry run returns-refunds-flow
```

### spring-ai-chaperone

A Spring Boot + Spring AI web app that acts as an AI chaperone for high school students on a field trip to San Francisco. Students chat with the AI to get activity suggestions tailored to their schedule, weather, school policies, and personal preferences.

**Key features:**
- RAG over trip itinerary, school policies, and activity brochure (loaded at startup)
- Per-student conversation memory keyed by name
- Live weather lookup via the NWS API (`@Tool`)
- Student feedback written back into the vector store to improve future suggestions (`@Tool`)
- Vanilla HTML/JS chat UI served at `http://localhost:8080`

| Endpoint | Description |
|---|---|
| `POST /chat` | Send a message: `{"studentName": "Alice", "message": "..."}` |
| `GET /activities` | All activity suggestions made during the session |

**Run:**
```bash
cd 02-frameworks-for-developing-llm-agents/spring-ai-chaperone
cp .env.example .env   # add OPENAI_API_KEY
./gradlew bootRun
```

## Requirements

| Module | Runtime | Key |
|---|---|---|
| `01-introduction-to-developing-ai-agents` | Python 3.10–3.13 + [Poetry](https://python-poetry.org/) | `OPENAI_API_KEY` in `.env` |
| `02-frameworks-for-developing-llm-agents/spring-ai-chaperone` | Java 25 + Gradle wrapper | `OPENAI_API_KEY` in `.env` |

## Setup

```bash
# clone
git clone https://github.com/andy489/Agentic-AI-for-Developers.git
cd Agentic-AI-for-Developers

# Python projects
cd 01-introduction-to-developing-ai-agents/feedback-analysis-crew
cp .env.example .env   # add your API key
poetry install

# Spring AI project
cd 02-frameworks-for-developing-llm-agents/spring-ai-chaperone
cp .env.example .env   # add your API key
./gradlew bootRun
```

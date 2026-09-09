# Agentic AI for Developers

Hands-on course material for building AI agents with [CrewAI](https://docs.crewai.com/) and [Spring AI](https://docs.spring.io/spring-ai/reference/).

## Structure

```
01-introduction-to-developing-ai-agents/
├── 01-introduction-to-developing-AI-agents.ipynb   # Core concepts & agent types
├── 02-customer-feedback-analysis-with-crewai.ipynb # CrewAI walkthrough
├── assets/                                          # Diagrams used in notebooks
├── feedback-analysis-crew/                          # CrewAI crew project
└── returns-refunds-flow/                            # CrewAI Flow project

02-frameworks-for-developing-llm-agents/
├── frameworks-for-developing-llm-agents.ipynb       # LLM frameworks overview
└── spring-ai-chaperone/                             # Spring Boot + Spring AI chat app
```

---

## 01 — Introduction to Developing AI Agents

### Notebooks

- [01 — Introduction to Developing AI Agents](01-introduction-to-developing-ai-agents/01-introduction-to-developing-AI-agents.ipynb)
- [02 — Customer Feedback Analysis with CrewAI](01-introduction-to-developing-ai-agents/02-customer-feedback-analysis-with-crewai.ipynb)

### feedback-analysis-crew

A two-agent CrewAI crew that analyzes customer feedback for an online shop.

| Agent | Role |
|---|---|
| `sentiment_analyst` | Classifies feedback as positive / negative / neutral with a percentage breakdown |
| `theme_analyst` | Identifies the top 5 recurring themes (e.g. Shipping Speed, Product Quality) |

Agents run sequentially — the theme analyst receives sentiment results as context.

```bash
cd 01-introduction-to-developing-ai-agents/feedback-analysis-crew
cp .env.example .env && poetry install && poetry run feedback-analysis-crew
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
cd 01-introduction-to-developing-ai-agents/returns-refunds-flow
cp .env.example .env && poetry install && poetry run returns-refunds-flow
```

---

## 02 — Frameworks for Developing LLM Agents

### Notebooks

- [Frameworks for Developing LLM Agents](02-frameworks-for-developing-llm-agents/frameworks-for-developing-llm-agents.ipynb)

### spring-ai-chaperone

A Spring Boot + Spring AI web app acting as an AI chaperone for high school students on a field trip to San Francisco. Students chat with the AI to get activity suggestions tailored to their schedule, weather, school policies, and personal preferences.

**Key features:**
- RAG over trip itinerary, school policies, and activity brochure (chunked and loaded at startup)
- Per-student conversation memory keyed by name → UUID chat ID
- Live weather lookup via the NWS API (`@Tool`)
- Student feedback written back into the vector store to improve future suggestions (`@Tool`)
- Vanilla HTML/JS chat UI at `http://localhost:8080` with info modal explaining usage

| Endpoint | Description |
|---|---|
| `POST /chat` | Send a message: `{"studentName": "Alice", "message": "..."}` |
| `GET /activities` | All activity suggestions made during the session |

```bash
cd 02-frameworks-for-developing-llm-agents/spring-ai-chaperone
cp .env.example .env && ./gradlew bootRun
```

---

## Requirements

| Module | Runtime | API key |
|---|---|---|
| `01-introduction-to-developing-ai-agents` | Python 3.10–3.13 + [Poetry](https://python-poetry.org/) | `OPENAI_API_KEY` in `.env` |
| `02-frameworks-for-developing-llm-agents/spring-ai-chaperone` | Java 25 + Gradle wrapper | `OPENAI_API_KEY` in `.env` |

## Setup

```bash
git clone https://github.com/andy489/Agentic-AI-for-Developers.git
cd Agentic-AI-for-Developers

# Python projects — example with feedback-analysis-crew
cd 01-introduction-to-developing-ai-agents/feedback-analysis-crew
cp .env.example .env   # set OPENAI_API_KEY
poetry install

# Spring AI project
cd 02-frameworks-for-developing-llm-agents/spring-ai-chaperone
cp .env.example .env   # set OPENAI_API_KEY
./gradlew bootRun
```

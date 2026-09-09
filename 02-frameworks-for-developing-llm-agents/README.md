# 02 — Frameworks for Developing LLM Agents

An overview of frameworks for building LLM-powered agents, with a hands-on project using [Spring AI](https://docs.spring.io/spring-ai/reference/).

## Notebooks

- [Frameworks for Developing LLM Agents](frameworks-for-developing-llm-agents.ipynb)

## Projects

### [spring-ai-chaperone](spring-ai-chaperone)

A Spring Boot + Spring AI web app acting as an AI chaperone for high school students on a field trip to San Francisco. Students chat with the AI to get activity suggestions tailored to their schedule, weather, school policies, and personal preferences.

**Key features:**
- RAG over trip itinerary, school policies, and activity brochure (chunked and loaded at startup)
- Per-student conversation memory keyed by name → UUID chat ID
- Live weather lookup via the NWS API (`@Tool`)
- Student feedback written back into the vector store to improve future suggestions (`@Tool`)
- Vanilla HTML/JS chat UI at `http://localhost:8080`

| Endpoint | Description |
|---|---|
| `POST /chat` | Send a message: `{"studentName": "Alice", "message": "..."}` |
| `GET /activities` | All activity suggestions made during the session |

```bash
cd spring-ai-chaperone
cp .env.example .env   # set OPENAI_API_KEY
./gradlew bootRun
```

## Requirements

- Java 25
- Gradle wrapper (included)
- `OPENAI_API_KEY` set in `.env` inside each project

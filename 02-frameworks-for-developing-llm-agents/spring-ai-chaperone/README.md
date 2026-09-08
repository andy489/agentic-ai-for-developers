# Spring AI Chaperone

A Spring Boot + Spring AI application that acts as an intelligent chaperone for high school students on a field trip to San Francisco. Students interact with the AI via a web chat UI to get activity suggestions tailored to their schedule, weather conditions, school policies, and personal preferences.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│             SpringAiChaperoneApplication            │
│  - Loads RAG docs into VectorStore on startup       │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│                    Chaperone                        │
│  ChatClient with:                                   │
│  - MessageChatMemoryAdvisor (per-student history)   │
│  - QuestionAnswerAdvisor   (RAG over docs)          │
│  - Tools: getWeatherForecast, saveStudentFeedback   │
│  - POST /chat endpoint                              │
│  - GET  /activities endpoint                        │
└──────────┬──────────────────────┬───────────────────┘
           │                      │
           ▼                      ▼
┌──────────────────┐   ┌─────────────────────────────┐
│   WeatherTools   │   │        FeedbackTools        │
│  Calls NWS API   │   │  Writes feedback as new RAG │
│  (SF grid point) │   │  documents into VectorStore │
└──────────────────┘   └─────────────────────────────┘
```

**RAG documents** (`src/main/resources/rag/`):
- `trip-itinerary.txt` — day-by-day schedule
- `school-policies.txt` — rules and restrictions
- `activity-brochure.txt` — pre-approved activities

All three are chunked at startup and stored in an in-memory `SimpleVectorStore`. Student feedback is also written back into the same store, influencing future suggestions.

**Conversation memory** is per-student, keyed by name → UUID chat ID, using `MessageWindowChatMemory`. Both the vector store and chat memory reset on restart.

## Prerequisites

- Java 25 (SapMachine or any OpenJDK 25 distribution)
- Gradle (only needed once to regenerate the wrapper jar — see below)
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Setup

1. **Regenerate the Gradle wrapper** (first time only, requires Gradle installed globally):
   ```bash
   gradle wrapper
   ```

2. **Configure your API key** — copy `.env.example` to `.env` and fill in your key:
   ```bash
   cp .env.example .env
   # edit .env and set OPENAI_API_KEY=sk-...
   ```

## Running

```bash
./gradlew bootRun
```

Once started, open **http://localhost:8080** in your browser. Enter your name and start chatting with the AI chaperone. Use the **Switch Student** button to hand off to another student — each student's conversation history is kept separate.

## REST API

While the app is running, two endpoints are available:

| Method | Path | Description |
|---|---|---|
| `POST` | `/chat` | Send a message. Body: `{"studentName": "Alice", "message": "What can I do?"}` |
| `GET` | `/activities` | Returns all activity suggestions made during the session as JSON |

## Building & Testing

```bash
# Build
./gradlew build

# Run tests
./gradlew test

# Run a single test
./gradlew test --tests "io.jzheaux.pluralsight.spring.spring_ai_chaperone.SpringAiChaperoneApplicationTests"
```

## Key Dependencies

| Dependency | Version | Purpose |
|---|---|---|
| Spring Boot | 4.1.1 | Application framework |
| Spring AI | 2.0.1 | LLM / embedding / vector store abstractions |
| spring-ai-starter-model-openai | (via BOM) | OpenAI model + embeddings |
| springboot4-dotenv | 5.1.0 | Load `.env` into Spring environment |
| Java toolchain | 25 | Runtime and compiled bytecode |
| Gradle wrapper | 9.7.1 | Build tool |

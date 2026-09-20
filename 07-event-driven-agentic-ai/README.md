# Module 07 — Event-Driven Agentic AI

Hands-on material covering the theory and practice of building AI agents that are triggered by events, react asynchronously, and emit events as output.

## Structure

```
07-event-driven-agentic-ai/
├── 07-event-driven-agentic-ai.ipynb   # Full lecture notes
└── assets/                            # Diagrams referenced by the notebook
```

## Learning Path

| Part | What you'll learn |
|---|---|
| Part 1 — Foundations | Event-driven architecture terminology, event sources (webhooks, queues, streams, IoT/MQTT, CDC), agentic use cases |
| Part 2 — Architectural Patterns | Event buses, pub/sub topologies, Kafka vs. NATS, topic design, sagas, outbox pattern, pitfalls (event storms, hot partitions, duplicate delivery), backpressure tuning |
| Part 3 — Frameworks and Tooling | Kafka / Azure Event Hubs, NATS / JetStream, Azure Durable Functions, Temporal, Semantic Kernel, LangChain, Azure Event Grid / AWS EventBridge |
| Part 4 — Real-Time Agent Workflows | Event-native agent design, guard clauses, inter-agent protocols (topics, roles, message formats), human-in-the-loop with SLA timers |
| Part 5 — Robustness | Failure taxonomy, retries with exponential backoff and jitter, dead-letter queues, idempotency keys, semantic idempotency, state machines |
| Part 6 — Observability, Monitoring, and Security | Distributed tracing (correlation IDs), metrics, structured logging, authentication vs. authorization, managed identity, PII redaction, content filters, approval gates |

## Key Concepts

- **Event-driven architecture** — loose coupling, asynchrony, scalability, and resilience through events
- **Event vs. Command vs. Fact** — naming and routing conventions for different message types
- **Kafka / Event Hubs** — durable, replayable, high-throughput streams; partition-key design
- **NATS** — sub-millisecond pub/sub for fast coordination and IoT
- **Sagas** — choreography vs. orchestration for long-running workflows; compensating transactions
- **Outbox pattern** — atomic database write + event publication without distributed transactions
- **Idempotency** — effect logs, idempotency keys, and semantic idempotency for safe retries
- **Event-native agents** — trigger → guards → tool selection → memory attachment → action → event output
- **Human-in-the-loop** — SLA-driven approval gates; escalation on timeout
- **Observability** — root span + child spans, correlation IDs, structured log fields

## Prerequisites

A working Python environment and an `OPENAI_API_KEY`. Copy `.env.example` to `.env` and fill in your key if a `.env.example` is present in the project root.

## Further Reading

- [Enterprise Integration Patterns](https://www.enterpriseintegrationpatterns.com/) — Hohpe & Woolf
- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [NATS Documentation](https://docs.nats.io/)
- [Azure Event Hubs Documentation](https://learn.microsoft.com/azure/event-hubs/)
- [Azure Service Bus Documentation](https://learn.microsoft.com/azure/service-bus-messaging/)
- [Temporal Documentation](https://docs.temporal.io/)
- [Semantic Kernel Documentation](https://learn.microsoft.com/semantic-kernel/)

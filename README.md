# Agentic AI for Developers

Hands-on course material for building AI agents.

## Modules

| Module | Topics | Stack |
|---|---|---|
| [01 — Introduction to Developing AI Agents](01-introduction-to-developing-ai-agents) | Agent concepts, PEAS framework, LangGraph, CrewAI | Python · CrewAI |
| [02 — Frameworks for Developing LLM Agents](02-frameworks-for-developing-llm-agents) | LLM frameworks overview, RAG, tools, memory | Java · Spring AI |
| [03 — Domain-Specific LLM Agents](03-domain-specific-llm-agents) | Fine-tuning, LoRA, data preparation, feedback loops | Python · Hugging Face · PEFT |
| [04 — Evaluating and Optimizing LLM Agents](04-evaluating-and-optimizing-llm-agents) | Agent quality metrics, DeepEval, LLM-as-a-Judge (G-Eval), Open-RAG-Eval, LangSmith observability | Python · LangChain · DeepEval · LangSmith |
| [05 — Developing Multi-agent Systems](05-developing-multi-agent-systems) | Multi-agent topologies (network, supervisor, hierarchical, swarm), human-in-the-loop, negotiation, game theory | Python · LangGraph · LangSmith |
| [06 — Memory-Augmented Persistent Agents](06-memory-augmented-persistent-agents) | Memory types (episodic/semantic/procedural), short-term buffers, long-term vector stores, summarization/pruning/caching, multi-agent memory sharing | Python · LangChain · LangGraph · ChromaDB · LangSmith |
| [07 — Event-Driven Agentic AI](07-event-driven-agentic-ai) | Event-driven architecture, Kafka/NATS/Event Hubs, sagas, outbox pattern, idempotency, event-native agent design, human-in-the-loop, observability, security | Python · Kafka · NATS · Azure Event Hubs · Semantic Kernel · LangChain |
| [08 — Agentic Knowledge Graphs](08-agentic-knowledge-graphs) | Knowledge graph foundations, entities/relationships/ontologies/schemas, graph traversal, LPG vs. RDF, Cypher/SPARQL, LLM+graph integration, hybrid retrieval, production pipelines, governance | Python · Neo4j · RDF · TypeDB · LangChain |
| [09 — ChatGPT AI Agents Lab](09-chat-gpt-ai-agents-lab) | RTCF prompting, tool schemas, local tool execution (calculator, KB lookup), multi-turn agent loop with Chat Completions API | Python · OpenAI |

## Quick Start

Each module has its own README with setup instructions. All projects require an `OPENAI_API_KEY` — copy `.env.example` to `.env` inside the project and fill in your key.

```bash
git clone https://github.com/andy489/Agentic-AI-for-Developers.git
cd Agentic-AI-for-Developers
```

Then follow the README in the module you want to run.

# Module 06 — Memory-Augmented Persistent Agents

Hands-on material covering why memory matters for agentic AI, how to compare persistent-memory frameworks, and how to build a full multi-agent engineering team with hybrid short-term and long-term memory.

## Structure

```
06-memory-augmented-persistent-agents/
├── 01-memory-concepts-and-demo/          # Core concepts + runnable demo notebook
├── 02-framework-comparisons/             # Four framework walkthroughs (notebooks)
│   ├── 1-kernel/                         # Semantic Kernel — thread-based memory
│   ├── 2-haystack/                       # Haystack + Mem0 — RAG + managed memory
│   ├── 3-memGPT/                         # MemGPT / Letta — structured memory blocks
│   └── 4-llamaIndex/                     # LlamaIndex — multi-agent team with RAG
├── 03-multi-agent-engineering-team/      # Full project: LangChain + LangGraph + ChromaDB
│   ├── start/                            # Exercise skeleton (stub functions to implement)
│   └── end/                              # Reference implementation
├── assets/                               # Diagrams referenced by the notes notebook
└── memory-augmented-persistent-agents-notes.ipynb   # Full lecture notes
```

## Learning Path

| Folder | What you'll do |
|---|---|
| `01-memory-concepts-and-demo` | Understand stateless vs stateful agents; build episodic/semantic/procedural memory; wire up ChromaDB retrieval and LangGraph thread persistence |
| `02-framework-comparisons` | Run side-by-side demos of Semantic Kernel, Haystack+Mem0, MemGPT/Letta, and LlamaIndex memory approaches |
| `03-multi-agent-engineering-team` | Implement a developer → reviewer → lead approval pipeline with hybrid memory, summarization, pruning, caching, and LangSmith tracing |

## Key Concepts

- **Stateless vs memory-augmented agents** — why every LLM call starts from zero and how to fix it
- **Memory types** — episodic (vector DB), semantic (RAG), procedural (system prompts)
- **Short-term memory** — `ConversationBufferWindowMemory` sliding window + LangGraph `thread_id` checkpointing
- **Long-term memory** — ChromaDB persistent vector store; swap-in path for Pinecone, pgvector, Redis
- **Optimization** — rolling summarization (~70% token savings), pruning (~40%), prompt caching (~50%), selective retrieval
- **Multi-agent memory sharing** — all agents read/write the same vector store; task results persisted across sessions

## Workflow Architecture (03-multi-agent-engineering-team)

```
User Task
    ↓
Developer Agent  ──── retrieve_context_tool (RAG)
    ↓                  retrieve_memory_tool (ChromaDB)
Reviewer Agent         store_memory_tool
    ↓
Lead Approval
    ↓
Decision Router
    ├── approved → Summarizer → Short-term maintenance → Long-term maintenance → END
    └── rejected → Developer (revision loop)
```

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key
- (Optional) LangSmith API key for tracing

### Install

```bash
# macOS
python3 -m venv .venv && source .venv/bin/activate
pip3 install -r 03-multi-agent-engineering-team/end/requirements.txt

# Windows
python -m venv .venv && .venv\Scripts\activate
pip install -r 03-multi-agent-engineering-team/end/requirements.txt
```

### Environment variables

Create a `.env` file in the project you want to run:

```
OPENAI_API_KEY=sk-...
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=ls__...
LANGSMITH_PROJECT=memory-agents-demo
```

### Run

```bash
# Jupyter notebooks (modules 01 and 02)
jupyter notebook

# Multi-agent CLI demo (03-multi-agent-engineering-team)
cd 03-multi-agent-engineering-team/end
python3 main.py

# Tests
cd 03-multi-agent-engineering-team/end
python3 test.py
```

## Production Vector Database Options

ChromaDB is used for development. Swap via the same `VectorStore` interface:

| DB | Strengths |
|---|---|
| **Redis** | Ultra-low latency, session caching |
| **Pinecone** | Fully managed, auto-scaling |
| **Weaviate** | Hybrid vector + keyword search |
| **PostgreSQL (pgvector)** | SQL + vector in one DB |
| **Elasticsearch** | Full-text + vector hybrid |

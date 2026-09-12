# 04 — Evaluating and Optimizing LLM Agents

Measuring agent quality, building custom metrics, and observing RAG pipelines in production using DeepEval, G-Eval, Open-RAG-Eval, and LangSmith.

## Notebook

- [evaluating-and-optimizing-llm-agents.ipynb](evaluating-and-optimizing-llm-agents.ipynb) — End-to-end walkthrough across two parts:

| Part | Topic |
|---|---|
| Part 1 — Measuring Agent Quality | DeepEval live scoring, LLM-as-a-Judge (G-Eval), custom metrics, multi-judge averaging |
| Part 2 — From Custom Metrics to Production | Open-RAG-Eval, LangSmith tracing, cost/latency visualisation |

## Example App

### example-app-langchain-rag

A LangChain + Streamlit RAG application used throughout the module as the evaluation target.

```bash
cd example-app-langchain-rag
/opt/homebrew/bin/python3.12 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your keys:

```
OPENAI_API_KEY="..."
HUGGINGFACEHUB_API_TOKEN="..."
LANGCHAIN_API_KEY="..."
LANGCHAIN_TRACING_V2="true"
```

Then run the Streamlit app:

```bash
streamlit run streamlit_app.py
```

See [example-app-langchain-rag/README.md](example-app-langchain-rag/README.md) for full setup, evaluation pipeline, and example queries.

## Requirements

- Python 3.12 (3.14+ not supported due to pinned dependencies)
- `OPENAI_API_KEY` required for LLM calls and G-Eval judging
- `LANGCHAIN_API_KEY` (LangSmith) required for tracing demos
- `HUGGINGFACEHUB_API_TOKEN` required for HuggingFace model access

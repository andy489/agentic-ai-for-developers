# Module 09 — ChatGPT AI Agents Lab

Hands-on lab building a tool-calling agent with the OpenAI Chat Completions API — RTCF prompting, local tool execution, and a multi-turn agentic loop.

## Structure

```
09-chat-gpt-ai-agents-lab/
└── chat-gpt-ai-agents-lab.ipynb   # Full lab notebook
```

## What you'll build

A single-file agent that:

1. Receives a natural-language task
2. Decides whether to call tools (calculator, knowledge-base lookup) or answer directly
3. Executes the tool locally and feeds results back to the model
4. Returns a structured response following the RTCF format

## Key Concepts

- **RTCF system prompt** — Role, Task, Context, Format; a structured prompt pattern that keeps agent responses consistent
- **Tool schemas** — JSON function definitions passed to the model so it can request calculator or KB-lookup calls
- **Agent loop** — plan → act (tool call) → observe (tool result) → synthesise final answer
- **Tool calling** — the model emits a `tool_calls` payload; the host application executes the function and appends a `tool` message before the next completion

## Setup

1. Copy the root `.env.example` to `.env` in the repo root and fill in `OPENAI_API_KEY`:

```bash
cp ../.env.example ../.env
# then edit ../.env and set OPENAI_API_KEY=sk-...
```

2. Install dependencies (JupyterLab + openai + python-dotenv):

```bash
pip install openai python-dotenv
```

3. Open the notebook:

```bash
jupyter lab chat-gpt-ai-agents-lab.ipynb
```

4. Run all cells top-to-bottom. The final cell runs four test tasks through the agent loop and prints structured responses.

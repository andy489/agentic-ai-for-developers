# 03 — Domain-Specific LLM Agents

Building, fine-tuning, and deploying LLMs for specialised domains using Hugging Face, PEFT, and LoRA.

## Notebook

- [domain-specific-llm-agents.ipynb](domain-specific-llm-agents.ipynb) — End-to-end walkthrough: comparison, data prep, fine-tuning, and feedback loop

## Project

### domain-specific-llm-agents

A four-section Python project covering the full domain-specific LLM lifecycle.

| Section | Topic |
|---|---|
| `section1` | Compare a telecom-domain model (`TSLAM-4B`) against `Llama-2-7b-chat-hf` |
| `section2` | Clean and annotate a DCGM GPU metrics CSV for training |
| `section3` | LoRA fine-tune `Mistral-7B-Instruct-v0.3` on a fitness & nutrition dataset |
| `section4` | Privacy-preserving feedback loop — anonymise PII, build dataset, update model |

```bash
cd domain-specific-llm-agents
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install torch transformers peft trl datasets accelerate bitsandbytes pandas numpy
```

See [domain-specific-llm-agents/README.md](domain-specific-llm-agents/README.md) for full setup and per-section instructions.

## Requirements

- Python 3.8+
- CUDA-compatible GPU recommended (sections 3 and 4)
- `OPENAI_API_KEY` or Hugging Face token as needed — copy `domain-specific-llm-agents/env.example` to `.env`

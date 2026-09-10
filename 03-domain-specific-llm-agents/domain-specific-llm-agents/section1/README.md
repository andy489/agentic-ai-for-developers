# Section 1 — General-purpose vs Domain-specific LLM Comparison

Demonstrates the practical difference between a general-purpose LLM and a domain-specific LLM through two interactive CLI scripts.

## Scripts

| File | Model | Domain |
|------|-------|--------|
| `domain-specific-llm.py` | `NetoAISolutions/TSLAM-4B` | Telecommunications |
| `general-purpose-llm.py` | `meta-llama/Llama-2-7b-chat-hf` | General purpose |

Both scripts start an interactive prompt loop. Type `quit` or `exit` to stop.

## Setup

### 1. Install dependencies

```bash
pip install torch transformers
```

### 2. Hugging Face authentication

`Llama-2-7b-chat-hf` requires accepting Meta's licence on Hugging Face and logging in:

```bash
pip install huggingface_hub
huggingface-cli login
```

`TSLAM-4B` is publicly available — no token required.

### 3. Run

```bash
# Domain-specific (telecom)
python domain-specific-llm.py

# General-purpose
python general-purpose-llm.py
```

## Hardware requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| GPU VRAM | 8 GB | 16 GB |
| System RAM | 16 GB | 32 GB |
| Disk | 15 GB free | 30 GB free |

CPU-only execution is supported but slow (expect 30–120 s per response).

## Example prompts

**Telecom domain** (use with `domain-specific-llm.py`):
- `Explain 5G network architecture`
- `What is network slicing and how is it used in 5G?`
- `How does MIMO improve wireless throughput?`

**General purpose** (use with `general-purpose-llm.py`):
- `What is machine learning?`
- `Summarise the causes of the 2008 financial crisis`
- `Write a Python function to reverse a string`

## What to observe

The telecom model gives precise, jargon-correct answers to network questions.
The general-purpose model gives broader answers that may lack domain precision.
Run the same question in both scripts to see the contrast.

## Notes

- Models are downloaded on first run and cached in `~/.cache/huggingface/`
- Generation length is capped at 2 000 tokens (`domain-specific-llm.py`) and 300 tokens (`general-purpose-llm.py`) — adjust `max_length` / `max_new_tokens` as needed
- `general-purpose-llm.py` hardcodes `.to("cuda")` — change to `device` variable if running on CPU

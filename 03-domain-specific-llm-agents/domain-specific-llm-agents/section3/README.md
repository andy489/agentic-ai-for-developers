# Section 3 — Fine-tuning a Domain-specific LLM

Fine-tunes `mistralai/Mistral-7B-Instruct-v0.3` on a fitness & nutrition dataset using LoRA (Low-Rank Adaptation) via Hugging Face PEFT and TRL. Includes three test scripts for verifying the result.

## Scripts

| File | Purpose |
|------|---------|
| `fine-tune-mistral-7b.py` | Full LoRA fine-tuning run on the fitness dataset |
| `test-model.py` | Load the local fine-tuned checkpoint and run a single inference |
| `test-model2.py` | Load the base `Mistral-7B-Instruct-v0.3` from HF Hub and run inference |
| `test-model3.py` | Simulated comparison (no model download) — old vs new response side-by-side |

## Setup

### 1. Install dependencies

```bash
pip install torch transformers peft trl datasets accelerate bitsandbytes
```

### 2. Hugging Face authentication

Mistral-7B requires accepting the licence on Hugging Face:

```bash
huggingface-cli login
```

### 3. (Optional) GPU check

```bash
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

## Run fine-tuning

```bash
python fine-tune-mistral-7b.py
```

Training uses the public dataset `chibbss/fitness-chat-prompt-completion-dataset` (downloaded automatically).

Expected output location: `./mistral7b_fitness_llm_finetuned/`

## Run tests

```bash
# Test your fine-tuned model (requires completed fine-tuning)
python test-model.py

# Test the base Mistral model directly from HF Hub
python test-model2.py

# Simulated comparison — no GPU or model download needed
python test-model3.py
```

## Hardware requirements

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| GPU VRAM | 16 GB | 24–40 GB |
| System RAM | 32 GB | 64 GB |
| Disk | 50 GB free | 100 GB free |

> `bitsandbytes` enables 4-bit quantisation, reducing VRAM usage to ~4 GB for the 7B model. Install it and the script uses it automatically on CUDA.  
> CPU-only execution is technically possible but will take hours per epoch.

## LoRA configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| `r` | 8 | Adapter rank — increase for more capacity |
| `lora_alpha` | 16 | Scaling (alpha/r = 2) |
| `lora_dropout` | 0.05 | Regularisation |
| `target_modules` | `q_proj`, `v_proj` | Attention projections only |
| `task_type` | `CAUSAL_LM` | Causal language modelling |

## Training configuration

| Parameter | Value |
|-----------|-------|
| Epochs | 2 |
| Batch size | 1 per device |
| Gradient accumulation | — |
| Mixed precision | fp16 (GPU) / fp32 (CPU) |
| Max sequence length | 512 tokens |
| Optimizer | adamw_torch |
| Eval strategy | per epoch |

## Output

| Path | Contents |
|------|----------|
| `./mistral7b_fitness_llm_finetuned/` | Fine-tuned model + tokenizer |
| `./logs/` | Training logs (loss per step) |

## SuperAdapters (advanced)

`SuperAdapters/` is a third-party framework supporting broader model and adapter combinations. See `SuperAdapters/README.md` for its own setup and CLI usage. It is independent of the main fine-tuning script.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `CUDA out of memory` | Reduce `per_device_train_batch_size` to 1 and add `gradient_accumulation_steps=8` |
| `RuntimeError: weight_only_quantized` | Ensure `bitsandbytes>=0.50.2` is installed |
| `401 Unauthorized` from HF Hub | Run `huggingface-cli login` |
| `eval_strategy` key error | Ensure `transformers>=4.46.0` |

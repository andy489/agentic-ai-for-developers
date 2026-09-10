# Section 4 — Privacy-preserving Feedback Loop and Continuous Learning

Implements a continuous learning pipeline: collect user feedback, anonymise PII, store it, and use it to further fine-tune the model from Section 3 via LoRA updates.

## Scripts

| File | Purpose | Requires GPU? |
|------|---------|---------------|
| `preprocess-feedback.py` | Anonymise text and log feedback to `feedback_log.json` | No |
| `create-feedback-dataset.py` | Convert `feedback_log.json` into a Hugging Face `Dataset` | No |
| `fine-tune-model.py` | LoRA update of the Section 3 model on the feedback dataset | Yes |
| `test-model.py` | Simulated before/after comparison (no model load) | No |

## Setup

### 1. Install dependencies

```bash
pip install torch transformers peft datasets accelerate
```

### 2. (Optional) PII anonymisation

`preprocess-feedback.py` uses regex-based anonymisation (email, phone) out of the box — no extra install needed. For production-grade anonymisation with Presidio:

```bash
pip install presidio-analyzer presidio-anonymizer spacy
python -m spacy download en_core_web_lg
```

## Workflow

Run scripts in this order:

### Step 1 — Log feedback

```bash
python preprocess-feedback.py
```

Appends an anonymised entry to `feedback_log.json`:

```json
{
  "timestamp": "2026-09-10 12:00:00",
  "user_input": "What are the best workout routines for weight loss?",
  "model_response": "For weight loss, consider HIIT and strength training.",
  "feedback": "Good response, but could be more specific."
}
```

Edit `user_input`, `model_response`, and `feedback` at the bottom of the script to log your own entries.

### Step 2 — Build feedback dataset

```bash
python create-feedback-dataset.py
```

Reads `feedback_log.json` and saves a Hugging Face `Dataset` to `./dataset/feedback_dataset/`.

**Requires `feedback_log.json` to exist** (created in Step 1).

### Step 3 — Fine-tune on feedback

```bash
python fine-tune-model.py
```

Loads the model from `./models/mistral7b_fitness_llm_finetuned/` (output of Section 3), applies LoRA, trains on the feedback dataset, and saves to `./models/mistral7b_fitness_llm_updated/`.

**Requires:**
- Completed Section 3 fine-tuning (`./models/mistral7b_fitness_llm_finetuned/` must exist)
- `./dataset/feedback_dataset/` from Step 2

### Step 4 — Compare models (no GPU needed)

```bash
python test-model.py
```

Prints a hardcoded before/after comparison to illustrate the expected improvement. No model loading required.

## LoRA update configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| `r` | 16 | Higher rank than Section 3 for more update capacity |
| `lora_alpha` | 32 | Scaling factor |
| `target_modules` | `q_proj`, `v_proj` | Same attention projections |
| `learning_rate` | 5e-5 | Conservative for fine updates |
| `num_train_epochs` | 1 | Short update — not full retraining |
| `gradient_accumulation_steps` | 4 | Effective batch size = 4 |

## PII anonymisation

`preprocess-feedback.py` removes:
- Email addresses → `[EMAIL]`
- Phone numbers (10–15 digits) → `[PHONE]`

For broader PII coverage (names, addresses, IDs) use the Presidio-based approach shown in the notebook.

## File and directory structure

```
section4/
├── preprocess-feedback.py       # Run first — generates feedback_log.json
├── create-feedback-dataset.py   # Run second — generates dataset/
├── fine-tune-model.py           # Run third — updates the model
├── test-model.py                # Run any time — simulated comparison
├── requirements.txt
├── feedback_log.json            # Created at runtime (gitignored)
├── dataset/                     # Created at runtime
│   └── feedback_dataset/
└── models/                      # Must be populated from Section 3
    ├── mistral7b_fitness_llm_finetuned/   # Input model
    └── mistral7b_fitness_llm_updated/     # Output model
```

## Hardware requirements (fine-tune-model.py only)

| Resource | Minimum | Recommended |
|----------|---------|-------------|
| GPU VRAM | 16 GB | 24 GB |
| System RAM | 32 GB | 64 GB |
| Disk | 20 GB free | 50 GB free |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `FileNotFoundError: feedback_log.json` | Run `preprocess-feedback.py` first |
| `FileNotFoundError: feedback_dataset` | Run `create-feedback-dataset.py` first |
| `OSError: model not found` | Ensure Section 3 fine-tuning completed and model is at `./models/mistral7b_fitness_llm_finetuned/` |
| `remove_unused_columns` warning | Already set to `False` in training args — safe to ignore |

## Notes

- `feedback_log.json` is append-only — each run of `preprocess-feedback.py` adds a new entry.
- Accumulate at least 50–100 feedback pairs before running `fine-tune-model.py` for meaningful improvements.
- Always evaluate the updated model on a held-out benchmark before replacing the production checkpoint.

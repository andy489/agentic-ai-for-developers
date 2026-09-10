# Domain-Specific LLM Agents

Code and resources for the Pluralsight course "Domain-Specific LLM Agents". Covers building, fine-tuning, and deploying domain-specific LLMs from data preparation through continuous learning.

## Project Structure

```
├── section1/          # General vs domain-specific LLM comparison
├── section2/          # Data preparation and preprocessing
├── section3/          # Model fine-tuning with LoRA (Mistral-7B)
├── section4/          # Privacy-preserving feedback loop and model updates
├── requirements.txt
├── env.example
└── README.md
```

## Prerequisites

- Python 3.8+
- CUDA-compatible GPU (recommended for sections 3 and 4)
- 16 GB+ RAM
- 50 GB+ free disk space

## Installation

```bash
git clone <repository-url>
cd domain-specific-llm-agents
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Install dependencies per section (see each section's README), or install everything at once:

```bash
pip install torch transformers peft trl datasets accelerate bitsandbytes pandas numpy
```

## Quick Start

### Section 1 — LLM Comparison

Compare a telecom-domain model against a general-purpose LLM:

```bash
cd section1
python domain-specific-llm.py   # NetoAISolutions/TSLAM-4B (telecom)
python general-purpose-llm.py   # meta-llama/Llama-2-7b-chat-hf
```

### Section 2 — Data Preparation

Clean and annotate a DCGM GPU metrics CSV for training:

```bash
cd section2
python data-prep.py              # expects dcgm.csv, produces prepared_dcgm.csv
```

### Section 3 — Fine-tuning

LoRA fine-tune Mistral-7B on a fitness & nutrition dataset:

```bash
cd section3
python fine-tune-mistral-7b.py   # output: ./mistral7b_fitness_llm_finetuned/
python test-model.py             # test local fine-tuned checkpoint
python test-model3.py            # simulated before/after comparison (no GPU needed)
```

### Section 4 — Feedback Loop

Collect feedback, anonymise PII, and incrementally update the model:

```bash
cd section4
python preprocess-feedback.py       # step 1: log anonymised feedback
python create-feedback-dataset.py   # step 2: build HF Dataset
python fine-tune-model.py           # step 3: LoRA update (requires section3 output)
python test-model.py                # step 4: simulated comparison (no GPU needed)
```

## Environment Variables

Required for the database-backed variant in Section 3:

```bash
export LLM_DB_HOST='your_host'
export LLM_DB_PORT=3306
export LLM_DB_USERNAME='your_username'
export LLM_DB_PASSWORD='your_password'
export LLM_DB_NAME='your_database'
```

Copy `env.example` to `.env` and fill in your values.

## Model Requirements

- **Base model**: `mistralai/Mistral-7B-Instruct-v0.3`
- **Fine-tuning method**: LoRA via Hugging Face PEFT
- **Hardware**: CUDA GPU with 16 GB+ VRAM recommended; 4-bit quantisation via `bitsandbytes` reduces this to ~4 GB

## Course Information

Pluralsight course: [Domain-Specific LLM Agents](https://app.pluralsight.com/library/courses/domain-specific-llm-agents/table-of-contents)

## Acknowledgments

- [Hugging Face](https://huggingface.co/) for model hosting and PEFT/TRL libraries
- [Mistral AI](https://mistral.ai/) for the base model
- [SuperAdapters](https://github.com/AGI-Edgerunners/LLM-Adapters) for the advanced fine-tuning framework (section3/SuperAdapters)

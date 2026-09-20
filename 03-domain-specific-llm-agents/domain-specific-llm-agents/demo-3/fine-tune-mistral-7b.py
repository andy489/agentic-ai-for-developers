import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from datasets import load_dataset
# Use PEFT for adapter-based fine-tuning
from peft import LoraConfig, get_peft_model
from transformers import DataCollatorForLanguageModeling, TrainerCallback


# Ensure GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Step 1: Load dataset from Hugging Face
dataset_name = "chibbss/fitness-chat-prompt-completion-dataset"
dataset = load_dataset(dataset_name, split="train")

# Step 2: Load the pre-trained Mistral-7B model with trust_remote_code=True
model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if device.type == "cuda" else torch.float32,
    trust_remote_code=True
).to(device)

# Disable cache to help with hidden state shape
model.config.use_cache = False

# Step 3: Define LoRA Configuration for parameter-efficient fine-tuning using PEFT
lora_config = LoraConfig(
    r=8,               # Rank of the LoRA decomposition
    lora_alpha=16,
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Step 4: Apply LoRA adaptation using PEFT
model = get_peft_model(model, lora_config)

# Step 5: Tokenize dataset with proper prompt formatting
def tokenize_function(examples):
    texts = []
    # Process each example in the batch
    for instr, out in zip(examples["instruction"], examples["output"]):
        # Format the prompt as expected by Mistral
        text = f"~~[INST] {instr} [/INST] {out}~~"
        texts.append(text)
    # Tokenize the list of texts
    return tokenizer(texts, truncation=True, padding="max_length", max_length=512)

tokenized_datasets = dataset.map(tokenize_function, batched=True, remove_columns=["instruction", "output"])

# (Optional) Print a sample tokenized prompt for debugging
print("Sample tokenized prompt:")
print(tokenizer.decode(tokenized_datasets[0]["input_ids"]))

# Step 6: Define data collator for language modeling
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Step 7: Define Training Arguments
training_args = TrainingArguments(
    output_dir="./mistral7b_fitness_llm_finetuned",
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=1,
    per_device_eval_batch_size=1,
    num_train_epochs=2,
    weight_decay=0.01,
    save_total_limit=1,
    logging_dir="./logs",
    logging_steps=100,
    eval_steps=500,
    fp16=device.type == "cuda",
    optim="adamw_torch",
    report_to="none"
)

# Custom Callback for printing progress every 500 steps
class PrintProgressCallback(TrainerCallback):
    def on_step_end(self, args, state, control, **kwargs):
        if state.global_step % 500 == 0 and state.global_step > 0:
            print(f"🔥 Training step {state.global_step}/{state.max_steps} - Loss: {state.log_history[-1]['loss']:.4f}")

# Step 8: Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    eval_dataset=tokenized_datasets,
    tokenizer=tokenizer,
    data_collator=data_collator,
    callbacks=[PrintProgressCallback()]
)

# Step 9: Train Model
trainer.train()

# Step 10: Save Model
trainer.save_model("./mistral7b_fitness_llm_finetuned")
print("✅ Fine-tuning completed! Model saved to './mistral7b_fitness_llm_finetuned'")

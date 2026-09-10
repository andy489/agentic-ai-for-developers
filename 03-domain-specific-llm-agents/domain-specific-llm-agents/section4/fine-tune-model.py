import torch
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, TrainingArguments, DataCollatorForLanguageModeling
from datasets import load_from_disk

# Load the fine-tuned model and tokenizer
model_path = "./models/mistral7b_fitness_llm_finetuned"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, torch_dtype=torch.float16, device_map="auto")

# Load feedback dataset
dataset_path = "./dataset/feedback_dataset"
feedback_dataset = load_from_disk(dataset_path)

# Fix dataset column names to match model requirements
def preprocess_function(examples):
    """
    Tokenizes text data and maps it to model input format.
    """
    inputs = tokenizer(examples["input"], truncation=True, padding="max_length", max_length=512)
    outputs = tokenizer(examples["output"], truncation=True, padding="max_length", max_length=512)
    
    return {
        "input_ids": inputs["input_ids"],
        "attention_mask": inputs["attention_mask"],
        "labels": outputs["input_ids"],  # Model needs "labels" instead of "output"
    }

# Apply preprocessing to dataset
feedback_dataset = feedback_dataset.map(preprocess_function, batched=True, remove_columns=["input", "output"])

# Configure LoRA (Low-Rank Adaptation)
lora_config = LoraConfig(
    r=16, 
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

# Apply LoRA to model
peft_model = get_peft_model(model, lora_config)

# Define Training Arguments
training_args = TrainingArguments(
    output_dir="./models/mistral7b_fitness_llm_updated",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    save_steps=10,
    learning_rate=5e-5,
    num_train_epochs=1,
    logging_dir="./logs",
    remove_unused_columns=False  # Prevents dataset column mismatch error
)

# Trainer initialization
trainer = Trainer(
    model=peft_model,
    args=training_args,
    train_dataset=feedback_dataset,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)  # Required for causal LM training
)

# Fine-tune the model
if __name__ == "__main__":
    trainer.train()
    print("Fine-tuning complete! Model saved in './models/mistral7b_fitness_llm_updated'.")

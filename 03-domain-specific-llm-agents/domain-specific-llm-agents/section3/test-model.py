import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Define the local model path for your fine-tuned model
model_path = "./mistral7b_fitness_llm_finetuned"

# Load the tokenizer with trust_remote_code=True
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# Set padding token and padding side
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.bos_token
tokenizer.padding_side = "left"

# Load the model onto the appropriate device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    trust_remote_code=True
).to(device)

# Optionally update model configuration special tokens if necessary
if model.config.eos_token_id is None:
    model.config.eos_token_id = tokenizer.eos_token_id

# Define the prompt using the expected Mistral chat template
prompt = "<s>[INST] What are the benefits of weightlifting for muscle growth? [/INST]"

# Tokenize the input and move to device
inputs = tokenizer(prompt, return_tensors="pt", padding=True)
inputs = {k: v.to(device) for k, v in inputs.items()}

# Generate the response using greedy decoding (do_sample=False)
with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=1.0,  # Adjusted temperature (ignored with greedy decoding)
        top_p=0.9,
        do_sample=False,  # Greedy decoding for stability
        remove_invalid_values=True  # Ensures no inf/nan values in generation
    )

# Decode and print the response
response = tokenizer.decode(output[0], skip_special_tokens=True)
print("\nModel Response:\n", response)

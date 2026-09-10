import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# Define the model path
model_path = "mistralai/Mistral-7B-Instruct-v0.3"

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# Set padding token and padding side
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.bos_token
tokenizer.padding_side = "left"

# Load the model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    trust_remote_code=True
).to(device)

# Define the prompt
prompt = "[INST] What are the benefits of weightlifting for muscle growth? [/INST]"

# Tokenize the input
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Generate the response
with torch.no_grad():
    output = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=1.0,  # Adjusted temperature
        top_p=0.9,
        do_sample=False,  # Disable sampling
        remove_invalid_values=True  # Remove inf/nan values
    )

# Decode and print the response
response = tokenizer.decode(output[0], skip_special_tokens=True)
print("\nModel Response:\n", response)

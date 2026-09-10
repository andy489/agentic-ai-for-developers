# Step 1 - Import Necessary Libraries
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Step 2 - Check if GPU is available, otherwise use CPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Step 3 - Load the Tokenizer and Model
model_name = "NetoAISolutions/TSLAM-4B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name).to(device)

# Function to Generate Response from the Model
def generate_domain_response(prompt):
    """Generates a response from the domain-specific LLM."""
    # Construct the input with system and user prompts
    formatted_prompt = f"<|system|>\nYou are a helpful assistant.<|end|>\n<|user|>{prompt}<|end|>\n<|assistant|>\n"
    # Tokenize and move input to the appropriate device
    inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)
    # Generate a response with a maximum token length of 2000
    outputs = model.generate(**inputs, max_length=2000, num_return_sequences=1)
    # Decode and return the generated text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract the assistant's response by splitting at the assistant tag
    response = generated_text.split("<|assistant|>")[-1].strip()
    return response

# Step 4 - Start an Interactive Prompt Loop
print("\nDomain-Specific LLM (TSLAM-4B Fine-Tuned for Telecommunications)")
print("Type 'quit' or 'exit' to stop.")

while True:
    # Take user input from the command line
    user_input = input("\nEnter your prompt: ")
    if user_input.lower() in ["quit", "exit"]:
        print("Exiting...")
        break
    # Generate and print the LLM response
    response = generate_domain_response(user_input)
    print("\nDomain-Specific LLM Response:\n", response)

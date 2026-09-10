# Step 1 - Import Transformers
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Check if GPU is available, otherwise use CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

# Step 2 - Load a general-purpose model (Llama 2-7B)
model_name = "meta-llama/Llama-2-7b-chat-hf"

# Step 3 - Load the tokenizer for processing text inputs
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Step 4 - Load the LLM model, ensuring it runs efficiently on a GPU with float16 precision
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")

def generate_response(prompt):
    """Generates a response from the general-purpose LLM."""
    # Tokenize the user input and send it to the GPU
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    # Generate a response with a max token length of 300
    output = model.generate(**inputs, max_length=300)
    # Decode and return the generated text
    return tokenizer.decode(output[0], skip_special_tokens=True)

# Step 5 - Start an interactive prompt loop
print("\nGeneral-Purpose LLM (Llama 2-7B)")
print("Type 'quit' or 'exit' to stop.")

while True:
    # Take user input from the command line
    user_input = input("\nEnter your prompt: ")
    if user_input.lower() in ["quit", "exit"]:
        print("Exiting...")
        break
    # Generate and print the LLM response
    response = generate_response(user_input)
    print("\nLLM Response:\n", response)
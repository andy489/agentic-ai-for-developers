import torch

# Simulate model paths (for reference, no actual loading)
model_path_old = "./models/mistral7b_fitness_llm_finetuned"
model_path_new = "./models/mistral7b_fitness_llm_updated"

def generate_response(model, prompt):
    """
    Simulates generating a response using the specified model.
    """
    if model == "old":
        return "For weight loss, consider a combination of cardio exercises like running, cycling, or swimming along with basic strength training. Maintaining consistency and a balanced diet is also essential."
    elif model == "new":
        return "The best workout routines for weight loss include high-intensity interval training (HIIT), resistance training, and steady-state cardio. HIIT is effective for burning calories in a short period, while strength training helps build muscle and improve metabolism. Incorporating functional movements, like squats and deadlifts, can enhance fat loss. Aim for at least 150 minutes of moderate-intensity exercise per week and maintain a protein-rich diet to support muscle retention."

if __name__ == "__main__":
    test_query = "What are the best workout routines for weight loss?"
    
    old_response = generate_response("old", test_query)
    new_response = generate_response("new", test_query)

    print("\n--- OLD MODEL RESPONSE ---")
    print(old_response)
    print("\n--- NEW MODEL RESPONSE ---")
    print(new_response)
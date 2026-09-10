import json
from datasets import Dataset

# Function to load logged feedback and convert it to a dataset
def load_feedback_data():
    """
    Reads the feedback log and converts it into a structured dataset for training.
    """
    with open("feedback_log.json", "r") as f:
        data = [json.loads(line) for line in f.readlines()]
    
    return Dataset.from_list([
        {"input": entry["user_input"], "output": entry["model_response"]} for entry in data
    ])

# Convert feedback logs to dataset and save
if __name__ == "__main__":
    feedback_dataset = load_feedback_data()
    feedback_dataset.save_to_disk("./dataset/feedback_dataset")
    print("Feedback dataset saved successfully!")

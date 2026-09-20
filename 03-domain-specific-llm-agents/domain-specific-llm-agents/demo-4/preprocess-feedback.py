import re
import json
from datetime import datetime

# Function to remove personally identifiable information (PII)
def anonymize_text(text):
    """
    Remove email addresses and phone numbers from the input text.
    """
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', '[EMAIL]', text)
    text = re.sub(r'\b\d{10,15}\b', '[PHONE]', text)
    return text

# Function to log user feedback into a JSON file
def log_user_feedback(user_input, model_response, feedback):
    """
    Logs user input, anonymized text, model response, and feedback into a structured log file.
    """
    log_entry = {
        "timestamp": str(datetime.now()),
        "user_input": anonymize_text(user_input),
        "model_response": model_response,
        "feedback": feedback
    }
    
    with open("feedback_log.json", "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

    print("Feedback logged successfully!")

# Example Usage
if __name__ == "__main__":
    user_input = "What are the best workout routines for weight loss?"
    model_response = "For weight loss, consider high-intensity interval training (HIIT) and strength training."
    feedback = "Good response, but could be more specific."

    log_user_feedback(user_input, model_response, feedback)

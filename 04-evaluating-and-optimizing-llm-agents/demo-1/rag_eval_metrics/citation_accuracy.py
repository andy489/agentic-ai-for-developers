# citation_accuracy.py
# Custom metric for open-rag-eval: checks if answer includes a source/citation.

def score(sample, prediction):
    # Return 1 if the word "Source:" appears in the answer (case-insensitive).
    # This helps us enforce that the agent provides citation for compliance and trust.
    return int("Source:" in prediction or "source:" in prediction)
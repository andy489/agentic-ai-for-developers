import os

def must_get(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required env var: {name}")
    return value

AZURE_OPENAI_ENDPOINT = must_get("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = must_get("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")
AZURE_OPENAI_CHAT_DEPLOYMENT = must_get("AZURE_OPENAI_CHAT_DEPLOYMENT")
AZURE_OPENAI_CHAT_MODEL = os.getenv("AZURE_OPENAI_CHAT_MODEL", "gpt-4o-mini")

AZURE_AI_SEARCH_SERVICE_NAME = must_get("AZURE_AI_SEARCH_SERVICE_NAME")
AZURE_AI_SEARCH_INDEX_NAME = must_get("AZURE_AI_SEARCH_INDEX_NAME")
AZURE_AI_SEARCH_API_KEY = must_get("AZURE_AI_SEARCH_API_KEY")

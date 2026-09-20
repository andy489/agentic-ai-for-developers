from __future__ import annotations

from typing import List
from langchain_community.retrievers.azure_ai_search import AzureAISearchRetriever

from shared.config import (
    AZURE_AI_SEARCH_API_KEY,
    AZURE_AI_SEARCH_INDEX_NAME,
    AZURE_AI_SEARCH_SERVICE_NAME,
)

def _build_retriever(top_k: int = 5) -> AzureAISearchRetriever:
    return AzureAISearchRetriever(
        api_key=AZURE_AI_SEARCH_API_KEY,
        service_name=AZURE_AI_SEARCH_SERVICE_NAME,
        index_name=AZURE_AI_SEARCH_INDEX_NAME,
        top_k=top_k,
    )

def search_runbooks_sync(query: str, top_k: int = 5) -> str:
    """
    Search internal runbooks/postmortems for incident triage.
    Returns short snippets with source names.
    """
    retriever = _build_retriever(top_k=top_k)
    docs = retriever.get_relevant_documents(query)

    if not docs:
        return "No relevant runbooks found."

    lines: List[str] = []
    for i, d in enumerate(docs, start=1):
        title = (
            d.metadata.get("title")
            or d.metadata.get("source")
            or d.metadata.get("file_name")
            or "unknown-source"
        )
        snippet = (d.page_content or "").strip().replace("\n", " ")
        snippet = snippet[:500] + ("..." if len(snippet) > 500 else "")
        lines.append(f"[{i}] {title}: {snippet}")

    return "\n".join(lines)

# AutoGen expects tools can be async; wrap sync retriever.
async def search_runbooks(query: str) -> str:
    """Tool: query the runbook knowledge base (Azure AI Search) and return relevant snippets."""
    return search_runbooks_sync(query=query, top_k=5)
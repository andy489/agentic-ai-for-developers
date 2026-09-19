import hashlib
from colorama import Fore
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from utils import (
    llm,
    vector_store,
    checkpointer,
    dev_config,
    reviewer_config,
    lead_config,
    dev_prompt,
    reviewer_prompt,
    lead_prompt,
    convo_buffer,
    retrieve_memory,
    update_short_term_memory,
    store_memory,
)

# -----------------------------
# In-memory response cache (sha256 keyed)
# -----------------------------
_response_cache: dict[str, str] = {}


def _extract_last_message(response) -> str:
    """Safely extract the final text from an agent response."""
    if isinstance(response, str):
        return response
    if isinstance(response, dict):
        messages = response.get("messages", [])
        if messages:
            last = messages[-1]
            if hasattr(last, "content"):
                return str(last.content)
            if isinstance(last, dict):
                return str(last.get("content", ""))
            return str(last)
    return str(response)


def _cache_key(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


# -----------------------------
# Memory tools (shared across agents)
# -----------------------------

@tool(response_format="content_and_artifact")
def retrieve_context_tool(query: str):
    """Retrieve relevant coding standards from the RAG index."""
    docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        f"Source: {doc.metadata}\nContent:\n{doc.page_content}" for doc in docs
    )
    return serialized, docs


@tool
def retrieve_memory_tool(query: str) -> str:
    """Search long-term engineering memory."""
    memories, _ = retrieve_memory(query, k=3)
    # TODO: return the joined memories string, or "No relevant memory found." if empty
    pass


@tool
def store_memory_tool(text: str, memory_type: str = "long") -> str:
    """Store text in short-term buffer or persistent long-term memory (ChromaDB)."""
    # TODO: if memory_type == "short", update_short_term_memory
    #       if memory_type == "long", store_memory
    #       return a confirmation string
    pass


_tools = [retrieve_context_tool, retrieve_memory_tool, store_memory_tool]

# -----------------------------
# Agents
# TODO: create dev_agent, reviewer_agent, lead_agent using create_react_agent
#       pass: llm, tools=_tools, prompt=<role_prompt>, checkpointer=checkpointer
# -----------------------------

dev_agent = None       # TODO
reviewer_agent = None  # TODO
lead_agent = None      # TODO


# -----------------------------
# Tools that wrap agent calls (used as LangGraph nodes)
# -----------------------------

@tool
def write_code(feature_description: str) -> str:
    """Generate code or specs for a given feature."""
    # TODO: check _response_cache for a hit, invoke dev_agent if miss, cache result
    pass


@tool
def review_code(code_snippet: str) -> str:
    """Review code and provide structured feedback."""
    # TODO: invoke reviewer_agent and return extracted text
    pass


@tool
def approve_code(review_feedback: str) -> str:
    """Approve or reject code based on review feedback."""
    # TODO: invoke lead_agent and return extracted text
    pass

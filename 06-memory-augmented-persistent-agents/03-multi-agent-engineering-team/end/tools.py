import hashlib
from colorama import Fore
from langchain_core.messages import AIMessage
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from utils import (
    llm,
    vector_store,
    memory_store,
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
    return "\n\n".join(memories) if memories else "No relevant memory found."


@tool
def store_memory_tool(text: str, memory_type: str = "long") -> str:
    """Store text in short-term buffer or persistent long-term memory (ChromaDB)."""
    if memory_type == "short":
        update_short_term_memory({"short_term_memory": convo_buffer}, text)
        return "Stored in short-term memory"
    if memory_type == "long":
        store_memory(text)
        return "Stored in long-term memory"
    return "Invalid memory_type — use 'short' or 'long'"


_tools = [retrieve_context_tool, retrieve_memory_tool, store_memory_tool]

# -----------------------------
# Agents
# -----------------------------

dev_agent = create_react_agent(
    llm,
    tools=_tools,
    prompt=dev_prompt,
    checkpointer=checkpointer,
)

reviewer_agent = create_react_agent(
    llm,
    tools=_tools,
    prompt=reviewer_prompt,
    checkpointer=checkpointer,
)

lead_agent = create_react_agent(
    llm,
    tools=_tools,
    prompt=lead_prompt,
    checkpointer=checkpointer,
)


# -----------------------------
# Tools that wrap agent calls (used as LangGraph nodes)
# -----------------------------

@tool
def write_code(feature_description: str) -> str:
    """Generate code or specs for a given feature."""
    key = _cache_key(feature_description)
    if key in _response_cache:
        print(Fore.YELLOW + "Cache hit: write_code" + Fore.RESET)
        return _response_cache[key]

    response = dev_agent.invoke(
        {"messages": [{"role": "user", "content": feature_description}]},
        config=dev_config,
    )
    result = _extract_last_message(response)
    _response_cache[key] = result

    store_memory(f"Dev wrote code for: {feature_description[:120]}")
    return result


@tool
def review_code(code_snippet: str) -> str:
    """Review code and provide structured feedback."""
    response = reviewer_agent.invoke(
        {"messages": [{"role": "user", "content": code_snippet}]},
        config=reviewer_config,
    )
    result = _extract_last_message(response)
    store_memory(f"Reviewed code: {code_snippet[:120]}")
    return result


@tool
def approve_code(review_feedback: str) -> str:
    """Approve or reject code based on review feedback."""
    response = lead_agent.invoke(
        {"messages": [{"role": "user", "content": review_feedback}]},
        config=lead_config,
    )
    return _extract_last_message(response)

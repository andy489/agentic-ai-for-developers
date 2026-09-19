import os
import uuid
import getpass
from typing import TypedDict

from dotenv import load_dotenv
from colorama import Fore
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# -----------------------------
# Setup
# -----------------------------
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter OpenAI API key: ")

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, max_tokens=4000)


class WorkflowState(TypedDict, total=False):
    task: str
    code: str
    review: str
    approval: str
    config: dict
    short_term_memory: list[str]
    summary: str


# Unique thread IDs keep each agent's conversation history isolated
dev_thread = str(uuid.uuid4())
reviewer_thread = str(uuid.uuid4())
lead_thread = str(uuid.uuid4())

dev_config = {"configurable": {"thread_id": dev_thread}}
reviewer_config = {"configurable": {"thread_id": reviewer_thread}}
lead_config = {"configurable": {"thread_id": lead_thread}}

shared_config = {"configurable": {"thread_id": "multi-agent-engineering-thread"}}

dev_prompt = (
    "You are a developer agent. Use the retrieve_context_tool to check coding standards "
    "and retrieve_memory_tool to check past decisions before writing code or specs."
)
reviewer_prompt = (
    "You are a code reviewer agent. Use the retrieve_context_tool to check coding standards "
    "and retrieve_memory_tool to look up prior reviews. Provide clear, actionable feedback."
)
lead_prompt = (
    "You are a lead developer agent. Review the code and feedback, then respond with "
    "exactly 'approved' if the code meets standards or 'rejected: <reason>' if it needs more work."
)

# -----------------------------
# RAG — load and index coding standards
# -----------------------------
_loader = TextLoader("coding_standards.txt")
_docs = _loader.load()

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
_splits = _splitter.split_documents(_docs)

# PersistentClient auto-persists — no explicit .persist() call needed
vector_store = Chroma(
    collection_name="coding_standards",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)
vector_store.add_documents(documents=_splits)

# -----------------------------
# Short-term memory (sliding window buffer)
# -----------------------------
MAX_SHORT_TERM = 6
convo_buffer: list[str] = []

checkpointer = InMemorySaver()


def update_short_term_memory(state: WorkflowState, entry: str) -> list[str]:
    """Append entry to short-term memory and enforce the sliding window."""
    memory = list(state.get("short_term_memory") or [])
    memory.append(entry)
    trimmed = memory[-MAX_SHORT_TERM:]
    state["short_term_memory"] = trimmed
    return trimmed


# -----------------------------
# Long-term memory (ChromaDB persistent vector store)
# -----------------------------
memory_store = Chroma(
    collection_name="engineering_memory",
    embedding_function=embeddings,
    persist_directory="./chroma_db",
)


def store_memory(text: str) -> None:
    """Store a memory entry in ChromaDB."""
    memory_store.add_texts(
        texts=[text],
        metadatas=[{"source": "agent_memory"}],
        ids=[str(uuid.uuid4())],
    )


def count_all_memories() -> int:
    """Return the total number of entries in long-term memory."""
    return len(memory_store.get()["ids"])


def retrieve_memory(query: str, k: int = 3) -> tuple[list[str], int]:
    """Return (relevant passages, total memory count) for a query."""
    docs = memory_store.similarity_search(query, k=k)
    return [doc.page_content for doc in docs], count_all_memories()


# -----------------------------
# Memory pruning & summarization
# -----------------------------
MAX_MEMORY_BEFORE_SUMMARY = 6


def summarize_compress_memory(text: str) -> str:
    """Summarize text using the LLM when it exceeds a useful length."""
    if len(text) < 500:
        return text
    return llm.invoke(
        "Summarize and compress the following engineering knowledge "
        "into reusable insights:\n\n" + text
    ).content


def prune_long_term_memory(max_docs: int = 100) -> str:
    """
    Prune long-term memory when it exceeds max_docs:
    - Summarize the oldest excess entries
    - Delete originals
    - Store compressed summary
    """
    all_items = memory_store._collection.get(include=["metadatas"])
    ids = all_items.get("ids", [])

    if len(ids) <= max_docs:
        return "No pruning required"

    excess = len(ids) - max_docs
    prune_ids = ids[:excess]

    prune_docs = memory_store._collection.get(ids=prune_ids, include=["documents"])
    combined = "\n".join(prune_docs.get("documents", []))

    summary = llm.invoke(
        "Summarize and compress the following engineering knowledge:\n" + combined
    ).content

    memory_store._collection.delete(ids=prune_ids)
    memory_store.add_texts(
        texts=[summary],
        metadatas=[{"source": "memory_pruned_summary"}],
        ids=[str(uuid.uuid4())],
    )

    return f"Pruned {excess} memories and stored compressed summary."


# -----------------------------
# LangGraph workflow nodes
# -----------------------------

def short_memory_maintenance_node(state: WorkflowState) -> WorkflowState:
    """Summarize short-term memory when it hits the limit."""
    memory = state.get("short_term_memory") or []
    if len(memory) >= MAX_MEMORY_BEFORE_SUMMARY:
        summary = summarize_compress_memory("\n".join(memory))
        return {**state, "short_term_memory": [summary], "summary": summary}
    return state


def long_term_maintenance_node(state: WorkflowState) -> WorkflowState:
    """Trigger long-term memory pruning."""
    prune_long_term_memory(max_docs=100)
    return state


def summarizer_node(state: WorkflowState) -> WorkflowState:
    """Generate a structured engineering summary for long-term storage."""
    context = f"""
Task:
{state.get('task', '')}

Final Decision:
{state.get('approval', '')}

Recent Actions:
{state.get('short_term_memory', [])}
"""
    summary = llm.invoke(
        "You are summarizing engineering workflow knowledge.\n\n"
        "Extract:\n"
        "- Key technical decisions\n"
        "- Design improvements\n"
        "- Bugs or risks identified\n"
        "- Performance or security considerations\n\n"
        "Compress into a reusable long-term engineering insight.\n\n"
        f"Context:\n{context}"
    ).content

    return {**state, "summary": summary}


def decision_router_node(state: WorkflowState) -> WorkflowState:
    """Pass approval state through — used as the conditional routing source."""
    return {**state, "approval": state.get("approval", "rejected")}

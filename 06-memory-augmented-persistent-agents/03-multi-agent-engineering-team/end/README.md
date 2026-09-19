# Build an Engineering AI Team (LangChain + LangGraph)
A hands-on project demonstrating how to orchestrate a multi-agent AI engineering team using LangChain and LangGraph. This solution models a realistic engineering workflow with distinct roles (developer, reviewer, lead) and integrates:
- Multi-agent orchastration
- Advanced Memory Management (Short-term, Long-term)
- Memory summarization and pruning 
- Intelligent Caching
- Observability & Monitoring (LangSmith)

---

[1]- Python installation
[2]- Create and activate a virtual Environment
[3]- Install packages
[4]- Create API keys & set the environment variables 
[5]- Project 

### [1]-Python installation

#### macOS
1. **Check if Python is already installed**
   ```sh
   python3 --version
   ```
   If Python is not installed, proceed with the steps below.

2. **Install Homebrew (if not installed)**
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

3. **Install Python**
   ```sh
   brew install python3
   ```

4. **Check Python Version**
   ```sh
   python3 --version
   ```

#### Windows
1. **Download Python** from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Run the installer** and check the box **"Add Python to PATH"** before proceeding with the installation.

3. **Check Python Version**
   ```sh
   python --version
   ```

---

### [2]-Create and activate a virtual environment - [venv](https://docs.python.org/3/library/venv.html)

#### macOS
1. **Navigate to your project directory**
   ```sh
   cd /path/to/your/project
   ```

2. **Create a virtual environment**
   ```sh
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**
   ```sh
   source .venv/bin/activate
   ```

4. **Verify that the virtual environment is active** (you should see `(venv)` in the terminal prompt).

#### Windows
1. **Navigate to your project directory**
   ```sh
   cd C:\path\to\your\project
   ```

2. **Create a virtual environment**
   ```sh
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   ```sh
   .venv\Scripts\activate
   ```

4. **Verify that the virtual environment is active** (Command Prompt should show `(venv)` before the directory path).

---

## Deactivating the Virtual Environment
For both macOS and Windows, deactivate the virtual environment by running:
```sh
 deactivate
```

---

### [3]-Install packages
(Mac)
```sh
pip3 install -r requirements.txt
```

(Windows)
```sh
pip install -r requirements.txt
```

---

## Exiting the Virtual Environment
Simply run:
```sh
deactivate
```

### [4]-Create API keys & set the environment variables 

#### 4.1 Setting Up OpenAI Secret Key  
1. Create an OpenAI Account[OpenAI's API Keys page](https://platform.openai.com/signup/),
2. Go to [OpenAI's API Keys page](https://platform.openai.com/settings/organization/api-keys),
3. Click **Create new secret key** and copy it, 
4. You will need to add your billing information (MANAGE > Settings > Billing).  

#### 4.2 Setting up LANGSMITH
1. Create an account : [Sign Up](https://smith.langchain.com/),
2. Create an [API Key](https://smith.langchain.com/o/64f05e18-d0b3-5b52-b1a2-201ed3a50b18/settings/apikeys),
3. Configure environment. Add to `env` file:

```sh
LANGSMITH_TRACING=true
LANGSMITH_API_KEY=<your-api-key>
OPENAI_API_KEY=<your-openai-api-key>
LANGSMITH_WORKSPACE_ID=<your-workspace-id>
```

### -Start the app
(Mac)
```sh
python3 main.py
```

(Windows)
```sh
python main.py
```

### [5]- Project STEPS

1. MEMORY STORAGE & MAINTENANCE
- Short-term Memory
- Long-Term Memory (ChromaDB Persistent Vector Store)
2. MEMORY OPTIMIZATION TECHNIQUES AND STRATEGIES
- Memory Pruning & Summarization
- Caching Responses 
3. TESTING & TRACING

# -----------------------------
# Workflow Architecture
# -----------------------------

```sh
START → User Task
   ↓
Memory Retrieval
   ↓
Developer
   ↓
Reviewer
   ↓
Lead Approval
   ↓
Decision_router
   |_ Approved → Summarizer Node → Short_memory_maintenance → Long_term_maintenance → END
   |_ Rejected → Developer (loop back for revisions)

```

# -----------------------------
#### MEMORY STORAGE & MAINTENANCE
# -----------------------------

##### Short-term Memory
```python
# thread-level persistence
checkpointer = InMemorySaver() 
shared_config = {"configurable": {"thread_id": "multi-agent-engineering-thread"}}



# Conversation Buffer (short-term Memory)
MAX_SHORT_TERM = 6
convo_buffer: list[str] = []
def update_short_term_memory(state: WorkflowState, entry: str):
    """Append new entry to short-term memory and maintain size limit."""
    memory = state.get("short_term_memory", [])
    memory.append(entry)
    state["short_term_memory"] = memory[-MAX_SHORT_TERM:]  # keep only recent entries
```
##### Long-Term Memory (ChromaDB Persistent Vector Store)

```python

memory_store = Chroma(
    collection_name="engineering_memory",
    embedding_function=embeddings,
    persist_directory="./chroma_db"   # persists to disk
)

def store_memory(text: str):
    """Store memory in ChromaDB with metadata for retrieval."""
    memory_store.add_texts(
        texts=[text],
        metadatas=[{"source": "agent_memory"}],
        ids=[str(uuid.uuid4())]
    )
    memory_store.persist()

def count_all_memories():
    """Helper function to count total memories in ChromaDB."""
    data = memory_store.get()
    return len(data['ids'])

def retrieve_memory(query: str, k: int = 3):
    """Retrieve relevant memories from ChromaDB based on a query."""
    docs = memory_store.similarity_search(query, k=k)
    memories_count = count_all_memories()
    return [doc.page_content for doc in docs], memories_count
```


# -----------------------------
#### MEMORY OPTIMIZATION TECHNIQUES AND STRATEGIES
# -----------------------------


##### Memory Pruning & Summarization

```python
MAX_MEMORY_BEFORE_SUMMARY = 6

def summarize_compress_memory(text: str):
    """
    Summarize text if it exceeds threshold.
    """
    if len(text) < 500:
        return text

    prompt = (
        "Summarize and compress the following engineering knowledge "
        "into reusable insights:\n\n" + text
    )
    return llm.invoke(prompt).content

        
def prune_long_term_memory(max_docs: int = 100):
    """
    Prune long-term memory in ChromaDB when it exceeds max_docs.
    Strategy:
        - Retrieve oldest documents
        - Summarize them
        - Delete originals
        - Store compressed summary
    """

    # Get all IDs
    all_items = memory_store._collection.get(include=["metadatas"])
    ids = all_items.get("ids", [])

    if len(ids) <= max_docs:
        return "No pruning required"

    # Determine how many to prune
    excess = len(ids) - max_docs

    # Get oldest items (assumes insertion order)
    prune_ids = ids[:excess]

    prune_docs = memory_store._collection.get(
        ids=prune_ids,
        include=["documents"]
    )

    documents = prune_docs.get("documents", [])

    combined_text = "\n".join(documents)

    # Summarize
    summary = llm.invoke(
        "Summarize and compress the following engineering knowledge:\n"
        + combined_text
    ).content

    # Delete old entries
    memory_store._collection.delete(ids=prune_ids)

    # Store summary
    memory_store.add_texts(
        texts=[summary],
        metadatas=[{"source": "memory_pruned_summary"}],
        ids=[str(uuid.uuid4())]
    )

    memory_store.persist()

    return f"Pruned {excess} memories and stored compressed summary."


def short_memory_maintenance_node(state: WorkflowState):
    """Maintain short-term memory by pruning old entries and summarizing when limit is exceeded."""
    memory = state.get("short_term_memory", [])

    if len(memory) >= MAX_MEMORY_BEFORE_SUMMARY:
        combined = "\n".join(memory)
        summary = summarize_compress_memory(combined)

        return {
            **state,
            "short_term_memory": [summary],
            "summary": summary
        }

    return state
        
def long_term_maintenance_node(state: WorkflowState):
    """Maintain long-term memory by invoking pruning when necessary."""
    prune_long_term_memory(max_docs=100)
    return state

def summarizer_node(state: WorkflowState):
    """
    Generate a structured engineering summary of the workflow.
    This summary is optimized for long-term memory storage.
    """

    task = state.get("task", "")
    approval = state.get("approval", "")
    short_term_memory = state.get("short_term_memory", [])

    combined_context = f"""
    Task:
    {task}

    Final Decision:
    {approval}

    Recent Actions:
    {short_term_memory}
    """

    summary = llm.invoke(
        f"""
        You are summarizing engineering workflow knowledge.

        Extract:
        - Key technical decisions
        - Design improvements
        - Bugs or risks identified
        - Performance or security considerations

        Compress the information into a reusable long-term engineering insight.

        Context:
        {combined_context}
        """
    ).content

    return {
        **state,
        "summary": summary
    }

```

##### Caching Responses 

```python
def check_cache(state: AgentState, runtime: Runtime):
    """
    Return cached response if query already seen.
    """
    if not state["messages"]:
        return None
    last_msg = state["messages"][-1].content
    key = hashlib.sha256(last_msg.encode()).hexdigest()
    if key in response_cache:
        print(Fore.YELLOW + "⚡ Returning cached response" + Fore.RESET)
        return {
            "messages": [AIMessage(content=response_cache[key])],
            "jump_to": "end"
        }
    return None
```
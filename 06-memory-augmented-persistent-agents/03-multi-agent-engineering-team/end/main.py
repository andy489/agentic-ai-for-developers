from langgraph.graph import END, StateGraph

from dotenv import load_dotenv
import warnings
from colorama import Fore
from utils import (
    WorkflowState, 
    shared_config, 
    update_short_term_memory, 
    short_memory_maintenance_node,
    long_term_maintenance_node,
    decision_router_node,
    summarizer_node
)  
from tools import (
    write_code, 
    review_code, 
    approve_code
)

load_dotenv()

# Silence all warnings
warnings.filterwarnings("ignore")
# -----------------------------
# Workflow Architecture
# -----------------------------

"""
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

"""

# ----------------------------
# Build a Langraph Workflow
# ----------------------------

# Worklow nodes that wrap the tool calls and return outputs for the next node

def dev_node(state: WorkflowState):
    code = write_code.invoke(state["task"], config=state["config"])

    short_memory = update_short_term_memory(
        state,
        f"Dev created code for: {state['task']}"
    )
    return {**state, "code": code, "short_term_memory": short_memory}

def review_node(state):
    result = review_code.invoke(state["code"], config=state["config"])
    short_memory = update_short_term_memory(
        state,
        f"Code reviewed: {state['code']}"
    )
    return {**state, "review": result, "short_term_memory": short_memory}

def lead_node(state):
    result = approve_code.invoke(state["review"], config=state["config"])
    short_memory = update_short_term_memory(
        state,
        f"Code approved: {state['review']}"
    )
    return {**state, "approval": result, "short_term_memory": short_memory}


# Build the Graph with StateGraph and define edges
graph = StateGraph(WorkflowState) 

# --- Core Agent Nodes ---
graph.add_node("dev", dev_node)
graph.add_node("review", review_node)
graph.add_node("lead", lead_node)

# --- Memory Nodes ---
graph.add_node("summarizer", summarizer_node)
graph.add_node("short_memory_maintenance", short_memory_maintenance_node)
graph.add_node("long_term_maintenance", long_term_maintenance_node)

# --- Routing Node ---
graph.add_node("decision_router", decision_router_node)

# Entry
graph.set_entry_point("dev")

# --- Core Flow ---
graph.add_edge("dev", "review")
graph.add_edge("review", "lead")

# --- Decision Branching ---
graph.add_edge("lead", "decision_router")

# Conditional routing
graph.add_conditional_edges(
    "decision_router",
    lambda state: state.get("approval"),
    {
        "approved": "summarizer",
        "rejected": "dev"
    }
)

# --- Memory Flow ---
graph.add_edge("summarizer", "short_memory_maintenance")
graph.add_edge("short_memory_maintenance", "long_term_maintenance")
graph.add_edge("long_term_maintenance", END)

workflow = graph.compile()

# Run the workflow
def main():
    while True:
        task = input("\nTask (exit to quit): ")

        if task == "exit":
            break
        
        print(f"{Fore.CYAN}START: {task}\n")
        print(f"Task: {task}{Fore.RESET}\n")
        print("-> Running workflow...task in progress\n")


        result = workflow.invoke({
            "task": task,
            "config": shared_config
        })

        print("\nFINAL RESULT:")
        print(result["approval"])
        
if __name__ == "__main__":
    main()
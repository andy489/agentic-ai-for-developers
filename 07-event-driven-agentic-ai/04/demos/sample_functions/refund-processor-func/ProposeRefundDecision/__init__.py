import os
import json
import azure.functions as func

from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, END

def _llm():
    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
        api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2024-06-01"),
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
        temperature=0.2,
    )

# State for the graph
# (Keeping it dict-based to stay lightweight)
def build_graph():
    llm = _llm()

    def policy_check(state: dict) -> dict:
        # In real life: fetch order data, policy, fraud signals, SLA tier, etc.
        req = state["request"]
        state["policy"] = {
            "max_auto_refund": 50,
            "partial_refund_pct_on_timeout": 0.25
        }
        state["facts"] = {
            "order_total": float(req.get("order_total", 0)),
            "currency": req.get("currency", "USD"),
            "reason": req.get("reason", "unspecified"),
            "customer_tier": req.get("customer_tier", "standard")
        }
        return state

    def propose(state: dict) -> dict:
        prompt = f"""
You are a refund decision agent. Return STRICT JSON only.

Facts:
{json.dumps(state["facts"], indent=2)}

Policy:
{json.dumps(state["policy"], indent=2)}

Decide:
- type: full_refund | partial_refund | deny
- amount (number)
- currency
- rationale (short)
- risk_notes (short)
"""
        resp = llm.invoke(prompt)
        text = resp.content if hasattr(resp, "content") else str(resp)
        try:
            decision = json.loads(text)
        except Exception:
            # Fallback: conservative partial
            decision = {
                "type": "partial_refund",
                "amount": round(state["facts"]["order_total"] * 0.15, 2),
                "currency": state["facts"]["currency"],
                "rationale": "Model output not valid JSON; conservative partial refund.",
                "risk_notes": "Verify order details."
            }

        # Ensure bounds
        if decision.get("type") == "full_refund":
            decision["amount"] = round(state["facts"]["order_total"], 2)
        if decision.get("type") == "partial_refund":
            decision["amount"] = max(0.0, min(round(float(decision.get("amount", 0)), 2), state["facts"]["order_total"]))
        if decision.get("type") == "deny":
            decision["amount"] = 0.0

        decision["currency"] = state["facts"]["currency"]
        state["proposal"] = decision
        return state

    g = StateGraph(dict)
    g.add_node("policy_check", policy_check)
    g.add_node("propose", propose)
    g.set_entry_point("policy_check")
    g.add_edge("policy_check", "propose")
    g.add_edge("propose", END)
    return g.compile()

graph = build_graph()

def main(name: func.Context) -> func.HttpResponse:
    # Durable activity binding passes input via context in Python Functions;
    # Many templates use df for activities. If you already have an activity template, adapt accordingly.
    # For clarity here, assume you’re using the standard Durable Functions activity signature in your project.
    raise NotImplementedError("Use Durable Functions activity template binding for Python and call graph.invoke(input).")

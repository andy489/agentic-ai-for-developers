import json
import azure.functions as func

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from shared.config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_API_VERSION,
    AZURE_OPENAI_CHAT_DEPLOYMENT,
    AZURE_OPENAI_CHAT_MODEL,
)
from shared.runbook_search import search_runbooks_sync, search_runbooks
from shared.prompts import LANGCHAIN_DRAFT_SYSTEM, LANGCHAIN_DRAFT_USER

app = func.FunctionApp()

def _json_response(payload: dict, status: int = 200) -> func.HttpResponse:
    return func.HttpResponse(
        body=json.dumps(payload, ensure_ascii=False, indent=2),
        status_code=status,
        mimetype="application/json",
    )

def _parse_body(req: func.HttpRequest) -> dict:
    try:
        return req.get_json()
    except Exception:
        raise ValueError("Invalid JSON body.")

# -------------------------
# LangChain: RAG Draft
# -------------------------
@app.function_name(name="LangChainDraft")
@app.route(route="langchain/draft", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def langchain_draft(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = _parse_body(req)
        title = body.get("title", "").strip()
        symptoms = body.get("symptoms", "").strip()
        context = body.get("context", "").strip()

        if not title or not symptoms:
            return _json_response(
                {"error": "Provide at least 'title' and 'symptoms'."},
                status=400,
            )

        # Retrieve snippets from Azure AI Search (vector/hybrid index)
        snippets = search_runbooks_sync(query=f"{title}\n{symptoms}\n{context}", top_k=5)

        llm = AzureChatOpenAI(
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT,
            temperature=0.2,
        )

        user_prompt = LANGCHAIN_DRAFT_USER.format(
            title=title, symptoms=symptoms, context=context, snippets=snippets
        )

        # Ask for JSON output, but still validate in code (models sometimes return extra text).
        resp = llm.invoke([SystemMessage(
            content=LANGCHAIN_DRAFT_SYSTEM),
            HumanMessage(content=user_prompt)])
        text = resp.content if hasattr(resp, "content") else str(resp)

        # Best-effort parse: if it's not valid JSON, return raw text for demo visibility.
        try:
            parsed = json.loads(text)
            return _json_response({"mode": "langchain_rag", "result": parsed})
        except Exception:
            return _json_response({"mode": "langchain_rag", "result_raw": text})

    except ValueError as ve:
        return _json_response({"error": str(ve)}, status=400)
    except Exception as e:
        return _json_response({"error": f"Server error: {e}"}, status=500)

# -------------------------
# AutoGen: Multi-agent Incident Team
# -------------------------
@app.function_name(name="AutoGenIncident")
@app.route(route="autogen/incident", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
async def autogen_incident(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = _parse_body(req)
        title = body.get("title", "").strip()
        symptoms = body.get("symptoms", "").strip()
        context = body.get("context", "").strip()

        if not title or not symptoms:
            return _json_response(
                {"error": "Provide at least 'title' and 'symptoms'."},
                status=400,
            )

        # Azure OpenAI model client for AutoGen
        # (AutoGen docs show AzureOpenAIChatCompletionClient for Azure endpoints) :contentReference[oaicite:7]{index=7}
        model_client = AzureOpenAIChatCompletionClient(
            model=AZURE_OPENAI_CHAT_MODEL,                 # e.g., "gpt-4o-mini" (capabilities come from name)
            api_key=AZURE_OPENAI_API_KEY,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_deployment=AZURE_OPENAI_CHAT_DEPLOYMENT,
            api_version=AZURE_OPENAI_API_VERSION,
            # Avoid concurrency surprises when teams/tools are involved
            parallel_tool_calls=False,
        )

        # Tool: runbook search (async)
        tools = [search_runbooks]

        triage_lead = AssistantAgent(
            name="TriageLead",
            model_client=model_client,
            system_message=(
                "You are the incident triage lead. Decide what to do next. "
                "Ask other agents for inputs. Finish by requesting a final customer update + internal steps."
            ),
            tools=tools,
            reflect_on_tool_use=True,
        )

        runbook_researcher = AssistantAgent(
            name="RunbookResearcher",
            model_client=model_client,
            system_message=(
                "You search internal runbooks/postmortems. Use the search_runbooks tool. "
                "Return key snippets and recommended checks. Keep it short."
            ),
            tools=tools,
            reflect_on_tool_use=True,
        )

        fix_planner = AssistantAgent(
            name="FixPlanner",
            model_client=model_client,
            system_message=(
                "You propose mitigations/rollback plans and verification steps. "
                "Prefer low-risk mitigations first. Provide a step-by-step plan."
            ),
            tools=tools,
            reflect_on_tool_use=True,
        )

        risk_reviewer = AssistantAgent(
            name="RiskReviewer",
            model_client=model_client,
            system_message=(
                "You review customer-facing text for safety: no guarantees, no blame, no sensitive details. "
                "If acceptable, respond with 'APPROVED' and the improved customer update. "
                "If not, respond with 'CHANGES NEEDED' and corrections."
            ),
        )

        # Dynamic team: SelectorGroupChat picks next speaker based on conversation context :contentReference[oaicite:8]{index=8}
        termination = TextMentionTermination("APPROVED")
        hard_cap = MaxMessageTermination(14)

        team = SelectorGroupChat(
            participants=[triage_lead, runbook_researcher, fix_planner, risk_reviewer],
            model_client=model_client,  # used for selecting the next speaker
            termination_condition=termination | hard_cap,
        )

        task = f"""We have an incident.

Title: {title}
Symptoms: {symptoms}
Context: {context}

Goals:
1) Gather likely causes and validation steps using runbooks.
2) Produce internal triage steps (engineer-facing).
3) Produce a customer update (2-4 sentences) reviewed by RiskReviewer.
When RiskReviewer is satisfied, they must include the word APPROVED.
"""

        result = await team.run(task=task)

        messages = []
        for m in result.messages:
            # m has fields like source/content/type
            content = getattr(m, "content", "")
            source = getattr(m, "source", "unknown")
            mtype = getattr(m, "type", m.__class__.__name__)
            messages.append({"source": source, "type": mtype, "content": content})

        # Best-effort: find the last RiskReviewer message to show as "final"
        final_customer_update = None
        for m in reversed(messages):
            if m["source"] == "RiskReviewer":
                final_customer_update = m["content"]
                break

        await model_client.close()

        return _json_response(
            {
                "mode": "autogen_multi_agent",
                "final_customer_update_candidate": final_customer_update,
                "transcript": messages,
            }
        )

    except ValueError as ve:
        return _json_response({"error": str(ve)}, status=400)
    except Exception as e:
        return _json_response({"error": f"Server error: {e}"}, status=500)

import datetime
import azure.durable_functions as df

# Time windows
HUMAN_APPROVAL_WINDOW_MIN = 15
POST_ESCALATION_WINDOW_MIN = 30  # "appropriate time window" after escalation

AUTO_REFUND_THRESHOLD_USD = 200

def _to_number(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def orchestrator_function(context: df.DurableOrchestrationContext):
    req = context.get_input() or {}
    refund_id = req.get("refund_id") or context.instance_id

    # 1) Run "agentic" decision (LangGraph) as an activity
    proposal = yield context.call_activity("ProposeRefundDecision", {
        "refund_id": refund_id,
        "request": req
    })

    # Auto-refund path for <= $200 USD
    currency = (proposal.get("currency") or "").upper().strip()
    amount = _to_number(proposal.get("amount"))

    if currency == "USD" and amount is not None and amount <= AUTO_REFUND_THRESHOLD_USD:
        result = yield context.call_activity("ExecuteRefund", {
            "refund_id": refund_id,
            "decision": proposal,
            "mode": "auto_refund_under_threshold"
        })
        yield context.call_activity("WriteAuditLog", {
            "refund_id": refund_id,
            "state": "AUTO_REFUNDED_UNDER_THRESHOLD",
            "proposal": proposal,
            "threshold_usd": AUTO_REFUND_THRESHOLD_USD,
            "result": result
        })
        return {"status": "auto_refunded", "refund_id": refund_id, "result": result}

    # 2) Ask human for approval + wait up to 15 minutes
    yield context.call_activity("NotifyHumanForApproval", {
        "refund_id": refund_id,
        "proposal": proposal,
        "instance_id": context.instance_id
    })

    human_deadline = context.current_utc_datetime + datetime.timedelta(minutes=HUMAN_APPROVAL_WINDOW_MIN)
    approval_event = context.wait_for_external_event("RefundApproval")  # expects {"decision":"approve|reject", "notes": "..."}
    timer = context.create_timer(human_deadline)

    winner = yield context.task_any([approval_event, timer])

    if winner == approval_event:
        human_response = approval_event.result or {}
        decision = (human_response.get("decision") or "").lower().strip()

        if decision == "approve":
            # Execute proposed refund
            result = yield context.call_activity("ExecuteRefund", {
                "refund_id": refund_id,
                "decision": proposal,
                "mode": "approved"
            })
            yield context.call_activity("WriteAuditLog", {
                "refund_id": refund_id,
                "state": "APPROVED",
                "proposal": proposal,
                "human_response": human_response,
                "result": result
            })
            return {"status": "approved", "refund_id": refund_id, "result": result}

        # Rejected by human → deny or apply human-provided override if you want
        result = yield context.call_activity("ExecuteRefund", {
            "refund_id": refund_id,
            "decision": {"type": "deny", "amount": 0, "currency": proposal.get("currency"), "reason": "Human rejected"},
            "mode": "rejected"
        })
        yield context.call_activity("WriteAuditLog", {
            "refund_id": refund_id,
            "state": "REJECTED",
            "proposal": proposal,
            "human_response": human_response,
            "result": result
        })
        return {"status": "rejected", "refund_id": refund_id, "result": result}

    # 3) Timer expired → escalate via PagerDuty
    yield context.call_activity("TriggerPagerDutyEscalation", {
        "refund_id": refund_id,
        "proposal": proposal,
        "instance_id": context.instance_id
    })

    # 4) Wait for an additional window after escalation
    escalation_deadline = context.current_utc_datetime + datetime.timedelta(minutes=POST_ESCALATION_WINDOW_MIN)
    approval_event2 = context.wait_for_external_event("RefundApproval")
    timer2 = context.create_timer(escalation_deadline)
    winner2 = yield context.task_any([approval_event2, timer2])

    if winner2 == approval_event2:
        human_response = approval_event2.result or {}
        decision = (human_response.get("decision") or "").lower().strip()

        if decision == "approve":
            result = yield context.call_activity("ExecuteRefund", {
                "refund_id": refund_id,
                "decision": proposal,
                "mode": "approved_after_escalation"
            })
            yield context.call_activity("WriteAuditLog", {
                "refund_id": refund_id,
                "state": "APPROVED_AFTER_ESCALATION",
                "proposal": proposal,
                "human_response": human_response,
                "result": result
            })
            return {"status": "approved_after_escalation", "refund_id": refund_id, "result": result}

        result = yield context.call_activity("ExecuteRefund", {
            "refund_id": refund_id,
            "decision": {"type": "deny", "amount": 0, "currency": proposal.get("currency"), "reason": "Human rejected after escalation"},
            "mode": "rejected_after_escalation"
        })
        yield context.call_activity("WriteAuditLog", {
            "refund_id": refund_id,
            "state": "REJECTED_AFTER_ESCALATION",
            "proposal": proposal,
            "human_response": human_response,
            "result": result
        })
        return {"status": "rejected_after_escalation", "refund_id": refund_id, "result": result}

    # 5) Still no response → fallback partial refund
    fallback = yield context.call_activity("ComputeFallbackPartialRefund", {
        "refund_id": refund_id,
        "proposal": proposal
    })

    result = yield context.call_activity("ExecuteRefund", {
        "refund_id": refund_id,
        "decision": fallback,
        "mode": "fallback_partial"
    })

    yield context.call_activity("WriteAuditLog", {
        "refund_id": refund_id,
        "state": "FALLBACK_PARTIAL",
        "proposal": proposal,
        "fallback": fallback,
        "result": result
    })

    return {"status": "fallback_partial", "refund_id": refund_id, "result": result}

main = df.Orchestrator.create(orchestrator_function)

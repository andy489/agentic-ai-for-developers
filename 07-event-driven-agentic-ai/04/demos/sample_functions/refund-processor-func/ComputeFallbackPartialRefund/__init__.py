import azure.durable_functions as df

def main(context: df.DurableActivityContext):
    payload = context.get_input()
    proposal = payload["proposal"]

    # Example policy: fallback to 25% partial refund if no approval
    currency = proposal.get("currency", "USD")

    # If proposal was already partial, keep the smaller of proposal or fallback cap
    proposed_amount = float(proposal.get("amount", 0.0))
    # In real life you’d pull order_total from DB; for demo keep it proportional
    # Here: ensure at least something but bounded
    fallback_amount = max(5.0, round(proposed_amount * 0.5, 2)) if proposed_amount > 0 else 10.0

    return {
        "type": "partial_refund",
        "amount": fallback_amount,
        "currency": currency,
        "rationale": "Fallback partial refund applied due to no human response within SLA.",
        "risk_notes": "Follow up with human review after the fact."
    }

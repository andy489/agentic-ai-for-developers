import os
import json
import requests
import azure.durable_functions as df

def main(context: df.DurableActivityContext):
    payload = context.get_input()
    refund_id = payload["refund_id"]
    proposal = payload["proposal"]
    instance_id = payload["instance_id"]

    routing_key = os.environ["PAGERDUTY_ROUTING_KEY"]  # Events API v2 integration key
    url = "https://events.pagerduty.com/v2/enqueue"

    event = {
        "routing_key": routing_key,
        "event_action": "trigger",
        "dedup_key": f"refund-{refund_id}",
        "payload": {
            "summary": f"Refund approval SLA breached for refund_id={refund_id}",
            "source": "refund-agent",
            "severity": "warning",
            "custom_details": {
                "instance_id": instance_id,
                "proposal": proposal
            }
        }
    }

    r = requests.post(url, json=event, timeout=10)
    r.raise_for_status()
    return {"pagerduty": "triggered", "status_code": r.status_code}

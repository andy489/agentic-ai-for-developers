import azure.functions as func
import azure.durable_functions as df

# POST /api/refund/approval?instanceId=...  body: {"decision":"approve|reject","notes":"..."}
async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)

    instance_id = req.params.get("instanceId")
    if not instance_id:
        return func.HttpResponse("Missing instanceId", status_code=400)

    body = req.get_json()
    await client.raise_event(instance_id, "RefundApproval", body)
    return func.HttpResponse("OK", status_code=200)

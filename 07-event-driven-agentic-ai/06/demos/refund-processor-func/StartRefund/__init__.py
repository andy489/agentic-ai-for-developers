import azure.functions as func
import azure.durable_functions as df
import json

async def main(req: func.HttpRequest, starter: str) -> func.HttpResponse:
    client = df.DurableOrchestrationClient(starter)
    body = req.get_json()

    instance_id = await client.start_new("RefundOrchestrator", None, body)
    return client.create_check_status_response(req, instance_id)

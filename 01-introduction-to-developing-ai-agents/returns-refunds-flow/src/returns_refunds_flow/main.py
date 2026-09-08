import sys
from dotenv import load_dotenv

from returns_refunds_flow.flow import ReturnsRefundsFlow

load_dotenv()

# Sample return requests — change these to test different scenarios
SAMPLE_REQUESTS = {
    "eligible": (
        "Order #12345 placed 10 days ago. I received a pair of running shoes "
        "in size 9 but I need size 10. The shoes are unworn and still in the "
        "original box with all tags attached. I'd like a full refund."
    ),
    "ineligible": (
        "Order #67890 placed 45 days ago. I bought these trainers in the summer "
        "sale (marked final sale). I've worn them a few times but the sole is "
        "coming apart. I want a refund."
    ),
    "defective": (
        "Order #11111 placed 3 days ago. The left shoe arrived with a broken "
        "buckle — it's clearly a manufacturing defect. The shoes are otherwise "
        "brand new. I'd like a replacement or refund."
    ),
}


def run(scenario: str = "eligible"):
    request = SAMPLE_REQUESTS.get(scenario, SAMPLE_REQUESTS["eligible"])

    print(f"\n{'='*60}")
    print(f"Processing return request (scenario: {scenario})")
    print(f"{'='*60}")
    print(f"Request: {request}\n")

    flow = ReturnsRefundsFlow()
    flow.state.return_request = request
    flow.kickoff()

    print(f"\n{'='*60}")
    print("FINAL RESPONSE TO CUSTOMER")
    print(f"{'='*60}")
    print(flow.state.final_response)


if __name__ == "__main__":
    # Pass scenario as command-line argument: eligible | ineligible | defective
    scenario = sys.argv[1] if len(sys.argv) > 1 else "eligible"
    run(scenario)

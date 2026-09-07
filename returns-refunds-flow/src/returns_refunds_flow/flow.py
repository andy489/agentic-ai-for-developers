from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, router, start

from returns_refunds_flow.crews import DenialCrew, RefundCrew, ValidationCrew


class ReturnState(BaseModel):
    """Shared state that flows through every step."""

    return_request: str = ""
    validation_result: str = ""
    decision: str = ""  # "APPROVED" or "REJECTED"
    final_response: str = ""


class ReturnsRefundsFlow(Flow[ReturnState]):
    """
    A three-step Flow for processing customer return requests:

      1. validate  — ValidationCrew decides APPROVED / REJECTED
      2. route     — branches to the correct crew based on the decision
      3. approved  — RefundCrew generates return instructions  (APPROVED path)
         rejected  — DenialCrew generates an empathetic denial  (REJECTED path)
    """

    @start()
    def validate(self):
        """Step 1: validate the return request against shop policy."""
        print("\n--- Step 1: Validating return request ---")

        result = ValidationCrew().crew().kickoff(
            inputs={"return_request": self.state.return_request}
        )

        self.state.validation_result = result.raw

        # Extract the decision keyword from the crew output
        upper = result.raw.upper()
        self.state.decision = "APPROVED" if "APPROVED" in upper else "REJECTED"

        print(f"\nDecision: {self.state.decision}")
        return self.state.decision

    @router(validate)
    def route_decision(self):
        """Step 2: branch to the approved or rejected path."""
        if self.state.decision == "APPROVED":
            return "approved"
        return "rejected"

    @listen("approved")
    def process_approved(self):
        """Step 3a: generate refund instructions for approved requests."""
        print("\n--- Step 3a: Processing approved refund ---")

        result = RefundCrew().crew().kickoff(
            inputs={
                "return_request": self.state.return_request,
                "validation_result": self.state.validation_result,
            }
        )

        self.state.final_response = result.raw
        return result.raw

    @listen("rejected")
    def process_rejected(self):
        """Step 3b: generate empathetic denial for rejected requests."""
        print("\n--- Step 3b: Generating denial response ---")

        result = DenialCrew().crew().kickoff(
            inputs={
                "return_request": self.state.return_request,
                "validation_result": self.state.validation_result,
            }
        )

        self.state.final_response = result.raw
        return result.raw

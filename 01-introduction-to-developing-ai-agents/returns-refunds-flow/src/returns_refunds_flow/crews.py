from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class ValidationCrew:
    """Validates whether a return request is eligible."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def return_validator(self) -> Agent:
        return Agent(config=self.agents_config["return_validator"], verbose=True)

    @task
    def validate_return_task(self) -> Task:
        return Task(config=self.tasks_config["validate_return_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


@CrewBase
class RefundCrew:
    """Processes an approved refund and generates customer instructions."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def refund_processor(self) -> Agent:
        return Agent(config=self.agents_config["refund_processor"], verbose=True)

    @task
    def process_refund_task(self) -> Task:
        return Task(config=self.tasks_config["process_refund_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )


@CrewBase
class DenialCrew:
    """Generates an empathetic denial response with alternatives."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def denial_agent(self) -> Agent:
        return Agent(config=self.agents_config["denial_agent"], verbose=True)

    @task
    def explain_denial_task(self) -> Task:
        return Task(config=self.tasks_config["explain_denial_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class FeedbackAnalysisCrew:
    """CrewAI crew for analyzing customer feedback."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def sentiment_analyst(self) -> Agent:
        return Agent(config=self.agents_config["sentiment_analyst"], verbose=True)

    @agent
    def theme_analyst(self) -> Agent:
        return Agent(config=self.agents_config["theme_analyst"], verbose=True)

    @task
    def sentiment_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["sentiment_analysis_task"])

    @task
    def theme_analysis_task(self) -> Task:
        return Task(config=self.tasks_config["theme_analysis_task"])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

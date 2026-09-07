import sys
from feedback_analysis_crew.crew import FeedbackAnalysisCrew

SAMPLE_FEEDBACK = """
1. "The shoes arrived in 2 days — super fast! Great quality too."
2. "Terrible experience. My order was wrong and support never responded."
3. "Good shoes but the sizing runs small. Took two tries to get the right fit."
4. "Love the styles! Will definitely order again."
5. "Package arrived damaged. The shoes were fine but the box was crushed."
"""


def run():
    inputs = {"feedback": SAMPLE_FEEDBACK}
    result = FeedbackAnalysisCrew().crew().kickoff(inputs=inputs)
    print(result)


if __name__ == "__main__":
    run()

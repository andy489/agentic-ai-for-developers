# g_eval.py

import os
from openai import OpenAI
from openai.types.chat import ChatCompletionUserMessageParam

# Step 1: Instantiate the OpenAI client using the API key from environment variables.
# This is required to make requests to the OPENAI API using the latest SDK (>=1.0.0).
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def judge(question, context_docs, answer):
  """
  Evaluates an LLM-generated answer using GPT-4o as a 'judge'.
  Returns a string with a numeric score and a brief rationale.

  Parameters:
    question (str): The original user question.
    context_docs (List[Document]): Retrieved context passages from the RAG system.
    answer (str): The generated answer from the LLM agent.

  Returns:
    str: Judgment in the format: "Score: <number>\nRationale: <one sentence>"
  """

  # Step 3: Combine the text from retrieved documents into a single string.
  # We truncate to 1500 characters to stay within token limits while retaining grounding context.
  if context_docs:
    combined_context = " ".join([doc.page_content for doc in context_docs])
    context_str = combined_context[:1500]
  else:
    context_str = ""

  # Step 3: Construct the evaluation prompt for GPT-4o.
  # The model is instructed to act as an impartial grader, assign a score (1-10),
  # and explain its reasoning in one sentence. This keeps outputs concise and structured.
  prompt = f"""
    You are an impartial grader evaluating an AI-generated answer.
    Assign a score from 1 to 10 based on relevance, accuracy, and groundedness.
    
    Question: {question}
    Context: {context_str}
    Answer: {answer}
    
    Provide a score from 1 to 10, then a brief one-sentence explanation.
    Respond with this format:
    Score: <number>
    Rationale: <one sentence>
  """

  # Step 4: Use GTP-4o to score and explain the answer using a chat completion call.
  # Temperature is set ot 0 for deterministic, repeatable results.
  response = client.chat.completions.create(
      model="gpt-4o",
      messages=[ChatCompletionUserMessageParam(role="user", content=prompt)],
      temperature=0,
      max_tokens=100
  )

  # Step 5: Extract the returned message content and strip whitespace.
  return (response.choices[0].message.content or "").strip()
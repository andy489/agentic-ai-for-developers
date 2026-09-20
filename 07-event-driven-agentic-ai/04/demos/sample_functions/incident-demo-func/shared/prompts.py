LANGCHAIN_DRAFT_SYSTEM = """You are an on-call incident triage assistant.
You produce concise, practical outputs for engineers and a separate customer-facing message.
Avoid claiming certainty; use probabilities and recommend verification steps.
"""

LANGCHAIN_DRAFT_USER = """Incident:
Title: {title}
Symptoms: {symptoms}
Context: {context}

Relevant internal runbooks/postmortems (snippets):
{snippets}

Return JSON with:
- customer_update (string, 2-4 sentences, no promises)
- triage_steps (array of 5-10 concrete steps)
- likely_causes (array of 3-6 items with probabilities)
- questions_to_ask (array)
- sources_used (array of snippet ids you relied on, like [1,3])
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv
import time

# Add rag_demo folder to the Python path (if your chains live there)
sys.path.append(os.path.join(os.path.dirname(__file__), "rag_demo"))
load_dotenv()

from local_loader import load_txt_files
from full_chain import create_full_chain
from ensemble import ensemble_retriever_from_docs
from g_eval import judge
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.chat_message_histories import ChatMessageHistory

# === CONFIGURE DELAY BETWEEN CALLS (in seconds) ===
DELAY_BETWEEN_QUERIES = 4    # Adjust to fit your rate limits (4 seconds = max 15/minute)
DELAY_BETWEEN_JUDGE = 2      # Optional: Add a pause before each judge call if needed

# Step 1: Load text documents from the data folder
docs = load_txt_files("data")
print(f"[INFO] Loaded {len(docs)} documents.")

if not docs:
    raise ValueError("No documents loaded. Please check the data folder for .txt files.")

# Step 2: Create the embedding and retrieval chain
openai_api_key = os.getenv("OPENAI_API_KEY")
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")
retriever = ensemble_retriever_from_docs(docs, embeddings=embeddings)
chain = create_full_chain(
    retriever,
    openai_api_key=openai_api_key,
    chat_memory=ChatMessageHistory()
)

# Step 3: Load questions from queries.csv
df = pd.read_csv("data/queries.csv")
rows = []

for idx, q in enumerate(df["query"]):
    # Query the RAG chain
    print(f"[INFO] Processing query {idx+1}/{len(df)}: {q[:50]}...")
    response = chain.invoke(
        {"question": q, "chat_history": []},
        config={"configurable": {"session_id": "batch-gen"}}
    )
    answer = response.content

    # Retrieve context docs for this query
    context_docs = retriever.invoke(q)
    main_passage = context_docs[0].page_content if context_docs else ""
    context = " ".join([doc.page_content for doc in context_docs])[:1500]

    # Delay before LLM judge call to further avoid rate limits
    time.sleep(DELAY_BETWEEN_JUDGE)
    g_eval = judge(q, context_docs, answer)

    # Save results with required fields for open_rag_eval
    rows.append({
        "query": q,
        "generated_answer": answer,
        "passage_id": idx,
        "passage": main_passage,
        "context": context,
        "g_eval": g_eval
    })

    # Delay between each batch query to avoid OpenAI TPM/RPM limits
    print(f"[INFO] Sleeping for {DELAY_BETWEEN_QUERIES} seconds to avoid rate limit.")
    time.sleep(DELAY_BETWEEN_QUERIES)

os.makedirs("scored_results", exist_ok=True)
pd.DataFrame(rows).to_csv("scored_results/rag_results.csv", index=False)
print("✅ RAG results saved to scored_results/rag_results.csv")
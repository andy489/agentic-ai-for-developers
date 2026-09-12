import os
import signal
from dotenv import load_dotenv
load_dotenv()
os.environ["DEEPEVAL_TRACING"] = "false"

# deepeval's TraceManager calls signal.signal() at import time, which fails in
# Streamlit's non-main thread. Temporarily disable signal registration.
_real_signal = signal.signal
def _noop_signal(sig, handler):
    try:
        return _real_signal(sig, handler)
    except (ValueError, OSError):
        pass
signal.signal = _noop_signal

import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_openai import OpenAIEmbeddings

from ensemble import ensemble_retriever_from_docs
from full_chain import create_full_chain, ask_question
from local_loader import load_txt_files

from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, HallucinationMetric

from g_eval import judge

signal.signal = _real_signal  # restore after deepeval has loaded

st.set_page_config(page_title="LangChain & Streamlit RAG")
st.title("LangChain & Streamlit RAG")


def show_ui(qa, retriever, prompt_to_user="How may I help you?"):
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": prompt_to_user}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = ask_question(qa, prompt)

                try:
                    # 1. Retrieve the supporting documents used for the answer
                    docs = retriever.invoke(prompt)

                    # 2. Build a DeepEval test case for this prompt/response/context
                    test_case = LLMTestCase(
                        input=prompt,
                        actual_output=response.content,
                        context=[doc.page_content for doc in docs]
                    )

                    # 3. Instantiate desired DeepEval metrics (add/remove as needed)
                    metrics = [
                        AnswerRelevancyMetric(),
                        HallucinationMetric(threshold=0.5),
                    ]

                    # 4. Evaluate! (returns EvaluationResult with one TestResult per test_case)
                    results = evaluate(
                        test_cases=[test_case],
                        metrics=metrics
                    )

                    # 5. Extract metrics scores for display
                    test_result = results.test_results[0]
                    answer_relevancy_score = None
                    hallucination_score = None

                    for metric in test_result.metrics_data:
                        # NOTE: These names match the DeepEval metric classes
                        if metric.name.lower() == "answer relevancy":
                            answer_relevancy_score = metric.score
                        elif metric.name.lower() == "hallucination":
                            hallucination_score = metric.score

                    # Show DeepEval scores in sidebar
                    st.sidebar.subheader("DeepEval Scores")
                    if answer_relevancy_score is not None:
                        st.sidebar.metric("Relevance", f"{answer_relevancy_score:.2f}")
                    if hallucination_score is not None:
                        st.sidebar.metric("Hallucination", f"{hallucination_score:.2f}")

                except Exception as e:
                    st.sidebar.error(f"DeepEval failed: {e}")

                # --- Step 6: Run G-Eval to score the answer using GPT-4o ---
                try:
                    # Run G-Eval using GPT-4o
                    judge_output = judge(str(prompt), docs, response.content)

                    # --- Step 7: Display G-Eval score and rationale in the sidebar ---
                    st.sidebar.subheader("LLM-as-a-Judge")
                    st.sidebar.write(judge_output)

                except Exception as e:
                    st.sidebar.error(f"G-Eval failed: {e}")

                st.markdown(response.content)
        message = {"role": "assistant", "content": response.content}
        st.session_state.messages.append(message)


@st.cache_resource
def get_retriever(openai_api_key=None):
    docs = load_txt_files()
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model="text-embedding-3-small")
    return ensemble_retriever_from_docs(docs, embeddings=embeddings)


def get_chain(openai_api_key=None, huggingfacehub_api_token=None):
    ensemble_retriever = get_retriever(openai_api_key=openai_api_key)
    chain = create_full_chain(ensemble_retriever,
                              openai_api_key=openai_api_key,
                              chat_memory=StreamlitChatMessageHistory(key="langchain_messages"))
    return chain


def get_secret_or_input(secret_key, secret_name, info_link=None):
    try:
        has_secret = secret_key in st.secrets
    except Exception:
        has_secret = False
    if has_secret:
        st.write("Found %s secret" % secret_key)
        secret_value = st.secrets[secret_key]
    else:
        st.write(f"Please provide your {secret_name}")
        secret_value = st.text_input(secret_name, key=f"input_{secret_key}", type="password")
        if secret_value:
            st.session_state[secret_key] = secret_value
        if info_link:
            st.markdown(f"[Get an {secret_name}]({info_link})")
    return secret_value


def run():
    ready = True

    openai_api_key = st.session_state.get("OPENAI_API_KEY")
    huggingfacehub_api_token = st.session_state.get("HUGGINGFACEHUB_API_TOKEN")

    with st.sidebar:
        if not openai_api_key:
            openai_api_key = get_secret_or_input('OPENAI_API_KEY', "OpenAI API key",
                                                 info_link="https://platform.openai.com/account/api-keys")
        if not huggingfacehub_api_token:
            huggingfacehub_api_token = get_secret_or_input('HUGGINGFACEHUB_API_TOKEN', "HuggingFace Hub API Token",
                                                           info_link="https://huggingface.co/docs/huggingface_hub/main/en/quick-start#authentication")

    if not openai_api_key:
        st.warning("Missing OPENAI_API_KEY")
        ready = False
    if not huggingfacehub_api_token:
        st.warning("Missing HUGGINGFACEHUB_API_TOKEN")
        ready = False

    if ready:
        retriever = get_retriever(openai_api_key=openai_api_key)
        chain = get_chain(openai_api_key=openai_api_key, huggingfacehub_api_token=huggingfacehub_api_token)
        st.subheader("Ask me questions about this week's meal plan")
        show_ui(chain, retriever, "What would you like to know?")
    else:
        st.stop()


run()

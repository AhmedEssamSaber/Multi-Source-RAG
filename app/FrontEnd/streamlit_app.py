import streamlit as st
import requests
import uuid

st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.title("🤖 RAG Chatbot")

# SESSION STATE INIT
if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "history" not in st.session_state:
    st.session_state.history = []

# CLEAN FUNCTION (IMPORTANT)
def clean_answer(text):
    unwanted = [
        "Based on the context provided,",
        "Based on the provided context,",
        "Based on the context,",
        "According to the context,"
    ]

    for u in unwanted:
        text = text.replace(u, "")

    return text.strip()

# SIDEBAR
st.sidebar.title("🧠 Chat History")

# show history
for i, item in enumerate(st.session_state.history[::-1]):
    if st.sidebar.button(item["question"][:40], key=i):
        st.session_state.messages = item["messages"]

st.sidebar.divider()

st.sidebar.write("Session ID:")
st.sidebar.code(st.session_state.session_id)

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = []

# DISPLAY CHAT
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg["role"] == "assistant":
            st.caption(f"📚 Source: {msg['source']}")

# INPUT
question = st.chat_input("Ask anything...")

if question:

    # save user msg
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={
                    "question": question,
                    "session_id": st.session_state.session_id
                }
            )

            if response.status_code == 200:
                data = response.json()

                answer = clean_answer(data["answer"])  
                source = data["source"]

                st.markdown(answer)
                st.caption(f"📚 Source: {source}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "source": source
                })

                # save in history
                st.session_state.history.append({
                    "question": question,
                    "messages": st.session_state.messages.copy()
                })

            else:
                st.error("API Error")


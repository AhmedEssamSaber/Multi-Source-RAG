import streamlit as st
import requests

st.set_page_config(page_title="RAG Chatbot", layout="wide")

st.title("🤖 RAG Chatbot")


# SESSION STATE INIT

if "history" not in st.session_state:
    st.session_state.history = []


# SIDEBAR (HISTORY)

st.sidebar.title("🧠 Previous Questions")

for i, item in enumerate(st.session_state.history):
    if st.sidebar.button(item["question"], key=i):
        st.session_state.selected = item


# MAIN INPUT

question = st.text_input("Enter your question:")

if st.button("Ask"):

    if not question:
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):

            response = requests.post(
                "http://127.0.0.1:8000/chat",
                json={"question": question}
            )

            if response.status_code == 200:
                data = response.json()

                answer = data["answer"]
                source = data["source"]

                
                st.session_state.history.append({
                    "question": question,
                    "answer": answer,
                    "source": source
                })

                st.session_state.selected = {
                    "question": question,
                    "answer": answer,
                    "source": source
                }

            else:
                st.error("Error connecting to API")


# DISPLAY SELECTED CHAT

if "selected" in st.session_state:

    st.subheader("📝 Question")
    st.write(st.session_state.selected["question"])

    st.subheader("💡 Answer")
    st.write(st.session_state.selected["answer"])

    st.info(f"Source: {st.session_state.selected['source']}")
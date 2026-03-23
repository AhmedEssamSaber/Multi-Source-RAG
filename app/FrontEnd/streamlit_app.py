import streamlit as st
import requests

#  Page Config
st.set_page_config(
    page_title="AI Knowledge Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Knowledge Chatbot")

# Input
question = st.text_input("Ask a question")

# Button
if st.button("Send"):

    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking... 🤔"):

            try:
                response = requests.post(
                    "http://localhost:8000/chat",
                    json={"question": question}
                )

                data = response.json()

                # Source
                st.markdown(f"### 🧠 Source: `{data['source']}`")

                # Answer
                st.markdown("### 🤖 Answer:")
                st.write(data.get("answer", "No answer returned."))

            except Exception as e:
                st.error("Failed to connect to backend.")
                st.text(str(e))
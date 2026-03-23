import streamlit as st
import requests

st.title("AI Knowledge Chatbot")

question = st.text_input("Ask a question")

if st.button("Send"):

    response = requests.post(
        "http://localhost:8000/chat",
        json={"question": question}
    )

    st.write(response.json()["answer"])

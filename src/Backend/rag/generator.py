import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))


def generate_answer(question, context):

    prompt = f"""
Use the context to answer the question.

Context:
{context}

Question:
{question}
"""

    response = co.chat(message=prompt)

    return response.text

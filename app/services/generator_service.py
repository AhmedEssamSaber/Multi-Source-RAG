import cohere
import os
from dotenv import load_dotenv

load_dotenv()


class GeneratorService:

    def __init__(self):
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

    def generate(self, question, context):

        prompt = f"""
Use the context to answer the question.

Context:
{context}

Question:
{question}
"""

        response = self.co.chat(message=prompt)

        return response.text
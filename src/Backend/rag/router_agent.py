import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))


def choose_source(question):

    prompt = f"""
        You are a router agent.

        Decide which source should answer the question.

        Sources:
        - pdf: research papers
        - wiki: general knowledge
        - docs: technical documentation

        Return only one word:
        pdf
        wiki
        docs

        Question:
            {question}
    """

    response = co.chat(message=prompt)

    source = response.text.strip().lower()

    return source
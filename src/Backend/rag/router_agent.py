import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

VALID_SOURCES = {"pdf", "wiki", "docs"}

def route(question: str) -> str:
    """
    Routes a question to the best knowledge source using the LLM.
    Returns one of: 'pdf', 'wiki', 'docs'
    """
    prompt = f"""You are an intelligent routing agent.

Choose the BEST source for answering the question.

Sources:
- pdf   → research papers, transformers, attention, deep learning architectures
- wiki  → general explanations and definitions
- docs  → programming, tutorials, libraries (PyTorch, FastAPI)

Rules:
- Return ONLY one word: pdf OR wiki OR docs
- No explanation, no punctuation

Question: {question}
"""
    try:
        response = co.chat(
            model="command-r7b-12-2024",
            message=prompt,
            temperature=0
        )

        output = response.text.strip().lower()

        # Extract the first valid token found in the response
        for token in output.split():
            if token in VALID_SOURCES:
                return token

        # Soft fallback if LLM returns something unexpected
        return "docs"

    except Exception as e:
        print("Router error:", e)
        return "docs"
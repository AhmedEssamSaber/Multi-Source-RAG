import cohere
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))


def llm_route(question):
    prompt = f"""
You are an intelligent routing agent.

Choose the BEST source for answering the question.

Sources:
- pdf → research papers, transformers, attention, deep learning architectures
- wiki → general explanations and definitions
- docs → programming, tutorials, libraries (PyTorch, FastAPI)

Rules:
- Return ONLY one word: pdf OR wiki OR docs
- No explanation

Question:
{question}
"""

    try:
        response = co.chat(
            model="command-r",
            message=prompt,
            temperature=0
        )

        output = response.text.strip().lower()

        if "pdf" in output:
            return "pdf"
        elif "wiki" in output:
            return "wiki"
        elif "docs" in output:
            return "docs"
        else:
            return "docs"

    except Exception as e:
        print("LLM Router error:", e)
        return "docs"


def choose_source(question):
    q = question.lower()

    # RULES (High precision)
    if "attention" in q or "transformer" in q:
        return "pdf"

    if "paper" in q or "research" in q:
        return "pdf"

    if "what is" in q or "define" in q:
        return "wiki"

    if "how to" in q or "use" in q or "code" in q:
        return "docs"

    # fallback to LLM
    return llm_route(question)
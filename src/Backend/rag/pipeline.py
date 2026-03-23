from src.Backend.rag.router_agent import choose_source
from src.Backend.rag.retriever import retrieve
from src.Backend.rag.generator import generate_answer


def rag_pipeline(question):

    source = choose_source(question)

    docs = retrieve(question)

    context = "\n".join(docs)

    answer = generate_answer(question, context)

    return answer
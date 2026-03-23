from src.Backend.rag.router_agent import choose_source
from src.Backend.rag.retriever import retrieve
from src.Backend.rag.generator import generate_answer


def rag_pipeline(question):

    # Step 1: choose source
    source = choose_source(question)
    print(f"Selected source: {source}")

    # Step 2: retrieve
    docs = retrieve(question, source=source)

    # Step 3: fallback 
    if not docs:
        print("Fallback to other sources...")

        fallback_sources = ["pdf", "wiki", "docs"]

        for src in fallback_sources:
            if src == source:
                continue

            docs = retrieve(question, source=src)

            if docs:
                print(f"Fallback success: {src}")
                source = src
                break

    if not docs:
        return "No relevant documents found."

    # Step 4: build context
    context = "\n".join(docs)

    # Step 5: generate answer
    answer = generate_answer(question, context)

    return source, answer
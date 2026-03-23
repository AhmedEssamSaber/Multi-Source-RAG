from src.Backend.rag.router_agent import route  # updated import
from src.Backend.rag.retriever import retrieve
from src.Backend.rag.generator import generate_answer


def rag_pipeline(question: str) -> tuple[str, str] | str:

    # Step 1: Route to best source
    source = route(question)
    print(f"Selected source: {source}")

    # Step 2: Retrieve from selected source
    docs = retrieve(question, source=source)

    # Step 3: Fallback to remaining sources if nothing found
    if not docs:
        print("Primary source empty, trying fallbacks...")

        FALLBACK_ORDER = {
            "pdf":  ["wiki", "docs"],
            "wiki": ["pdf",  "docs"],
            "docs": ["wiki", "pdf"],
        }

        for fallback in FALLBACK_ORDER[source]:
            if fallback == source:
                continue

            docs = retrieve(question, source=fallback)

            if docs:
                print(f"Fallback success: {fallback}")
                source = fallback
                break

    if not docs:
        return "No relevant documents found."

    # Step 4: Build context
    context = "\n".join(docs)

    # Step 5: Generate answer
    answer = generate_answer(question, context)

    return source, answer
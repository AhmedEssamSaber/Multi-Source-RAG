from app.services.retriever_service import RetrieverService
from app.services.generator_service import GeneratorService

from app.models.repositories.query_log_repository import QueryLogRepository
from app.models.db.database import AsyncSessionLocal


class RAGService:

    def __init__(self):
        self.retriever = RetrieverService()
        self.generator = GeneratorService()

    # SIMPLE RULE-BASED ROUTING
    def decide_sources(self, question: str):
        q = question.lower()

        if any(w in q for w in ["pytorch", "tensorflow", "api", "install", "code"]):
            return ["docs"]

        if any(w in q for w in ["paper", "research", "transformer", "attention"]):
            return ["pdf"]

        if any(w in q for w in ["what is", "define", "explain"]):
            return ["wiki"]

        return ["docs", "wiki"]


    def clean_answer(self, text):
        bad_phrases = [
            "based on the context",
            "based on the provided context",
            "according to the context"
        ]

        text_lower = text.lower()

        for phrase in bad_phrases:
            if text_lower.startswith(phrase):
                text = text[len(phrase):]

        return text.strip()

    async def run(self, question: str, session_id: str):

        # GET HISTORY 
        async with AsyncSessionLocal() as session:
            log_repo = QueryLogRepository(session)

            try:
                history = await log_repo.get_last_messages(
                    session_id=session_id,
                    limit=3
                )
            except:
                history = []

        history_text = "\n".join([
            f"User: {h.question}\nAssistant: {h.answer}"
            for h in history
        ])

        # RETRIEVE
        sources = self.decide_sources(question)

        all_results = []

        for src in sources:
            docs = self.retriever.retrieve_from_source(question, src, k=5)

            for d in docs:
                all_results.append({
                    "content": str(d),   
                    "source": src
                })

        # FALLBACK
        if not all_results:
            docs = self.retriever.retrieve_all(question)

            for d in docs:
                all_results.append(d)

        # GENERATION
        if not all_results:
            answer = "No relevant documents found."
            source = "none"
        else:
            context = "\n".join([r["content"] for r in all_results[:5]])

            print("\= DEBUG CONTEXT=\n")
            print(context)
            print("\=======\n")

            answer = self.generator.generate(
                question=question,
                context=context
            )

            answer = self.clean_answer(answer)

            source = list(set([r["source"] for r in all_results]))

        # SAVE
        async with AsyncSessionLocal() as session:
            log_repo = QueryLogRepository(session)

            await log_repo.create_log(
                question=question,
                answer=answer,
                source=",".join(source) if isinstance(source, list) else source,
                session_id=session_id
            )

            await session.commit()

        return source, answer

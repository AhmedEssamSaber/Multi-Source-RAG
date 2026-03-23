from app.services.router_service import RouterService
from app.services.retriever_service import RetrieverService
from app.services.generator_service import GeneratorService
from app.core.enums import SourceType


class RAGService:

    def __init__(self):
        self.router = RouterService()
        self.retriever = RetrieverService()
        self.generator = GeneratorService()

    def run(self, question: str):

        source = self.router.route(question)

        docs = self.retriever.retrieve(question, source)

        if not docs:

            fallback_map = {
                SourceType.PDF:  [SourceType.WIKI, SourceType.DOCS],
                SourceType.WIKI: [SourceType.PDF,  SourceType.DOCS],
                SourceType.DOCS: [SourceType.WIKI, SourceType.PDF],
            }

            for fallback in fallback_map[source]:

                docs = self.retriever.retrieve(question, fallback)

                if docs:
                    source = fallback
                    break

        if not docs:
            return source.value, "No documents found."

        context = "\n".join(docs)

        answer = self.generator.generate(question, context)

        return source.value, answer
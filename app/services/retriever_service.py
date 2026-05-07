import os
import faiss
import pickle
import numpy as np

from app.models.embedding_model import EmbeddingModel


class RetrieverService:

    def __init__(self):
        self.embedder = EmbeddingModel()

        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.vector_store = os.path.join(self.base_dir, "vector_store")

        self.sources = ["docs", "wiki", "pdf"]

    def retrieve_all(self, query, k_per_source=3, final_k=5):

        all_docs = []

        for source in self.sources:
            docs = self.retrieve_from_source(query, source, k_per_source)

            for d in docs:
                all_docs.append({
                    "content": str(d),
                    "source": source
                })

        ranked_docs = self.rerank(query, all_docs)

        return ranked_docs[:final_k]

    def retrieve_from_source(self, query, source, k=5):

        index_path = os.path.join(
            self.vector_store, f"{source}.faiss"
        )

        texts_path = os.path.join(
            self.vector_store, f"{source}_texts.pkl"
        )

        if not os.path.exists(index_path):
            return []

        index = faiss.read_index(index_path)

        with open(texts_path, "rb") as f:
            texts = pickle.load(f)

        query_embedding = self.embedder.embed([query])[0]

        D, I = index.search(
            np.array([query_embedding]).astype("float32"),
            int(k)
        )

        docs = [texts[i] for i in I[0] if i < len(texts)]

        return docs

    def rerank(self, query, docs):

        query_emb = self.embedder.embed([query])[0]

        doc_texts = [d["content"] for d in docs]
        doc_embeddings = self.embedder.embed(doc_texts)

        scored_docs = []

        for d, doc_emb in zip(docs, doc_embeddings):

            score = self.cosine_similarity(query_emb, doc_emb)

            scored_docs.append({
                "content": d["content"],
                "source": d["source"],
                "score": score
            })

        ranked = sorted(
            scored_docs,
            key=lambda x: x["score"],
            reverse=True
        )

        return ranked

    def cosine_similarity(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-10)

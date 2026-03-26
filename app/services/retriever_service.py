import os
import faiss
import pickle
import numpy as np

from app.models.embedding_model import EmbeddingModel


class RetrieverService:

    def __init__(self):
        self.embedder = EmbeddingModel()

        # path -> app/
        self.base_dir = os.path.dirname(os.path.dirname(__file__))

        # app/vector_store
        self.vector_store = os.path.join(self.base_dir, "vector_store")

    # MAIN RETRIEVE FUNCTION
    def retrieve(self, query, source, k=5):

        index_path = os.path.join(
            self.vector_store, f"{source.value}.faiss"
        )

        texts_path = os.path.join(
            self.vector_store, f"{source.value}_texts.pkl"
        )

        if not os.path.exists(index_path):
            return []

        # load FAISS index
        index = faiss.read_index(index_path)

        # load chunks
        with open(texts_path, "rb") as f:
            texts = pickle.load(f)

        # embed query
        query_embedding = self.embedder.embed([query])[0]

        # search Top-K
        D, I = index.search(
            np.array([query_embedding]).astype("float32"),
            k
        )

        # get docs
        docs = [texts[i] for i in I[0] if i < len(texts)]

        # rerank
        docs = self.rerank(query, docs)

        return docs

    # RERANK FUNCTION
    def rerank(self, query, docs):

        scored_docs = []

        for doc in docs:
            score = self.simple_score(query, doc)
            scored_docs.append((doc, score))

        ranked = sorted(
            scored_docs,
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, _ in ranked[:3]]

    # SIMPLE SCORING
    def simple_score(self, query, doc):

        query_words = set(query.lower().split())
        doc_words = set(doc.lower().split())

        return len(query_words.intersection(doc_words))
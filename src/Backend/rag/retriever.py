import faiss
import numpy as np
import pickle
import os

from src.Backend.rag.embeddings import embed_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
VECTOR_STORE = os.path.join(BASE_DIR, "vector_store")


def retrieve(query, source, k=5):

    index_path = os.path.join(VECTOR_STORE, f"{source}.faiss")
    texts_path = os.path.join(VECTOR_STORE, f"{source}_texts.pkl")

    if not os.path.exists(index_path):
        print(f"Index not found: {source}")
        return []

    if not os.path.exists(texts_path):
        print(f"Texts not found: {source}")
        return []

    index = faiss.read_index(index_path)

    with open(texts_path, "rb") as f:
        documents = pickle.load(f)

    query_embedding = embed_text([query])[0]

    D, I = index.search(
        np.array([query_embedding]).astype("float32"),
        k
    )

    results = []
    for i in I[0]:
        if 0 <= i < len(documents):
            results.append(documents[i])

    return results
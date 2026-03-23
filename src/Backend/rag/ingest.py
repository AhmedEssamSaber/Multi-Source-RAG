import os
import faiss
import numpy as np
import pickle

from src.Backend.rag.loaders import load_pdf, load_txt
from src.Backend.rag.chunking import chunk_text
from src.Backend.rag.embeddings import embed_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")
print("Data path:", DATA_PATH)
VECTOR_STORE = os.path.join(BASE_DIR, "vector_store")

def load_documents(source):
    texts = []

    source_path = os.path.join(DATA_PATH, source)

    print(f"\n Scanning folder: {source_path}")

    for root, dirs, files in os.walk(source_path):
        print("Files found:", files)  

        for file in files:
            path = os.path.join(root, file)
            print("Processing:", path)

            if file.lower().endswith(".pdf"):
                text = load_pdf(path)
            elif file.lower().endswith(".txt"):
                text = load_txt(path)
            else:
                print("Skipped (not txt/pdf):", file)
                continue

            print("Text length:", len(text) if text else 0)

            if not text:
                continue

            chunks = chunk_text(text)
            print("Chunks:", len(chunks))

            texts.extend(chunks)

    return texts

def ingest():
    os.makedirs(VECTOR_STORE, exist_ok=True)

    sources = ["docs", "pdf", "wiki"]

    for source in sources:
        print(f"\n Processing source: {source}")

        texts = load_documents(source)

        if not texts:
            print(f"No documents found in {source}")
            continue

        print(f"Documents count: {len(texts)}")

        embeddings = embed_text(texts)

        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)

        index.add(np.array(embeddings).astype("float32"))

        # save index
        faiss.write_index(index, os.path.join(VECTOR_STORE, f"{source}.faiss"))

        # save texts
        with open(os.path.join(VECTOR_STORE, f"{source}_texts.pkl"), "wb") as f:
            pickle.dump(texts, f)

        print(f"Saved {source} index")

    print("\n Multi-source ingestion completed!")


if __name__ == "__main__":
    ingest()
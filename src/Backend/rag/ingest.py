import os
import faiss
import numpy as np

from src.Backend.rag.loaders import load_pdf, load_txt
from src.Backend.rag.chunking import chunk_text
from src.Backend.rag.embeddings import embed_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data")

documents = []

def load_documents():
    texts = []
    for root, dirs, files in os.walk(DATA_PATH):
        for file in files:
            path = os.path.join(root, file)
            if file.endswith(".pdf"):
                text = load_pdf(path)
            elif file.endswith(".txt"):
                text = load_txt(path)
            else:
                continue
            if not text:
                continue
            chunks = chunk_text(text)
            texts.extend(chunks)
    return texts

def ingest():
    global documents
    documents = load_documents()
    print("Documents count:", len(documents))
    print("Sample:", documents[:2])
    embeddings = embed_text(documents)
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings).astype("float32"))
    os.makedirs("vector_store", exist_ok=True)
    faiss.write_index(index, "vector_store/index.faiss")
    print("Ingestion completed")

if __name__ == "__main__":
    ingest()
    print("Docs files:", os.listdir(os.path.join(DATA_PATH, "docs")))
    print("PDF files:", os.listdir(os.path.join(DATA_PATH, "pdf")))
    print("Wiki files:", os.listdir(os.path.join(DATA_PATH, "wiki")))
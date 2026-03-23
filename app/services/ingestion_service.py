import os
import faiss
import numpy as np
import pickle

from app.models.loader_model import DocumentLoader
from app.models.chunking_model import TextChunker
from app.models.embedding_model import EmbeddingModel


class IngestionService:

    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self.embedder = EmbeddingModel()

        self.base_dir = os.path.abspath(".")
        self.data_path = os.path.join(self.base_dir, "data")
        self.vector_store = os.path.join(self.base_dir, "vector_store")

    def load_documents(self, source):

        texts = []
        source_path = os.path.join(self.data_path, source)

        print(f"\n Scanning: {source_path}")

        for root, _, files in os.walk(source_path):

            for file in files:
                path = os.path.join(root, file)

                if file.lower().endswith(".pdf"):
                    text = self.loader.load_pdf(path)

                elif file.lower().endswith(".txt"):
                    text = self.loader.load_txt(path)

                else:
                    continue

                if not text:
                    continue

                chunks = self.chunker.chunk(text)

                texts.extend(chunks)

        return texts

    def ingest(self):

        os.makedirs(self.vector_store, exist_ok=True)

        sources = ["docs", "pdf", "wiki"]

        for source in sources:

            print(f"\n Processing: {source}")

            texts = self.load_documents(source)

            if not texts:
                print(f"No docs in {source}")
                continue

            embeddings = self.embedder.embed(texts)

            dimension = len(embeddings[0])

            index = faiss.IndexFlatL2(dimension)
            index.add(np.array(embeddings).astype("float32"))

            # save index
            faiss.write_index(
                index,
                os.path.join(self.vector_store, f"{source}.faiss")
            )

            # save texts
            with open(
                os.path.join(self.vector_store, f"{source}_texts.pkl"),
                "wb"
            ) as f:
                pickle.dump(texts, f)

            print(f"✅ Saved {source}")

        print("\n Ingestion Done")
import os
import faiss
import numpy as np
import pickle
import re

from app.models.loader_model import DocumentLoader
from app.models.chunking_model import TextChunker
from app.models.embedding_model import EmbeddingModel

from app.models.db.database import AsyncSessionLocal

from app.models.repositories.document_repository import DocumentRepository
from app.models.repositories.chunk_repository import ChunkRepository
from app.models.repositories.embedding_repository import EmbeddingRepository


# CLEAN FUNCTION 
def clean_text(text: str) -> str:
    if not text:
        return ""

    # remove null bytes
    text = text.replace("\x00", "")

    # remove weird unicode chars
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


class IngestionService:

    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self.embedder = EmbeddingModel()

        # (fix path)
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_path = os.path.join(self.base_dir, "data")
        self.vector_store = os.path.join(self.base_dir, "vector_store")

    
    # LOAD DOCUMENTS
    def load_documents(self, source):

        texts = []
        source_path = os.path.join(self.data_path, source)

        print(f"PATH: {source_path}")

        for root, _, files in os.walk(source_path):
            print(f"FILES FOUND: {files}")

            for file in files:

                path = os.path.join(root, file)
                print(f"Reading file: {path}")

                # load file
                if file.endswith(".pdf"):
                    text = self.loader.load_pdf(path)
                else:
                    text = self.loader.load_txt(path)

                if not text:
                    print(f"Empty file: {file}")
                    continue

                # CLEAN TEXT BEFORE CHUNKING
                text = clean_text(text)

                chunks = self.chunker.chunk(text)

                texts.extend([(file, chunk) for chunk in chunks])

        print(f"TOTAL CHUNKS: {len(texts)}")
        return texts

    
    # INGEST
    async def ingest(self):

        os.makedirs(self.vector_store, exist_ok=True)

        async with AsyncSessionLocal() as session:

            doc_repo = DocumentRepository(session)
            chunk_repo = ChunkRepository(session)
            emb_repo = EmbeddingRepository(session)

            sources = ["docs", "pdf", "wiki"]

            for source in sources:

                print(f"\n Processing: {source}")

                texts = self.load_documents(source)

                if not texts:
                    print("No data found")
                    continue

                file_names = [t[0] for t in texts]
                chunks = [t[1] for t in texts]

                # EMBEDDINGS
                embeddings = self.embedder.embed(chunks)

                dimension = len(embeddings[0])

                index = faiss.IndexFlatL2(dimension)
                index.add(np.array(embeddings).astype("float32"))

                # save FAISS
                faiss.write_index(
                    index,
                    os.path.join(self.vector_store, f"{source}.faiss")
                )

                with open(
                    os.path.join(self.vector_store, f"{source}_texts.pkl"),
                    "wb"
                ) as f:
                    pickle.dump(chunks, f)

                print(f"FAISS saved for {source}")

                # SAVE TO DATABASE
                current_file = None
                doc = None

                for file_name, chunk_text, emb in zip(file_names, chunks, embeddings):

                    # new document
                    if file_name != current_file:
                        doc = await doc_repo.create_document(source, file_name)
                        doc.content = clean_text(chunk_text)
                        current_file = file_name

                    # clean chunk
                    clean_chunk = clean_text(chunk_text)

                    # create chunk
                    chunk_obj = await chunk_repo.create_chunk(
                        doc.id,
                        clean_chunk
                    )

                    # create embedding
                    await emb_repo.create_embedding(
                        chunk_obj.id,
                        emb
                    )

            # IMPORTANT
            await session.commit()

        print("\n Hybrid Ingestion Done")

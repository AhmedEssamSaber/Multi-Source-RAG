import cohere 
import os
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def embed_text(texts):
    if not texts:
        raise ValueError("texts list is empty")

    response = co.embed(
        texts=texts,
        model="embed-english-v3.0",
        input_type="search_document"
    )

    if not response.embeddings:
        raise ValueError("Empty embeddings returned from Cohere")

    return response.embeddings
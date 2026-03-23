import cohere
import os
from dotenv import load_dotenv

load_dotenv()


class EmbeddingModel:

    def __init__(self):
        self.co = cohere.Client(os.getenv("COHERE_API_KEY"))

    def embed(self, texts, input_type="search_document"):  

        if not texts:
            raise ValueError("texts list is empty")

        response = self.co.embed(
            texts=texts,
            model="embed-english-v3.0",
            input_type=input_type   
        )

        return response.embeddings
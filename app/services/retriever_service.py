# import faiss
# import numpy as np
# import pickle
# import os

# from app.models.embedding_model import EmbeddingModel
# from app.core.enums import SourceType


# class RetrieverService:

#     def __init__(self):
#         self.embedder = EmbeddingModel()
#         self.base_dir = os.path.abspath(".")
#         self.vector_store = os.path.join(self.base_dir, "vector_store")

#     def retrieve(self, query: str, source: SourceType, k=5):

#         source_name = source.value  

#         index_path = os.path.join(self.vector_store, f"{source_name}.faiss")
#         texts_path = os.path.join(self.vector_store, f"{source_name}_texts.pkl")

#         if not os.path.exists(index_path):
#             return []

#         index = faiss.read_index(index_path)

#         with open(texts_path, "rb") as f:
#             documents = pickle.load(f)

#         query_embedding = self.embedder.embed([query])[0]

#         D, I = index.search(
#             np.array([query_embedding]).astype("float32"),
#             k
#         )

#         print("📊 Documents loaded:", len(documents))

#         return [documents[i] for i in I[0] if i < len(documents)]

import faiss
import numpy as np
import pickle
import os

from app.models.embedding_model import EmbeddingModel
from app.core.enums import SourceType


class RetrieverService:

    def __init__(self):
        self.embedder = EmbeddingModel()

        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        self.vector_store = os.path.join(BASE_DIR, "vector_store")

    def retrieve(self, query: str, source: SourceType, k=10):

        source_name = source.value

        index_path = os.path.join(self.vector_store, f"{source_name}.faiss")
        texts_path = os.path.join(self.vector_store, f"{source_name}_texts.pkl")

        if not os.path.exists(index_path):
            print(f"Index not found: {index_path}")
            return []

        if not os.path.exists(texts_path):
            print(f"Texts not found: {texts_path}")
            return []

        index = faiss.read_index(index_path)

        with open(texts_path, "rb") as f:
            documents = pickle.load(f)

        # print("Documents loaded:", len(documents))
        # print("Index size:", index.ntotal)

    
        query_embedding = self.embedder.embed(
            [query],
            input_type="search_query"
        )[0]

        D, I = index.search(
            np.array([query_embedding]).astype("float32"),
            k
        )

        # print("Indices:", I)
        # print("Distances:", D)

        results = []
        for i in I[0]:
            if 0 <= i < len(documents):
                results.append(documents[i])

        return results
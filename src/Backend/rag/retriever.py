import faiss
import numpy as np

from src.Backend.rag.embeddings import embed_text
from src.Backend.rag.ingest import documents

index = faiss.read_index("vector_store/index.faiss")


# def retrieve(query, k=3):

#     query_embedding = embed_text([query])[0]

#     D, I = index.search(
#         np.array([query_embedding]).astype("float32"),
#         k
#     )

#     results = [documents[i] for i in I[0]]

#     return results
# import numpy as np
# import faiss

def retrieve(question, k=5):
    
    if not documents:
        print("⚠️ Documents list is empty!")
        return []

    
    question_embedding = embed_text(question)

    
    I, D = index.search(np.array([question_embedding], dtype='float32'), k)
    
   
    valid_indices = [i for i in I[0] if 0 <= i < len(documents)]
    
    
    if not valid_indices:
        print("⚠️ No matching documents found!")
        return []

    
    results = [documents[i] for i in valid_indices]

    return results

def embed_text(text):
    
    raise NotImplementedError("Implement embedding for the text using your model")
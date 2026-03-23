from fastapi import APIRouter
from pydantic import BaseModel

from src.Backend.rag.retriever import retrieve
from src.Backend.rag.generator import generate_answer
from src.Backend.rag.pipeline import rag_pipeline


router = APIRouter()


class Query(BaseModel):
    question: str


@router.post("/chat")
def chat(query: Query):

    answer = rag_pipeline(query.question)

    return {"answer": answer}

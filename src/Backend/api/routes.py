from fastapi import APIRouter
from pydantic import BaseModel

from src.Backend.rag.retriever import retrieve
from src.Backend.rag.generator import generate_answer
from src.Backend.rag.pipeline import rag_pipeline


router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
def chat(request: ChatRequest):

    source, answer = rag_pipeline(request.question)

    return {
        "answer": answer,
        "source": source
    }

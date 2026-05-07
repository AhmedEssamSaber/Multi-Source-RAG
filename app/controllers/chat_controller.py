from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import RAGService

router = APIRouter()
rag = RAGService()


class ChatRequest(BaseModel):
    question: str
    session_id: str


@router.post("/chat")
async def chat(request: ChatRequest):

    source, answer = await rag.run(
        question=request.question,
        session_id=request.session_id
    )

    return {
        "answer": answer,
        "source": source
    }

@router.get("/")
async def root():
    return {"message": "Welcome to the Multi-Source RAG API!"}
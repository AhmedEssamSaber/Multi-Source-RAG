from fastapi import APIRouter
from pydantic import BaseModel

from app.services.rag_service import RAGService
from app.core.enums import SourceType

router = APIRouter()
rag = RAGService()


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    source: str


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):

    source, answer = await rag.run(req.question)

    return {
        "answer": answer,
        "source": source
    }

@router.get("/sources")
async def get_sources():
    return [s.value for s in SourceType]
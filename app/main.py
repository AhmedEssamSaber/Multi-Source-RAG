from fastapi import FastAPI
from app.controllers.chat_controller import router

app = FastAPI(title="Multi Source Agentic RAG")

app.include_router(router)
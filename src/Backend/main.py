from fastapi import FastAPI
from src.Backend.api.routes import router

app = FastAPI(title="Multi Source RAG Chatbot")

app.include_router(router)

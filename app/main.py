from fastapi import FastAPI
from app.controllers.chat_controller import router

from app.models.db.database import init_db

app = FastAPI(title="Multi Source Agentic RAG")

app.include_router(router)


@app.on_event("startup")
async def startup():
    print("🚀 STARTUP EVENT CALLED")
    await init_db()
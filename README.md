## Multi-Source Agentic RAG System

This project is an end-to-end Retrieval-Augmented Generation (RAG) system that integrates multiple data sources and uses vector search + LLMs to generate accurate answers.

# Overview
The system follows an Agentic RAG pipeline:
- Ingest data from multiple sources (Docs, PDF, Wiki)
- Split into chunks
- Generate embeddings
- Store in PostgreSQL + Vector Store
- Retrieve relevant chunks using FAISS
- Generate answers using LLM
- Log queries for monitoring

# Installation

```bash
git clone https://github.com/your-username/multi-source-rag.git 
cd multi-source-rag
```

# install the Requirements
```bash
pip install -r requirements.txt
```

# Usage
- Run Ingestion
```bash
python -m app.scripts.run_ingest
```

- Run Backend
```bash
uvicorn app.main:app --reload
```

- Run Frontend
```bash
streamlit run app/FrontEnd/streamlit_app.py
```

# Project Structure

```bash
app/
├── controllers/
│   ├── chat_controller.py
│
├── core/
│   ├── config.py
│   ├── enums.py
│
├── data/
│   ├── docs/
│   ├── pdf/
│   └── wiki/
│
├── FrontEnd/
│   └── streamlit_app.py
│
├── models/
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── database.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   ├── document_repository.py
│   │   ├── chunk_repository.py
│   │   ├── embedding_repository.py
│   │   └── query_log_repository.py
│   │
│   ├── loader_model.py
│   ├── chunking_model.py
│   ├── embedding_model.py
│   └── wiki_model.py
│
├── scripts/
│   ├── download_wiki.py
│   └── run_ingest.py
│
├── services/
│   ├── ingestion_service.py
│   ├── retriever_service.py
│   ├── generator_service.py
│   ├── router_service.py
│   └── rag_service.py
│
docker/
│   ├── docker-compose.yml
│   ├── .env.example
│   └── .gitignore
│
.env.example
.gitignore
LICENCE
requirements.txt
README.md
```


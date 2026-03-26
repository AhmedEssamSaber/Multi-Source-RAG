## Multi-Source Agentic RAG System

This project is an end-to-end Retrieval-Augmented Generation (RAG) system that integrates multiple data sources and uses vector search + LLMs to generate accurate answers.


# system architecture diagram
```mermaid
graph TD

    USER((User))
    API[FastAPI]

    USER --> API

    subgraph RAG_System
        RAG[RAG Service]
        ROUTER[Router]
        RETRIEVER[Retriever]
        GENERATOR[Generator]

        RAG --> ROUTER
        RAG --> RETRIEVER
        RAG --> GENERATOR
    end

    API --> RAG

    subgraph Data
        DOCS[Docs]
        PDF[PDF]
        WIKI[Wiki]
    end

    ROUTER --> DOCS
    ROUTER --> PDF
    ROUTER --> WIKI

    subgraph Storage
        DB[(PostgreSQL)]
        VECTOR[(FAISS)]
    end

    RETRIEVER --> VECTOR
    VECTOR --> DB

    subgraph Model
        LLM[LLM]
    end

    GENERATOR --> LLM

    subgraph Ingestion
        INGEST[Loader -> Chunker -> Embedder]
    end

    INGEST --> DB
    INGEST --> VECTOR

    GENERATOR --> API
```

## System Preview

### 🖥️ Streamlit UI
![UI](<images/Streamlit/q4.png>)


### 🗄️ Database (PostgreSQL)
![DB](<images/Database/all question in db.png>)

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
git clone https://github.com/AhmedEssamSaber/multi-source-rag.git 
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

# 📁 Project Structure

```bash
app/
├── controllers/
│   ├── chat_controller.py        # FastAPI endpoint for handling chat requests
│
├── core/
│   ├── config.py                 # Project configuration 
│   ├── enums.py                  # Enum definitions 
│
├── data/
│   ├── docs/                     # Text documents source
│   ├── pdf/                      # PDF files source
│   └── wiki/                     # Wikipedia data source
│
├── FrontEnd/
│   └── streamlit_app.py          # Streamlit UI for interacting with the system
│
├── models/
│   ├── db/
│   │   ├── __init__.py           # DB module init
│   │   ├── base.py               # SQLAlchemy base model
│   │   └── database.py           # Database connection & session (Async)
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py        # Base CRUD operations
│   │   ├── document_repository.py    # Documents table operations
│   │   ├── chunk_repository.py       # Chunks table operations
│   │   ├── embedding_repository.py   # Embeddings table operations
│   │   └── query_log_repository.py   # Logs user queries & answers
│   │
│   ├── loader_model.py           # Load data from PDF / TXT
│   ├── chunking_model.py         # Split text into chunks
│   ├── embedding_model.py        # Generate embeddings
│   └── wiki_model.py             # Handle Wikipedia data fetching
│
├── scripts/
│   ├── download_wiki.py          # Script to download Wikipedia data
│   └── run_ingest.py             # Run full ingestion pipeline
│
├── services/
│   ├── ingestion_service.py      # Load → chunk → embed → store pipeline
│   ├── retriever_service.py      # Retrieve relevant chunks
│   ├── generator_service.py      # Generate answers using LLM
│   ├── router_service.py         # Route query to best data source
│   └── rag_service.py            # Main RAG orchestration logic
│
docker/
│   ├── docker-compose.yml        # Multi-container setup (app + DB)
│   ├── .env.example              # Example environment variables
│   └── .gitignore                # Ignore docker-related files
│
.env.example                    # Project environment variables template
.gitignore                      # Git ignore rules
LICENCE                         # Project license
requirements.txt                # Python dependencies
README.md                       # Project documentation
```

# Features
- Multi-source RAG (Docs / PDF / Wiki)
- FAISS vector search
- Async PostgreSQL
- Query logging system
- Reranking (Top-K → Best-K)
- Streamlit UI with chat history


# Database Schema
- documents
- chunks
- embeddings
- query_logs

# Database Stats
| Metric      | Count |
|-------------|-------|
| Documents   | 8     |
| Chunks      | 774   |
| Embeddings  | 774   |

# Why This Project Matters

- This project demonstrates:

  - Real-world RAG system design
  - Scalable backend architecture
  - AI + Backend integration
  - Production-level pipeline thinking

## 👤 Author

**Ahmed Essam**
- GitHub: [@AhmedEssamSaber](https://github.com/AhmedEssamSaber)

# 📄 License

This project is licensed under the terms in the [LICENSE](./LICENSE) file.
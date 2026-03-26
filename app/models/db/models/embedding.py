from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy import JSON

from app.models.db.base import Base


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True)

    chunk_id = Column(Integer, ForeignKey("chunks.id"))

    # vector size != embedding model
    embedding = Column(JSON)

    chunk = relationship("Chunk", backref="embedding")
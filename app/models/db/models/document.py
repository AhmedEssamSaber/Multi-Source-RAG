from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.models.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, index=True)   # pdf / wiki / docs
    file_name = Column(String)
    content = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
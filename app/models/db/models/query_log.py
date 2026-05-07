# from sqlalchemy import Column, Integer, String, Text, DateTime
# from datetime import datetime

# from app.models.db.database import Base


# class QueryLog(Base):
#     __tablename__ = "query_logs"

#     id = Column(Integer, primary_key=True, index=True)
#     question = Column(Text)
#     answer = Column(Text)
#     source = Column(String)
#     created_at = Column(DateTime, default=datetime.utcnow)


from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from app.models.db.database import Base


class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    source = Column(String)

    session_id = Column(String, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)
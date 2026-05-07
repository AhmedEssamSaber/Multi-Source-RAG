from app.models.db.models import QueryLog


class QueryLogRepository:

    def __init__(self, session):
        self.session = session

    async def create_log(self, question, answer, source, session_id):

        new_log = QueryLog(
            question=question,
            answer=answer,
            source=source,
            session_id=session_id 
        )

        self.session.add(new_log)
        await self.session.flush()

        return new_log
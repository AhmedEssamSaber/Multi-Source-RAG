class QueryLogRepository:

    def __init__(self, session):
        self.session = session

    async def create_log(self, question, answer, source):
        from app.models.db.models.query_log import QueryLog

        log = QueryLog(
            question=question,
            answer=answer,
            source=source
        )

        self.session.add(log)
        await self.session.flush()

        return log
from app.models.db.models.document import Document
from .base_repository import BaseRepository


class DocumentRepository(BaseRepository):

    async def create_document(self, source: str, file_name: str):

        doc = Document(
            source=source,
            file_name=file_name
        )

        self.session.add(doc)
        await self.session.flush() 

        return doc
from app.models.db.models.chunk import Chunk
from .base_repository import BaseRepository


class ChunkRepository(BaseRepository):

    async def create_chunk(self, document_id: int, content: str):

        chunk = Chunk(
            document_id=document_id,
            content=content
        )

        self.session.add(chunk)
        await self.session.flush()

        return chunk
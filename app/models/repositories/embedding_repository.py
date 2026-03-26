from app.models.db.models.embedding import Embedding
from .base_repository import BaseRepository


class EmbeddingRepository(BaseRepository):

    async def create_embedding(self, chunk_id: int, embedding):

        emb = Embedding(
            chunk_id=chunk_id,
            embedding=embedding
        )

        self.session.add(emb)
        await self.session.flush() 
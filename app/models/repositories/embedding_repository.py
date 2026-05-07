from app.models.db.models.embedding import Embedding
from .base_repository import BaseRepository

class EmbeddingRepository(BaseRepository):
    async def create_embedding(self, chunk_id, embedding):

        embedding = embedding.tolist()  

        new_embedding = Embedding(
            chunk_id=chunk_id,
            embedding=embedding
        )

        self.session.add(new_embedding)
        await self.session.flush()

        return new_embedding
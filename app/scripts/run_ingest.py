import asyncio
from app.services.ingestion_service import IngestionService


async def main():
    ingestor = IngestionService()
    await ingestor.ingest()


if __name__ == "__main__":
    asyncio.run(main())
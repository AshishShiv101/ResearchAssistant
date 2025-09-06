from celery import shared_task
from app.core.ingestion import ingest_document
import logging

logger = logging.getLogger(__name__)

@shared_task
def ingest_document_task(file_bytes: bytes, filename: str, content_type: str):
    """
    Background ingestion task.
    Runs the full ingestion pipeline asynchronously.
    """
    try:
        result = ingest_document(file_bytes, filename, content_type)
        logger.info(f"✅ Document {filename} ingested successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ Ingestion failed for {filename}: {str(e)}")
        raise

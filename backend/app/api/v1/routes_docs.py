from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ingestion import ingest_document

router = APIRouter(prefix="/docs", tags=["Documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        result = ingest_document(file_bytes, file.filename, file.content_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

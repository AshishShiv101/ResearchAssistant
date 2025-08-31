from fastapi import APIRouter, UploadFile, File
import os
import shutil

router = APIRouter(prefix="/docs", tags=["Documents"])

UPLOAD_DIR = "./uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a research document (PDF, DOCX, TXT, etc.)
    For now, just saves file to disk. Later -> ingestion pipeline.
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename, "path": file_path, "status": "uploaded"}

@router.get("/list")
async def list_documents():
    """List all uploaded documents"""
    files = os.listdir(UPLOAD_DIR)
    return {"documents": files}

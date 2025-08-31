from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/health")
def health_check():
    """Simple healthcheck endpoint"""
    return {"status": "ok", "service": "Research Assistant Backend"}

@router.get("/config")
def get_config():
    """Return basic config info (safe subset only)."""
    return {
        "app": "ResearchAssistant",
        "version": "1.0.0",
        "features": ["chat", "docs", "rag"],
    }

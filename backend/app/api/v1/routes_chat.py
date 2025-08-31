from fastapi import APIRouter, Query
import requests
from app.core.config import settings

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/ask")
def ask(query: str = Query(..., description="User's research question")):
    """
    Ask a question to the LLaMA model (Ollama backend for now).
    Later, you can hook this into RAG pipeline.
    """
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": settings.llm_model, "prompt": query},
            timeout=120,
        )
        data = response.json()
        return {"answer": data.get("response", "No response from model.")}
    except Exception as e:
        return {"error": str(e)}

# app/api/v1/routes_chat.py
from fastapi import APIRouter, Query
from app.services.embeddings import search_embeddings
import requests
from app.core.config import settings

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/ask")
def ask(query: str = Query(..., description="User's research question")):
    query = query.strip()  # remove any trailing newline or whitespace

    # Step 1: Retrieve relevant docs
    results = search_embeddings(query, top_k=3)
    context = "\n\n".join([r[1]["text"] for r in results])

    # Step 2: Send query + context to LLM (Ollama/LLaMA)
    prompt = f"Answer the following question using context:\n\n{context}\n\nQuestion: {query}"
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": settings.llm_model, "prompt": prompt},
        timeout=120,
    )
    data = response.json()
    return {
        "answer": data.get("response", "No response"),
        "sources": [r[1]["metadata"] for r in results],
    }

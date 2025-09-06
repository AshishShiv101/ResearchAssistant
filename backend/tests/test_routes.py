import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Research Assistant" in response.json()["message"]

def test_upload_txt_document():
    file_content = b"Hello from test file.\nThis should be ingested."
    response = client.post(
        "/docs/upload",
        files={"file": ("test.txt", file_content, "text/plain")},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ingested"
    assert data["filename"] == "test.txt"

def test_chat_endpoint_with_query(monkeypatch):
    # Monkeypatch rag pipeline to avoid heavy LLM call
    from app.core import rag

    def fake_rag_pipeline(query, top_k=5, system_prompt=None):
        return {"answer": "Mocked response", "sources": []}

    monkeypatch.setattr(rag, "rag_pipeline", fake_rag_pipeline)

    response = client.get("/chat/ask", params={"query": "What is AI?"})
    assert response.status_code == 200
    data = response.json()
    assert data["answer"] == "Mocked response"

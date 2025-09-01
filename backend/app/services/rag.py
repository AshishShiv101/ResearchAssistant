from typing import List, Dict
from app.core.embeddings import search_embeddings
from app.core.model_service import ModelService

model_service = ModelService()

def rag_pipeline(
    query: str,
    top_k: int = 5,
    system_prompt: str = None
) -> Dict:
    """
    Full Retrieval-Augmented Generation (RAG) pipeline:
    1. Retrieve top_k similar chunks from Firestore
    2. Build context
    3. Ask the LLM
    4. Return structured response
    """
    # Step 1: Retrieve chunks
    results = search_embeddings(query, top_k=top_k)
    if not results:
        return {"answer": "No relevant information found.", "sources": []}

    # Step 2: Prepare context (list of chunks)
    context_chunks = [r[1]["text"] for r in results]
    sources = [r[1]["metadata"] for r in results]

    # Step 3: Call LLM with RAG
    answer = model_service.rag_generate(
        query=query,
        context_chunks=context_chunks,
        system_prompt=system_prompt
    )

    return {
        "answer": answer,
        "sources": sources
    }

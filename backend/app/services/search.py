import numpy as np
from app.core.firebase import get_firestore
from app.core.embeddings import embed_text

db = get_firestore()

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Compute cosine similarity between two vectors."""
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def semantic_search(query: str, top_k: int = 5):
    """
    Perform semantic search over stored embeddings in Firestore.
    Returns top_k results sorted by similarity score.
    """
    query_vector = np.array(embed_text(query))
    embeddings_ref = db.collection("embeddings").stream()

    scored_results = []
    for doc in embeddings_ref:
        data = doc.to_dict()
        stored_vec = np.array(data["embedding"])
        score = cosine_similarity(query_vector, stored_vec)
        scored_results.append((score, data))

    # Sort by score
    scored_results.sort(key=lambda x: x[0], reverse=True)
    return scored_results[:top_k]

def hybrid_search(query: str, top_k: int = 5):
    """
    Placeholder for hybrid search (semantic + keyword).
    Could combine BM25, TF-IDF, or reranker.
    """
    return semantic_search(query, top_k)

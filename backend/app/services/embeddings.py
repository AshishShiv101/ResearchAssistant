from sentence_transformers import SentenceTransformer
import numpy as np
import json
from app.core.config import settings
from app.core.firebase import get_firestore

# Load embedding model (only once)
embedding_model = SentenceTransformer(settings.embedding_model)
db = get_firestore()

def embed_text(text: str) -> list[float]:
    """
    Generate vector embedding for given text using SentenceTransformers.
    Returns a list of floats (storable in Firestore).
    """
    vector = embedding_model.encode(text, convert_to_numpy=True).tolist()
    return vector

def store_embedding(doc_id: str, text: str, metadata: dict = None):
    """
    Store embedding + metadata in Firestore.
    Each chunk of a document gets its own embedding entry.
    """
    vector = embed_text(text)
    embedding_data = {
        "embedding": vector,
        "text": text,
        "metadata": metadata or {},
    }
    db.collection("embeddings").document(doc_id).set(embedding_data)

def search_embeddings(query: str, top_k: int = 5):
    """
    Naive semantic search over stored embeddings in Firestore.
    (Better: use FAISS, Pinecone, Weaviate, etc.)
    """
    query_vector = np.array(embed_text(query))
    embeddings_ref = db.collection("embeddings").stream()

    scored_results = []
    for doc in embeddings_ref:
        data = doc.to_dict()
        stored_vec = np.array(data["embedding"])
        # cosine similarity
        score = np.dot(query_vector, stored_vec) / (
            np.linalg.norm(query_vector) * np.linalg.norm(stored_vec)
        )
        scored_results.append((score, data))

    # Sort by similarity
    scored_results.sort(key=lambda x: x[0], reverse=True)
    return scored_results[:top_k]

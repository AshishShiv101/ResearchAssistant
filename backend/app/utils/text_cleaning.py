import re

def clean_text(text: str) -> str:
    """
    Basic text cleaning for ingestion pipeline.
    - Removes extra whitespace
    - Normalizes Unicode quotes, dashes
    - Strips non-printable characters
    """
    if not text:
        return ""

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    # Replace fancy quotes/dashes
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")
    text = text.replace("–", "-").replace("—", "-")

    # Remove non-printable characters
    text = "".join(c for c in text if c.isprintable())

    return text.strip()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
    Split text into overlapping chunks for embeddings.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks

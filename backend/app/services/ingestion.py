import os
import uuid
import fitz               # PyMuPDF for PDFs
import docx               # python-docx for Word
from app.core.firebase import get_firestore, get_bucket
from app.core.embeddings import store_embedding

db = get_firestore()
bucket = get_bucket()

# --------- Text Extraction Helpers ---------

def extract_text_from_pdf(file_bytes: bytes) -> list[str]:
    """Extract text chunks from a PDF file."""
    text_chunks = []
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        for page in doc:
            text = page.get_text("text")
            if text.strip():
                text_chunks.append(text)
    return text_chunks

def extract_text_from_docx(file_bytes: bytes) -> list[str]:
    """Extract text chunks from a DOCX file."""
    from io import BytesIO
    doc = docx.Document(BytesIO(file_bytes))
    return [para.text for para in doc.paragraphs if para.text.strip()]

def extract_text_from_txt(file_bytes: bytes) -> list[str]:
    """Extract text from TXT file."""
    text = file_bytes.decode("utf-8")
    return text.split("\n\n")  # split by paragraphs

# --------- Chunking ---------

def chunk_text(text: str, max_tokens: int = 500) -> list[str]:
    """
    Split text into chunks ~500 tokens each.
    Naive method: split by sentences.
    """
    import nltk
    nltk.download("punkt", quiet=True)
    from nltk.tokenize import sent_tokenize

    sentences = sent_tokenize(text)
    chunks, current_chunk = [], []
    token_count = 0

    for sentence in sentences:
        tokens = sentence.split()
        if token_count + len(tokens) > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk, token_count = [], 0
        current_chunk.append(sentence)
        token_count += len(tokens)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# --------- Ingestion Pipeline ---------

def ingest_document(file_bytes: bytes, filename: str, content_type: str) -> dict:
    """
    Full ingestion pipeline:
    1. Upload file to Firebase Storage
    2. Extract text
    3. Chunk text
    4. Store embeddings + metadata in Firestore
    """
    file_id = str(uuid.uuid4())
    blob = bucket.blob(f"docs/{file_id}_{filename}")
    blob.upload_from_string(file_bytes, content_type=content_type)

    # Extract text depending on file type
    if filename.endswith(".pdf"):
        raw_chunks = extract_text_from_pdf(file_bytes)
    elif filename.endswith(".docx"):
        raw_chunks = extract_text_from_docx(file_bytes)
    elif filename.endswith(".txt"):
        raw_chunks = extract_text_from_txt(file_bytes)
    else:
        raise ValueError("Unsupported file type")

    # Refine into token-based chunks
    final_chunks = []
    for raw_text in raw_chunks:
        final_chunks.extend(chunk_text(raw_text, max_tokens=500))

    # Store embeddings
    for idx, chunk in enumerate(final_chunks):
        doc_ref = f"{file_id}_{idx}"
        store_embedding(
            doc_id=doc_ref,
            text=chunk,
            metadata={"filename": filename, "doc_id": file_id, "chunk": idx}
        )

    return {
        "status": "ingested",
        "doc_id": file_id,
        "filename": filename,
        "chunks": len(final_chunks)
    }

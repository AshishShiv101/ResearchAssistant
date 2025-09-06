import pytest
from app.core.ingestion import ingest_document

@pytest.fixture
def sample_pdf_bytes():
    return b"%PDF-1.4 fake pdf file content"  # lightweight mock

def test_ingest_txt_file(tmp_path):
    content = b"Hello world.\n\nThis is a test document."
    filename = "sample.txt"
    content_type = "text/plain"

    result = ingest_document(content, filename, content_type)

    assert result["status"] == "ingested"
    assert result["filename"] == filename
    assert result["chunks"] > 0

def test_ingest_docx_file(tmp_path):
    from docx import Document
    from io import BytesIO

    doc = Document()
    doc.add_paragraph("This is a test DOCX document.")
    file_stream = BytesIO()
    doc.save(file_stream)

    filename = "sample.docx"
    content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

    result = ingest_document(file_stream.getvalue(), filename, content_type)

    assert result["status"] == "ingested"
    assert result["filename"] == filename
    assert result["chunks"] > 0

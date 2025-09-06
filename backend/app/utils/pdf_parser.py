from PyPDF2 import PdfReader
from utils.ocr import extract_text_from_image

def extract_text_from_pdf(file_bytes: bytes, use_ocr: bool = False) -> str:
    """
    Extract text from a PDF. If `use_ocr` is True, runs OCR on each page image.
    """
    text_content = []
    try:
        reader = PdfReader(io.BytesIO(file_bytes))

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
            elif use_ocr:
                # Render page as image for OCR
                try:
                    import fitz  # PyMuPDF
                    doc = fitz.open(stream=file_bytes, filetype="pdf")
                    pix = doc[page.number].get_pixmap()
                    image_bytes = pix.tobytes("png")
                    text_content.append(extract_text_from_image(image_bytes))
                except ImportError:
                    raise RuntimeError(
                        "OCR fallback requires PyMuPDF (pip install pymupdf)"
                    )

        return "\n".join(text_content).strip()

    except Exception as e:
        raise RuntimeError(f"PDF parsing failed: {str(e)}")

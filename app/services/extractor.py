import tempfile
import mimetypes
from fastapi import UploadFile
from pathlib import Path
from docx import Document
import pytesseract
from PIL import Image
import pdfplumber

async def extract_text(file: UploadFile) -> str:
    # Save file temporarily
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    ext = suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(tmp_path)
    elif ext == ".docx":
        return extract_text_from_docx(tmp_path)
    elif ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(tmp_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def extract_text_from_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(path: str) -> str:
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_from_image(path: str) -> str:
    return pytesseract.image_to_string(Image.open(path))

import os
import io
import tempfile
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
from docx import Document
import pdfplumber
from fastapi import UploadFile


def is_image(filename: str):
    return filename.lower().endswith((".jpg", ".jpeg", ".png"))


def is_pdf(filename: str):
    return filename.lower().endswith(".pdf")


def is_docx(filename: str):
    return filename.lower().endswith(".docx")


async def extract_text_from_pdf(file: UploadFile) -> str:
    contents = await file.read()


    text = ""
    with pdfplumber.open(io.BytesIO(contents)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    if not text.strip():
        images = convert_from_bytes(contents)
        for img in images:
            text += pytesseract.image_to_string(img)

    return text


async def extract_text_from_docx(file: UploadFile) -> str:
    contents = await file.read()
    doc = Document(io.BytesIO(contents))
    return "\n".join([para.text for para in doc.paragraphs])


async def extract_text_from_image(file: UploadFile) -> str:
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    return pytesseract.image_to_string(image)


async def extract_text(file: UploadFile) -> str:
    filename = file.filename.lower()
    if is_pdf(filename):
        return await extract_text_from_pdf(file)
    elif is_docx(filename):
        return await extract_text_from_docx(file)
    elif is_image(filename):
        return await extract_text_from_image(file)
    else:
        raise ValueError("Unsupported file type")

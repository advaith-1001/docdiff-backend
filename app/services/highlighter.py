import fitz  # PyMuPDF
from io import BytesIO

from fastapi import HTTPException
from starlette.datastructures import UploadFile


def highlight_pdfs(comparison_result, file1: UploadFile, file2: UploadFile):
    def highlight_text_in_pdf(upload_file: UploadFile, texts_to_highlight, color=(1, 0, 0)):
        from difflib import SequenceMatcher
        upload_file.file.seek(0)
        pdf_bytes = upload_file.file.read()
        if not pdf_bytes:
            raise ValueError("PDF stream is empty.")

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page in doc:
            words = page.get_text("words")
            word_texts = [w[4] for w in words]

            for phrase in texts_to_highlight:
                if not phrase.strip():
                    continue

                tokens = phrase.strip().split()
                max_len = len(tokens)
                phrase_lower = phrase.lower()

                for i in range(len(words) - max_len + 1):
                    window = words[i:i + max_len]
                    window_text = " ".join(w[4] for w in window).lower()
                    sim_ratio = SequenceMatcher(None, phrase_lower, window_text).ratio()

                    if sim_ratio > 0.9:
                        rects = [fitz.Rect(w[:4]) for w in window]
                        union_rect = rects[0]
                        for r in rects[1:]:
                            union_rect |= r
                        annot = page.add_highlight_annot(union_rect)
                        annot.set_colors(stroke=color)
                        annot.update()

        output = BytesIO()
        doc.save(output, garbage=4, deflate=True, clean=True)
        doc.close()
        output.seek(0)
        return output

    remove_texts = []
    add_texts = []

    for entry in comparison_result['diff']:
        if entry["type"] == "line_diff":
            for part in entry["parts"]:
                if part["type"] == "remove":
                    remove_texts.append(part["text"])
                elif part["type"] == "add":
                    add_texts.append(part["text"])
        elif entry["type"] == "remove":
            remove_texts.append(entry["text"])
        elif entry["type"] == "add":
            add_texts.append(entry["text"])

    pdf1_bytes = highlight_text_in_pdf(file1, remove_texts, color=(1.0, 0.6, 0.6))  # red
    pdf2_bytes = highlight_text_in_pdf(file2, add_texts, color=(0.6, 1.0, 0.6))     # green

    return pdf1_bytes, pdf2_bytes

import filetype
from PIL import Image
from docx import Document
from fpdf import FPDF

async def ensure_pdf(upload_file: UploadFile) -> UploadFile:
    upload_file.file.seek(0)
    file_bytes = await upload_file.read()
    kind = filetype.guess(file_bytes)

    if kind is None or kind.mime == "application/pdf":
        upload_file.file.seek(0)
        return upload_file

    pdf_stream = BytesIO()

    # Convert image to PDF
    if kind.mime.startswith("image/"):
        image = Image.open(BytesIO(file_bytes)).convert("RGB")
        image.save(pdf_stream, format="PDF")

    # Convert DOCX to PDF (basic text-only handling)
    elif kind.mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(BytesIO(file_bytes))
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        for para in doc.paragraphs:
            pdf.multi_cell(0, 10, para.text)
        pdf.output(pdf_stream)

    else:
        raise HTTPException(status_code=415, detail="Unsupported file type for conversion")

    pdf_stream.seek(0)
    return UploadFile(filename="converted.pdf", file=pdf_stream)
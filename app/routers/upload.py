import base64

from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.responses import JSONResponse
from app.services.extractor import extract_text
from difflib import HtmlDiff
from app.services.ocr import extract_text
from app.services.text_comparator import compare_texts
from app.services.highlighter import highlight_pdfs

from app.services.highlighter import ensure_pdf

router = APIRouter()


@router.post("/compare", response_model=str)
async def compare_documents(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        text1 = await extract_text(file1)
        text2 = await extract_text(file2)

        comparison_result = compare_texts(text1, text2)

        pdf_file1 = await ensure_pdf(file1)
        pdf_file2 = await ensure_pdf(file2)

        highlighted_pdf1, highlighted_pdf2 = highlight_pdfs(comparison_result, pdf_file1, pdf_file2)

        highlighted_pdf1_b64 = base64.b64encode(highlighted_pdf1.getvalue()).decode('utf-8')
        highlighted_pdf2_b64 = base64.b64encode(highlighted_pdf2.getvalue()).decode('utf-8')


        return JSONResponse(content={
            "diff": comparison_result,
            "highlighted_pdf1": highlighted_pdf1_b64,
            "highlighted_pdf2": highlighted_pdf2_b64
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


import base64

from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.responses import JSONResponse

from app.services.ai_summarizer import get_ai_summary
from app.services.extractor import extract_text
from app.services.ocr import extract_text
from app.services.text_comparator import compare_texts
from app.services.highlighter import highlight_pdfs
from app.services.compare import compare_pdf_formatting, compare_docx_formatting
from app.services.highlighter import ensure_pdf

router = APIRouter()


@router.post("/compare", response_model=str)
async def compare_documents(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        text1 = await extract_text(file1)
        text2 = await extract_text(file2)

        ai_summary = await get_ai_summary(text1, text2)

        file_extension = file1.filename.split('.')[-1].lower()


        comparison_result = compare_texts(text1, text2)

        pdf_file1 = await ensure_pdf(file1)
        pdf_file2 = await ensure_pdf(file2)

        differences = []

        if file_extension == 'docx':
            differences = compare_docx_formatting(file1, file2)
        elif file_extension == 'pdf':
            differences = await compare_pdf_formatting(file1, file2)

        highlighted_pdf1, highlighted_pdf2 = highlight_pdfs(comparison_result, pdf_file1, pdf_file2)

        highlighted_pdf1_b64 = base64.b64encode(highlighted_pdf1.getvalue()).decode('utf-8')
        highlighted_pdf2_b64 = base64.b64encode(highlighted_pdf2.getvalue()).decode('utf-8')


        return JSONResponse(content={
            "diff": comparison_result,
            "highlighted_pdf1": highlighted_pdf1_b64,
            "highlighted_pdf2": highlighted_pdf2_b64,
            "formatting_diffs": differences,
            "ai_summary": ai_summary,
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


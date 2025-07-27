from fastapi import APIRouter, UploadFile, File, HTTPException
from starlette.responses import JSONResponse
from app.services.extractor import extract_text
from difflib import HtmlDiff
from app.services.ocr import extract_text
from app.services.text_comparator import compare_texts


router = APIRouter()


@router.post("/compare", response_model=str)
async def compare_documents(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        text1 = await extract_text(file1)
        text2 = await extract_text(file2)

        comparison_result = compare_texts(text1, text2)

        return JSONResponse(content={
            "diff": comparison_result
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

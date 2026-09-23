from fastapi import APIRouter, HTTPException
from database.models import CorrectRequest, CorrectResponse
from correction.java_corrector import fix_java_code
from correction.python_corrector import fix_python_code

router = APIRouter(prefix="/api", tags=["Correction"])

@router.post("/correct", response_model=CorrectResponse)
async def correct_code_endpoint(request: CorrectRequest):
    lang = request.language.lower().strip()
    code = request.code

    if not code.strip():
        raise HTTPException(status_code=400, detail="Cannot correct empty code.")

    if lang == "java":
        return fix_java_code(code)
    elif lang == "python":
        return fix_python_code(code)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")

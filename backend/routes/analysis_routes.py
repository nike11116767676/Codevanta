from fastapi import APIRouter, HTTPException
from database.models import AnalyzeRequest, AnalyzeResponse
from analyzers.java_analyzer import analyze_java_code
from analyzers.python_analyzer import analyze_python_code

router = APIRouter(prefix="/api", tags=["Analysis"])

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code_endpoint(request: AnalyzeRequest):
    lang = request.language.lower().strip()
    code = request.code

    if not code.strip():
        return AnalyzeResponse(
            success=True,
            has_errors=False,
            errors=[],
            warnings=[],
            summary="Empty code buffer."
        )

    if lang == "java":
        return analyze_java_code(code)
    elif lang == "python":
        return analyze_python_code(code)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")

@router.post("/live-analyze", response_model=AnalyzeResponse)
async def live_analyze_endpoint(request: AnalyzeRequest):
    """Fast lightweight analysis for editor debouncing."""
    return await analyze_code_endpoint(request)

from fastapi import APIRouter, HTTPException
from database.models import AnalyzeRequest, CodeIntelligenceResponse
from ast_engine.java_ast import analyze_java_ast_intelligence
from ast_engine.python_ast import analyze_python_ast_intelligence
from analyzers.java_analyzer import analyze_java_code
from analyzers.python_analyzer import analyze_python_code

router = APIRouter(prefix="/api", tags=["AST & Intelligence"])

@router.post("/ast", response_model=CodeIntelligenceResponse)
async def get_ast_intelligence(request: AnalyzeRequest):
    lang = request.language.lower().strip()
    code = request.code

    if not code.strip():
        return CodeIntelligenceResponse(
            classes=0,
            methods=0,
            variables=0,
            loops=0,
            conditions=0,
            imports=0,
            health_score=100,
            ast_tree=None,
            breakdown={}
        )

    # First get error counts for genuine health score calculation
    if lang == "java":
        diag = analyze_java_code(code)
        return analyze_java_ast_intelligence(code, len(diag.errors), len(diag.warnings))
    elif lang == "python":
        diag = analyze_python_code(code)
        return analyze_python_ast_intelligence(code, len(diag.errors), len(diag.warnings))
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")

from fastapi import APIRouter, HTTPException
from database.models import RunRequest, RunResponse
from execution.java_executor import execute_java_code
from execution.python_executor import execute_python_code
from security.sandbox import validate_code_safety

router = APIRouter(prefix="/api", tags=["Execution"])

@router.post("/run", response_model=RunResponse)
async def run_code(request: RunRequest):
    lang = request.language.lower().strip()
    code = request.code
    stdin_input = request.stdin_input or ""

    if not code.strip():
        raise HTTPException(status_code=400, detail="Source code cannot be empty.")

    # Phase 6 Security Validation
    is_safe, sec_message = validate_code_safety(code)
    if not is_safe:
        return RunResponse(
            success=False,
            status="system_error",
            output="",
            error_output=sec_message,
            exit_code=-1,
            execution_time=0.0,
            command_echo="[SECURITY GUARD BLOCKED EXECUTION]"
        )

    if lang == "java":
        result = execute_java_code(code, stdin_input)
    elif lang == "python":
        result = execute_python_code(code, stdin_input)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}. Supported: 'java', 'python'")

    return RunResponse(
        success=result["success"],
        status=result["status"],
        output=result["output"],
        error_output=result.get("error_output", ""),
        exit_code=result["exit_code"],
        execution_time=result["execution_time"],
        command_echo=result["command_echo"]
    )

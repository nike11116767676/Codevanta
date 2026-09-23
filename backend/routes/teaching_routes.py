from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from database.db import get_concept, get_connection, get_all_error_history
from database.models import TeachResponse, QuizCheckRequest, QuizCheckResponse, QuizQuestion

router = APIRouter(prefix="/api", tags=["Teaching & History"])

@router.get("/teach/{error_id}", response_model=TeachResponse)
async def get_teaching_content(error_id: str):
    # Lookup by error_id or map error_id to concept
    conn = get_connection()
    cursor = conn.cursor()
    
    # First check errors table for concept_id
    cursor.execute("SELECT concept FROM errors WHERE id = ?", (error_id,))
    err_row = cursor.fetchone()
    conn.close()

    # Match concept
    concept = None
    if "SEMICOLON" in error_id:
        concept = get_concept("JAVA_STATEMENTS")
    elif "PAREN" in error_id:
        concept = get_concept("JAVA_PARENTHESES")
    elif "COLON" in error_id:
        concept = get_concept("PY_COMPOUND_STATEMENTS")
    elif "INDENT" in error_id:
        concept = get_concept("PY_INDENTATION")
    elif "NAME" in error_id:
        concept = get_concept("PY_NAME_ERROR")
    elif "SYMBOL" in error_id:
        concept = get_concept("JAVA_CANNOT_FIND_SYMBOL")
    elif "TYPE" in error_id:
        concept = get_concept("JAVA_INCOMPATIBLE_TYPES")
    elif "ZERO" in error_id or "ARITHMETIC" in error_id:
        concept = get_concept("JAVA_ARITHMETIC_ZERO")

    if not concept:
        # Fallback to general statement concept
        concept = get_concept("JAVA_STATEMENTS") or {
            "id": error_id,
            "title": "General Programming Concept",
            "what_happened": "A syntax or runtime constraint was violated.",
            "why_it_happened": "Compilers enforce strict grammatical rules to generate machine instructions unambiguously.",
            "wrong_example": "// Review line indicated",
            "correct_example": "// Follow language documentation",
            "memory_rule": "Read compiler diagnostics carefully.",
            "quiz": None
        }

    quiz_data = concept.get("quiz")
    quiz_obj = None
    if quiz_data:
        quiz_obj = QuizQuestion(
            question_id=quiz_data.get("question_id", "q_1"),
            question=quiz_data.get("question", ""),
            options=quiz_data.get("options", []),
            explanation=quiz_data.get("explanation", "")
        )

    return TeachResponse(
        error_id=error_id,
        title=concept.get("title", "Programming Concept"),
        concept=concept.get("title", ""),
        what_happened=concept.get("what_happened", ""),
        why_it_happened=concept.get("why_it_happened", ""),
        wrong_example=concept.get("wrong_example", ""),
        correct_example=concept.get("correct_example", ""),
        memory_rule=concept.get("memory_rule", ""),
        quiz=quiz_obj
    )

@router.post("/quiz/check", response_model=QuizCheckResponse)
async def check_quiz(request: QuizCheckRequest):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT quiz_json FROM concepts WHERE quiz_json LIKE ?", (f"%{request.question_id}%",))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Question not found")

    import json
    quiz = json.loads(row["quiz_json"])
    correct_id = quiz.get("correct_id", "A")
    explanation = quiz.get("explanation", "")

    is_correct = (request.selected_option_id.upper() == correct_id.upper())

    return QuizCheckResponse(
        correct=is_correct,
        explanation=explanation,
        correct_option_id=correct_id
    )

@router.get("/history")
async def get_history():
    return get_all_error_history(50)

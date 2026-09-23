from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class RunRequest(BaseModel):
    language: str = Field(..., description="Target language: 'java' or 'python'")
    code: str = Field(..., description="Source code to compile/execute")
    stdin_input: Optional[str] = Field("", description="Standard input for the program")

class RunResponse(BaseModel):
    success: bool
    status: str  # 'success', 'compilation_error', 'runtime_error', 'timeout', 'system_error'
    output: str
    error_output: Optional[str] = ""
    exit_code: int
    execution_time: float
    command_echo: str

class AnalyzeRequest(BaseModel):
    language: str
    code: str

class ErrorDetail(BaseModel):
    error_id: Optional[str] = None
    error_type: str  # 'syntax_error', 'compilation_error', 'runtime_error', 'logic_error'
    line: Optional[int] = None
    column: Optional[int] = None
    message: str
    title: str
    explanation: str
    cause: str
    solution: str
    concept: Optional[str] = None
    difficulty: Optional[str] = "beginner"
    severity: str = "error"  # 'error', 'warning', 'info'

class AnalyzeResponse(BaseModel):
    success: bool
    has_errors: bool
    errors: List[ErrorDetail] = []
    warnings: List[ErrorDetail] = []
    summary: str

class CorrectRequest(BaseModel):
    language: str
    code: str

class CodeChange(BaseModel):
    line: int
    before: str
    after: str
    description: str

class CorrectResponse(BaseModel):
    success: bool
    can_auto_correct: bool
    corrected_code: str
    changes: List[CodeChange] = []
    message: str
    diff_unified: str

class QuizOption(BaseModel):
    id: str
    text: str

class QuizQuestion(BaseModel):
    question_id: str
    question: str
    options: List[QuizOption]
    explanation: str

class TeachResponse(BaseModel):
    error_id: str
    title: str
    concept: str
    what_happened: str
    why_it_happened: str
    wrong_example: str
    correct_example: str
    memory_rule: str
    quiz: Optional[QuizQuestion] = None

class QuizCheckRequest(BaseModel):
    question_id: str
    selected_option_id: str

class QuizCheckResponse(BaseModel):
    correct: bool
    explanation: str
    correct_option_id: str

class ASTNode(BaseModel):
    name: str
    node_type: str
    line: Optional[int] = None
    children: List['ASTNode'] = []

ASTNode.model_rebuild()

class CodeIntelligenceResponse(BaseModel):
    classes: int
    methods: int
    variables: int
    loops: int
    conditions: int
    imports: int
    health_score: int
    ast_tree: Optional[ASTNode] = None
    breakdown: Dict[str, Any] = {}

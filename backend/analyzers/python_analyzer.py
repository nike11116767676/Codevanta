import ast
import builtins
import re
from typing import List, Set
from database.db import find_error_rule, record_error_history
from database.models import ErrorDetail, AnalyzeResponse

BUILTIN_NAMES = set(dir(builtins))

class VariableScopeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.defined_names: Set[str] = set()
        self.loaded_names: List[tuple] = []  # (name, lineno, col_offset)
        self.assigned_names: Set[str] = set()
        self.imported_names: Set[str] = set()

    def visit_Import(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.defined_names.add(name)
            self.imported_names.add(name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            name = alias.asname or alias.name
            self.defined_names.add(name)
            self.imported_names.add(name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.defined_names.add(node.name)
        # Add parameter names
        for arg in node.args.args:
            self.defined_names.add(arg.arg)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node):
        self.defined_names.add(node.name)
        for arg in node.args.args:
            self.defined_names.add(arg.arg)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.defined_names.add(node.name)
        self.generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self.defined_names.add(node.id)
            self.assigned_names.add(node.id)
        elif isinstance(node.ctx, ast.Load):
            self.loaded_names.append((node.id, node.lineno, node.col_offset))
        self.generic_visit(node)

def analyze_python_code(code: str) -> AnalyzeResponse:
    """
    Analyzes Python source code using compile(), ast.parse(), rule matching,
    and static AST variable scope analysis.
    """
    errors: List[ErrorDetail] = []
    warnings: List[ErrorDetail] = []

    # 1. Check for SyntaxError or IndentationError
    try:
        compile(code, "<string>", "exec")
    except (SyntaxError, IndentationError) as e:
        raw_msg = f"{e.__class__.__name__}: {e.msg}"
        line = e.lineno or 1
        column = e.offset or 1
        rule = find_error_rule("python", raw_msg) or find_error_rule("python", e.msg)

        if rule:
            err_detail = ErrorDetail(
                error_id=rule["id"],
                error_type=rule["error_type"],
                line=line,
                column=column,
                message=raw_msg,
                title=rule["title"],
                explanation=rule["explanation"],
                cause=rule["cause"],
                solution=rule["solution"],
                concept=rule["concept"],
                difficulty=rule.get("difficulty", "beginner"),
                severity="error"
            )
            record_error_history("python", rule["id"], rule["title"], line, e.text or "")
        else:
            err_detail = ErrorDetail(
                error_id="PY_SYNTAX_ERROR",
                error_type="syntax_error",
                line=line,
                column=column,
                message=raw_msg,
                title="Python Syntax Error",
                explanation=f"Python syntax violation at line {line}: {e.msg}",
                cause=f"The interpreter could not parse the code structure: {e.msg}",
                solution="Inspect line and column position. Ensure parentheses match and blocks end with colons.",
                concept="Python Grammar & Syntax",
                difficulty="beginner",
                severity="error"
            )
        errors.append(err_detail)
        return AnalyzeResponse(
            success=False,
            has_errors=True,
            errors=errors,
            warnings=[],
            summary=f"1 syntax error detected at line {line}."
        )
    except Exception as e:
        errors.append(ErrorDetail(
            error_id="PY_COMPILE_FAIL",
            error_type="syntax_error",
            line=1,
            column=1,
            message=str(e),
            title="Python Compilation Failure",
            explanation=str(e),
            cause="Unable to compile python script.",
            solution="Review recent edits.",
            concept="Syntax",
            severity="error"
        ))
        return AnalyzeResponse(success=False, has_errors=True, errors=errors, warnings=[], summary="Compilation failure.")

    # 2. If code parses cleanly, perform AST static checks
    try:
        tree = ast.parse(code)
        visitor = VariableScopeVisitor()
        visitor.visit(tree)

        # Check for undefined variables
        all_known = BUILTIN_NAMES | visitor.defined_names
        for name, lineno, col_offset in visitor.loaded_names:
            if name not in all_known:
                rule = find_error_rule("python", f"NameError: name '{name}' is not defined")
                warnings.append(ErrorDetail(
                    error_id="PY_NAME_ERROR",
                    error_type="runtime_error",
                    line=lineno,
                    column=col_offset + 1,
                    message=f"NameError: name '{name}' is not defined",
                    title="Undefined Variable Reference",
                    explanation=f"Variable '{name}' is referenced but was never defined or imported in this scope.",
                    cause=f"Possible typo in '{name}', or variable used before assignment.",
                    solution=f"Assign an initial value to '{name}' before this line, or fix spelling.",
                    concept="Variables & Scopes",
                    difficulty="beginner",
                    severity="warning"
                ))

        # Check for literal division by zero in AST
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Div, ast.FloorDiv, ast.Mod)):
                if isinstance(node.right, ast.Constant) and node.right.value == 0:
                    warnings.append(ErrorDetail(
                        error_id="PY_ZERO_DIVISION",
                        error_type="runtime_error",
                        line=node.lineno,
                        column=node.col_offset + 1,
                        message="ZeroDivisionError: division by zero",
                        title="Division by Zero Detected",
                        explanation="Expression attempts to divide directly by literal zero 0.",
                        cause="Denominator is constant 0.",
                        solution="Ensure the denominator is not 0.",
                        concept="Arithmetic & Exception Handling",
                        difficulty="beginner",
                        severity="warning"
                    ))

            # Comparison to None using == instead of 'is'
            if isinstance(node, ast.Compare):
                for comparator in node.comparators:
                    if isinstance(comparator, ast.Constant) and comparator.value is None:
                        for op in node.ops:
                            if isinstance(op, ast.Eq):
                                warnings.append(ErrorDetail(
                                    error_id="PY_STYLE_NONE_COMPARISON",
                                    error_type="logic_error",
                                    line=node.lineno,
                                    column=node.col_offset + 1,
                                    message="Use 'is None' instead of '== None'",
                                    title="PEP 8 None Comparison",
                                    explanation="Comparisons to singletons like None should always be done with 'is' or 'is not', never the equality operators.",
                                    cause="Used '==' to compare an expression against None.",
                                    solution="Replace '== None' with 'is None'.",
                                    concept="Python Idioms & PEP 8",
                                    difficulty="beginner",
                                    severity="info"
                                ))

    except Exception as e:
        pass

    has_errors = len(errors) > 0
    total_issues = len(errors) + len(warnings)
    summary = f"{len(errors)} error(s), {len(warnings)} warning(s) detected." if total_issues > 0 else "Code passed compilation and syntax analysis."

    return AnalyzeResponse(
        success=not has_errors,
        has_errors=has_errors,
        errors=errors,
        warnings=warnings,
        summary=summary
    )

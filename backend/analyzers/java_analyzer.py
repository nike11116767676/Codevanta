import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any
from config import JAVAC_EXECUTABLE, DEFAULT_TIMEOUT_SECONDS
from execution.java_executor import extract_java_class_name
from analyzers.error_parser import parse_javac_output
from database.db import find_error_rule, record_error_history
from database.models import ErrorDetail, AnalyzeResponse

def check_java_logical_bugs(code: str) -> List[ErrorDetail]:
    """Deterministic static checks for common Java beginner logic pitfalls."""
    bugs = []
    lines = code.splitlines()

    for idx, line in enumerate(lines, start=1):
        clean_line = line.strip()

        # 1. Accidental semicolon directly after loop header: while (condition); or for (...);
        if re.search(r'\b(for|while)\s*\([^)]*\)\s*;', clean_line) and not clean_line.startswith("//"):
            bugs.append(ErrorDetail(
                error_id="JAVA_LOGIC_EMPTY_LOOP",
                error_type="logic_error",
                line=idx,
                column=len(line) - 1,
                message="Loop body immediately terminated with semicolon ';'",
                title="Accidental Empty Loop Semicolon",
                explanation="Placing a semicolon immediately after a loop header creates an empty loop body. The code block beneath it will only execute once after the loop ends (or cause an infinite loop if the condition never changes).",
                cause="Accidentally placed ';' right after the loop condition instead of using a '{' block.",
                solution="Remove the ';' immediately following the loop header and enclose the loop body in curly braces '{ }'.",
                concept="Java Loops & Control Flow",
                difficulty="beginner",
                severity="warning"
            ))

        # 2. Off-by-one array length indexing: i <= arr.length
        if re.search(r'\b[a-zA-Z0-9_]+\s*<=\s*[a-zA-Z0-9_]+\.length\b', clean_line):
            bugs.append(ErrorDetail(
                error_id="JAVA_ARRAY_INDEX_OOB",
                error_type="logic_error",
                line=idx,
                column=clean_line.find("<="),
                message="Potential off-by-one error: using '<=' with array .length",
                title="Off-by-One Array Bound",
                explanation="Java arrays are 0-indexed, so the highest valid index is length - 1. Iterating with '<= length' will cause an ArrayIndexOutOfBoundsException.",
                cause="Condition tested '<=' instead of '<' against array length.",
                solution="Change '<=' to '<' in your loop condition.",
                concept="Arrays & Zero-Indexing",
                difficulty="beginner",
                severity="warning"
            ))

        # 3. String comparison with == instead of .equals()
        if re.search(r'\b[a-zA-Z0-9_]+\s*==\s*"[^"]*"', clean_line) or re.search(r'"[^"]*"\s*==\s*[a-zA-Z0-9_]+', clean_line):
            bugs.append(ErrorDetail(
                error_id="JAVA_STRING_EQUALS",
                error_type="logic_error",
                line=idx,
                column=1,
                message="String comparison using '==' checks reference identity, not value equality.",
                title="String Comparison with '=='",
                explanation="In Java, '==' compares object memory references. To compare the actual string contents, you must use .equals().",
                cause="Used the '==' operator to compare a String object with a literal or another string.",
                solution="Replace 'str == \"value\"' with 'str.equals(\"value\")'.",
                concept="Java Strings & Object Equality",
                difficulty="beginner",
                severity="warning"
            ))

    return bugs

def analyze_java_code(code: str) -> AnalyzeResponse:
    """
    Analyzes Java code using javac compiler diagnostics, knowledge base rules,
    and deterministic static checks.
    """
    class_name = extract_java_class_name(code)
    temp_dir = tempfile.mkdtemp(prefix="codevanta_java_diag_")
    errors: List[ErrorDetail] = []
    warnings: List[ErrorDetail] = []

    try:
        java_file_path = Path(temp_dir) / f"{class_name}.java"
        with open(java_file_path, "w", encoding="utf-8") as f:
            f.write(code)

        # Run javac with -Xlint
        cmd = [JAVAC_EXECUTABLE, "-Xlint", f"{class_name}.java"]
        proc = subprocess.run(
            cmd,
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=DEFAULT_TIMEOUT_SECONDS
        )

        parsed_diagnostics = parse_javac_output(proc.stderr or proc.stdout)

        for diag in parsed_diagnostics:
            raw_msg = diag["raw_message"]
            rule = find_error_rule("java", raw_msg)

            if rule:
                err_detail = ErrorDetail(
                    error_id=rule["id"],
                    error_type=rule["error_type"],
                    line=diag["line"],
                    column=diag["column"],
                    message=raw_msg,
                    title=rule["title"],
                    explanation=rule["explanation"],
                    cause=rule["cause"],
                    solution=rule["solution"],
                    concept=rule["concept"],
                    difficulty=rule.get("difficulty", "beginner"),
                    severity=diag["severity"]
                )
                # Record to history
                record_error_history("java", rule["id"], rule["title"], diag["line"], diag["code_snippet"])
            else:
                err_detail = ErrorDetail(
                    error_id="JAVA_UNKNOWN",
                    error_type="compilation_error" if diag["severity"] == "error" else "warning",
                    line=diag["line"],
                    column=diag["column"],
                    message=raw_msg,
                    title="Java Compilation Issue",
                    explanation=f"The Java compiler reported: {raw_msg}",
                    cause="Syntax or type violation reported by javac.",
                    solution="Inspect the line indicated and ensure standard Java syntax rules are met.",
                    concept="Java Compiler Diagnostics",
                    difficulty="intermediate",
                    severity=diag["severity"]
                )

            if diag["severity"] == "error":
                errors.append(err_detail)
            else:
                warnings.append(err_detail)

    except subprocess.TimeoutExpired:
        errors.append(ErrorDetail(
            error_id="JAVA_TIMEOUT",
            error_type="compilation_error",
            line=1,
            column=1,
            message="Compilation timed out",
            title="Compiler Timeout",
            explanation="The Java compiler took too long to analyze the source code.",
            cause="Complex nested structures or system delay.",
            solution="Simplify the code structure.",
            concept="Compilation",
            severity="error"
        ))
    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

    # Add deterministic logic warnings if no blocking syntax errors
    if not errors:
        logic_warnings = check_java_logical_bugs(code)
        warnings.extend(logic_warnings)

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

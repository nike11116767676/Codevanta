import re
from typing import Tuple, Optional
from analyzers.java_analyzer import analyze_java_code
from correction.diff_generator import generate_code_diff
from database.models import CorrectResponse

def fix_java_code(code: str) -> CorrectResponse:
    """
    Applies deterministic correction rules to Java source code.
    Follows safe correction policy: only modifies code when correction is deterministic.
    """
    analysis = analyze_java_code(code)

    if not analysis.has_errors and not analysis.warnings:
        return CorrectResponse(
            success=True,
            can_auto_correct=False,
            corrected_code=code,
            changes=[],
            message="No errors detected. Code is already syntactically valid.",
            diff_unified=""
        )

    lines = code.splitlines()
    modified = False
    message = "Applied automatic fix."

    # Priority 1: Handle compiler errors
    for err in analysis.errors:
        line_idx = (err.line or 1) - 1
        if 0 <= line_idx < len(lines):
            target_line = lines[line_idx]

            # Rule 1: Missing semicolon ';'
            if "';' expected" in err.message or err.error_id == "JAVA_SEMICOLON":
                stripped = target_line.rstrip()
                if not stripped.endswith(";") and not stripped.endswith("{") and not stripped.endswith("}"):
                    lines[line_idx] = stripped + ";"
                    modified = True
                    message = f"Added missing semicolon ';' at line {err.line}."
                    break

            # Rule 2: Unbalanced parenthesis ')' expected
            elif "')' expected" in err.message or err.error_id == "JAVA_PAREN_EXPECTED":
                # Count parens on line
                open_cnt = target_line.count("(")
                close_cnt = target_line.count(")")
                if open_cnt > close_cnt:
                    needed = open_cnt - close_cnt
                    stripped = target_line.rstrip()
                    if stripped.endswith(";"):
                        lines[line_idx] = stripped[:-1] + (")" * needed) + ";"
                    else:
                        lines[line_idx] = stripped + (")" * needed)
                    modified = True
                    message = f"Closed {needed} missing parenthesis ')' at line {err.line}."
                    break

            # Rule 3: Unclosed string literal
            elif "unclosed string literal" in err.message or err.error_id == "JAVA_UNCLOSED_STRING":
                quote_count = target_line.count('"') - target_line.count('\\"')
                if quote_count % 2 != 0:
                    stripped = target_line.rstrip()
                    if stripped.endswith(";"):
                        lines[line_idx] = stripped[:-1] + '";'
                    else:
                        lines[line_idx] = stripped + '"'
                    modified = True
                    message = f"Added missing closing quote '\"' at line {err.line}."
                    break

    # Rule 4: Global curly brace balance
    if not modified:
        total_open_braces = code.count("{")
        total_close_braces = code.count("}")
        if total_open_braces > total_close_braces:
            missing_braces = total_open_braces - total_close_braces
            lines.append("}" * missing_braces)
            modified = True
            message = f"Added {missing_braces} missing closing brace(s) '}}' at the end of class."

    # Priority 2: Handle deterministic warnings (like empty loops or string ==)
    if not modified and analysis.warnings:
        for warn in analysis.warnings:
            line_idx = (warn.line or 1) - 1
            if 0 <= line_idx < len(lines):
                target_line = lines[line_idx]

                # Off-by-one <= length fix
                if warn.error_id == "JAVA_ARRAY_INDEX_OOB":
                    fixed_line = re.sub(r'<=\s*([a-zA-Z0-9_]+\.length)\b', r'< \1', target_line)
                    if fixed_line != target_line:
                        lines[line_idx] = fixed_line
                        modified = True
                        message = f"Fixed off-by-one array boundary '<=' to '<' at line {warn.line}."
                        break

                # Accidental empty loop semicolon
                if warn.error_id == "JAVA_LOGIC_EMPTY_LOOP":
                    fixed_line = re.sub(r'(\b(?:for|while)\s*\([^)]*\))\s*;', r'\1', target_line)
                    if fixed_line != target_line:
                        lines[line_idx] = fixed_line
                        modified = True
                        message = f"Removed accidental loop-terminating semicolon at line {warn.line}."
                        break

    if not modified:
        # Safe correction policy per Section 25: multiple ambiguous ways to fix
        return CorrectResponse(
            success=False,
            can_auto_correct=False,
            corrected_code=code,
            changes=[],
            message="Multiple possible corrections exist or manual symbol declaration is required. Please review suggestion.",
            diff_unified=""
        )

    corrected_code = "\n".join(lines)
    changes, diff_unified = generate_code_diff(code, corrected_code)

    return CorrectResponse(
        success=True,
        can_auto_correct=True,
        corrected_code=corrected_code,
        changes=changes,
        message=message,
        diff_unified=diff_unified
    )

import re
import difflib
from typing import Tuple, List, Set
from analyzers.python_analyzer import analyze_python_code, VariableScopeVisitor
from correction.diff_generator import generate_code_diff
from database.models import CorrectResponse

COMPOUND_KEYWORDS = (
    "if", "elif", "else", "for", "while", "def", 
    "class", "try", "except", "finally", "with", "match", "case"
)

def fix_python_code(code: str) -> CorrectResponse:
    """
    Applies deterministic correction rules to Python code.
    Follows safe correction policy: only modifies when solution is unambiguous.
    """
    analysis = analyze_python_code(code)

    if not analysis.has_errors and not analysis.warnings:
        return CorrectResponse(
            success=True,
            can_auto_correct=False,
            corrected_code=code,
            changes=[],
            message="No errors detected. Python syntax is valid.",
            diff_unified=""
        )

    lines = code.splitlines()
    modified = False
    message = "Applied automatic fix."

    # Priority 1: Handle Syntax Errors
    for err in analysis.errors:
        line_idx = (err.line or 1) - 1
        if 0 <= line_idx < len(lines):
            target_line = lines[line_idx]
            stripped = target_line.strip()

            # Rule 1: Missing colon ':'
            # e.g., "if x > 10" or "def foo()" or "while True"
            for kw in COMPOUND_KEYWORDS:
                if re.match(rf'^{kw}\b', stripped) and not stripped.endswith(":"):
                    lines[line_idx] = target_line.rstrip() + ":"
                    modified = True
                    message = f"Added missing colon ':' to '{kw}' statement at line {err.line}."
                    break

            if modified:
                break

            # Rule 2: Unclosed parenthesis / bracket
            if "was never closed" in err.message or err.error_id == "PY_UNCLOSED_PAREN":
                open_parens = target_line.count("(") - target_line.count(")")
                open_brackets = target_line.count("[") - target_line.count("]")
                open_curlies = target_line.count("{") - target_line.count("}")

                fixed_line = target_line.rstrip()
                if open_parens > 0:
                    fixed_line += ")" * open_parens
                if open_brackets > 0:
                    fixed_line += "]" * open_brackets
                if open_curlies > 0:
                    fixed_line += "}" * open_curlies

                if fixed_line != target_line:
                    lines[line_idx] = fixed_line
                    modified = True
                    message = f"Closed unclosed delimiter(s) at line {err.line}."
                    break

            # Rule 3: Expected an indented block
            if "expected an indented block" in err.message or err.error_id == "PY_INDENTATION_ERROR":
                # Check if next line exists and needs indentation, or insert 'pass'
                if line_idx < len(lines):
                    prev_indent = len(target_line) - len(target_line.lstrip())
                    new_indent = " " * (prev_indent + 4)
                    lines.insert(line_idx, f"{new_indent}pass")
                    modified = True
                    message = f"Inserted default 'pass' block with 4-space indentation at line {err.line}."
                    break

    # Priority 2: Handle Warnings & Name Typos
    if not modified and analysis.warnings:
        for warn in analysis.warnings:
            line_idx = (warn.line or 1) - 1
            if 0 <= line_idx < len(lines):
                target_line = lines[line_idx]

                # Rule 4: Fix NameError typos if close match exists
                name_match = re.search(r"NameError: name '([^']+)' is not defined", warn.message)
                if name_match:
                    bad_name = name_match.group(1)
                    # Find candidates in the file
                    tokens = set(re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', code))
                    tokens.discard(bad_name)
                    close_matches = difflib.get_close_matches(bad_name, list(tokens), n=1, cutoff=0.7)
                    if close_matches:
                        suggested_name = close_matches[0]
                        # Replace only the specific identifier
                        fixed_line = re.sub(rf'\b{re.escape(bad_name)}\b', suggested_name, target_line)
                        if fixed_line != target_line:
                            lines[line_idx] = fixed_line
                            modified = True
                            message = f"Corrected typo '{bad_name}' to '{suggested_name}' at line {warn.line}."
                            break

                # Rule 5: Fix == None to is None
                if warn.error_id == "PY_STYLE_NONE_COMPARISON":
                    fixed_line = re.sub(r'==\s*None\b', 'is None', target_line)
                    if fixed_line != target_line:
                        lines[line_idx] = fixed_line
                        modified = True
                        message = f"Replaced '== None' with 'is None' at line {warn.line}."
                        break

    if not modified:
        return CorrectResponse(
            success=False,
            can_auto_correct=False,
            corrected_code=code,
            changes=[],
            message="Multiple possible fixes exist. Manual review is recommended.",
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

import re
from typing import List, Dict, Any, Optional

def parse_javac_output(output: str) -> List[Dict[str, Any]]:
    """
    Parses Java compiler output into structured error diagnostics.
    Typical format:
    Main.java:4: error: ';' expected
        int a = 10
                  ^
    """
    errors = []
    lines = output.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i]
        # Match pattern: <filename>:<line>: error: <message>
        match = re.match(r'^(?:[A-Za-z0-9_]+\.java|\<[a-z]+\>):(\d+):\s*(error|warning):\s*(.+)$', line.strip())
        if match:
            line_num = int(match.group(1))
            severity = match.group(2).lower()
            message = match.group(3).strip()
            
            column = 1
            code_line = ""
            
            # Check next lines for snippet and column caret ^
            if i + 1 < len(lines) and not re.match(r'^\S+\.java:\d+:', lines[i+1]):
                code_line = lines[i+1]
                if i + 2 < len(lines) and '^' in lines[i+2]:
                    caret_line = lines[i+2]
                    column = caret_line.find('^') + 1
                    i += 2
                else:
                    i += 1

            errors.append({
                "line": line_num,
                "column": column,
                "severity": severity,
                "raw_message": message,
                "code_snippet": code_line.strip()
            })
        i += 1

    return errors

def parse_python_traceback(stderr: str) -> Optional[Dict[str, Any]]:
    """
    Parses Python runtime traceback or syntax error output.
    """
    lines = stderr.strip().splitlines()
    if not lines:
        return None

    # Check for SyntaxError / IndentationError
    last_line = lines[-1]
    syntax_match = re.match(r'^(SyntaxError|IndentationError):\s*(.+)$', last_line)
    if syntax_match:
        err_type = syntax_match.group(1)
        err_msg = syntax_match.group(2)
        line_num = 1
        col_num = 1

        for l in lines:
            line_match = re.search(r'line\s+(\d+)', l)
            if line_match:
                line_num = int(line_match.group(1))
            if '^' in l:
                col_num = l.find('^') + 1

        return {
            "type": err_type,
            "message": f"{err_type}: {err_msg}",
            "line": line_num,
            "column": col_num,
            "is_syntax": True
        }

    # Check for runtime exception (e.g., ZeroDivisionError: division by zero)
    runtime_match = re.match(r'^([A-Za-z0-9_]+Error|[A-Za-z0-9_]+Exception):\s*(.+)$', last_line)
    if runtime_match:
        exc_type = runtime_match.group(1)
        exc_msg = runtime_match.group(2)
        line_num = 1

        # Look for the last "File "...", line X" in traceback
        for l in reversed(lines):
            line_match = re.search(r'line\s+(\d+)', l)
            if line_match:
                line_num = int(line_match.group(1))
                break

        return {
            "type": exc_type,
            "message": f"{exc_type}: {exc_msg}",
            "line": line_num,
            "column": 1,
            "is_syntax": False
        }

    return None

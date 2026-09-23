import os
import re
from typing import Tuple

FORBIDDEN_PATTERNS = [
    r'\bformat\s+[a-zA-Z]:',
    r'\bdel\s+/[a-zA-Z0-9\s]*[cC]:',
    r'\brmdir\s+/[a-zA-Z0-9\s]*[cC]:',
    r'os\.system\s*\(\s*["\'](?:format|del|rmdir|shutdown)',
    r'subprocess\.(?:call|Popen|run)\s*\(\s*["\'](?:shutdown|format)'
]

def validate_code_safety(code: str) -> Tuple[bool, str]:
    """
    Scans code for destructive system operations prior to execution.
    Deterministic security boundary check.
    """
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, code, re.IGNORECASE):
            return False, "Security constraint violated: Potentially destructive system command detected."
    return True, "Code passed security validation."

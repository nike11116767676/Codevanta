import difflib
from typing import List, Dict, Any, Tuple
from database.models import CodeChange

def generate_code_diff(original: str, corrected: str) -> Tuple[List[CodeChange], str]:
    """
    Compares original and corrected code, returning structured line changes
    and a unified diff string.
    """
    orig_lines = original.splitlines()
    corr_lines = corrected.splitlines()

    changes: List[CodeChange] = []

    # Generate unified diff string
    unified_diff_list = list(difflib.unified_diff(
        orig_lines,
        corr_lines,
        fromfile='original',
        tofile='corrected',
        lineterm=''
    ))
    unified_diff = '\n'.join(unified_diff_list)

    # Calculate line-by-line before/after pairs
    matcher = difflib.SequenceMatcher(None, orig_lines, corr_lines)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            for line_idx in range(i1, i2):
                before = orig_lines[line_idx]
                after_idx = j1 + (line_idx - i1)
                after = corr_lines[after_idx] if after_idx < j2 else ""
                changes.append(CodeChange(
                    line=line_idx + 1,
                    before=before,
                    after=after,
                    description=f"Replaced '{before.strip()}' with '{after.strip()}'"
                ))
        elif tag == 'insert':
            for line_idx in range(j1, j2):
                changes.append(CodeChange(
                    line=i1 + 1,
                    before="",
                    after=corr_lines[line_idx],
                    description=f"Added '{corr_lines[line_idx].strip()}'"
                ))
        elif tag == 'delete':
            for line_idx in range(i1, i2):
                changes.append(CodeChange(
                    line=line_idx + 1,
                    before=orig_lines[line_idx],
                    after="",
                    description=f"Removed '{orig_lines[line_idx].strip()}'"
                ))

    return changes, unified_diff

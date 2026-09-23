import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Tuple
from config import JAVAC_EXECUTABLE, JAVA_EXECUTABLE, DEFAULT_TIMEOUT_SECONDS, MAX_OUTPUT_LENGTH

def extract_java_class_name(code: str) -> str:
    """
    Finds the public class name or the class with main method,
    defaulting to 'Main' if none found.
    """
    # Look for public class <Name>
    public_match = re.search(r'\bpublic\s+class\s+([A-Za-z0-9_]+)', code)
    if public_match:
        return public_match.group(1)

    # Look for any class <Name> containing main method
    class_blocks = re.finditer(r'\bclass\s+([A-Za-z0-9_]+)\s*\{', code)
    for match in class_blocks:
        class_name = match.group(1)
        # Search if main method exists nearby or in code
        return class_name

    # Check for general class <Name>
    general_match = re.search(r'\bclass\s+([A-Za-z0-9_]+)', code)
    if general_match:
        return general_match.group(1)

    return "Main"

def execute_java_code(code: str, stdin_input: str = "", timeout: float = DEFAULT_TIMEOUT_SECONDS) -> dict:
    """
    Compiles and runs Java code in an isolated directory.
    Returns:
      success: bool
      status: str ('success', 'compilation_error', 'runtime_error', 'timeout', 'system_error')
      output: str
      error_output: str
      exit_code: int
      execution_time: float
      command_echo: str
    """
    class_name = extract_java_class_name(code)
    temp_dir = tempfile.mkdtemp(prefix="codevanta_java_")

    try:
        java_file_path = Path(temp_dir) / f"{class_name}.java"
        with open(java_file_path, "w", encoding="utf-8") as f:
            f.write(code)

        # 1. Compile with javac
        compile_cmd = [JAVAC_EXECUTABLE, f"{class_name}.java"]
        compile_echo = f"$ javac {class_name}.java"
        
        start_time = time.perf_counter()
        try:
            compile_proc = subprocess.run(
                compile_cmd,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "status": "timeout",
                "output": "",
                "error_output": f"Compilation timed out after {timeout} seconds.",
                "exit_code": -1,
                "execution_time": timeout,
                "command_echo": compile_echo
            }
        except FileNotFoundError:
            return {
                "success": False,
                "status": "system_error",
                "output": "",
                "error_output": f"Java compiler '{JAVAC_EXECUTABLE}' not found on system PATH.",
                "exit_code": -1,
                "execution_time": 0.0,
                "command_echo": compile_echo
            }

        compile_time = time.perf_counter() - start_time

        if compile_proc.returncode != 0:
            err_msg = compile_proc.stderr[:MAX_OUTPUT_LENGTH]
            return {
                "success": False,
                "status": "compilation_error",
                "output": compile_proc.stdout[:MAX_OUTPUT_LENGTH],
                "error_output": err_msg,
                "exit_code": compile_proc.returncode,
                "execution_time": round(compile_time, 3),
                "command_echo": compile_echo
            }

        # 2. Execute with java
        run_cmd = [JAVA_EXECUTABLE, "-cp", ".", class_name]
        full_echo = f"$ javac {class_name}.java\n$ java {class_name}"
        
        run_start_time = time.perf_counter()
        try:
            run_proc = subprocess.run(
                run_cmd,
                cwd=temp_dir,
                input=stdin_input,
                capture_output=True,
                text=True,
                timeout=timeout
            )
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "status": "timeout",
                "output": "",
                "error_output": f"Execution timed out after {timeout} seconds (possible infinite loop).",
                "exit_code": -1,
                "execution_time": timeout,
                "command_echo": full_echo
            }
        except FileNotFoundError:
            return {
                "success": False,
                "status": "system_error",
                "output": "",
                "error_output": f"Java runtime '{JAVA_EXECUTABLE}' not found on system PATH.",
                "exit_code": -1,
                "execution_time": round(compile_time, 3),
                "command_echo": full_echo
            }

        total_time = round(time.perf_counter() - run_start_time, 3)

        if run_proc.returncode != 0:
            return {
                "success": False,
                "status": "runtime_error",
                "output": run_proc.stdout[:MAX_OUTPUT_LENGTH],
                "error_output": run_proc.stderr[:MAX_OUTPUT_LENGTH],
                "exit_code": run_proc.returncode,
                "execution_time": total_time,
                "command_echo": full_echo
            }

        return {
            "success": True,
            "status": "success",
            "output": run_proc.stdout[:MAX_OUTPUT_LENGTH],
            "error_output": run_proc.stderr[:MAX_OUTPUT_LENGTH],
            "exit_code": 0,
            "execution_time": total_time,
            "command_echo": full_echo
        }

    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from config import PYTHON_EXECUTABLE, DEFAULT_TIMEOUT_SECONDS, MAX_OUTPUT_LENGTH

def execute_python_code(code: str, stdin_input: str = "", timeout: float = DEFAULT_TIMEOUT_SECONDS) -> dict:
    """
    Executes Python code in an isolated directory.
    Returns:
      success: bool
      status: str ('success', 'compilation_error', 'runtime_error', 'timeout', 'system_error')
      output: str
      error_output: str
      exit_code: int
      execution_time: float
      command_echo: str
    """
    temp_dir = tempfile.mkdtemp(prefix="codevanta_py_")
    command_echo = "$ python script.py"

    try:
        py_file_path = Path(temp_dir) / "script.py"
        with open(py_file_path, "w", encoding="utf-8") as f:
            f.write(code)

        run_cmd = [PYTHON_EXECUTABLE, "-u", "script.py"]
        start_time = time.perf_counter()

        try:
            proc = subprocess.run(
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
                "command_echo": command_echo
            }
        except FileNotFoundError:
            return {
                "success": False,
                "status": "system_error",
                "output": "",
                "error_output": f"Python executable '{PYTHON_EXECUTABLE}' not found on system PATH.",
                "exit_code": -1,
                "execution_time": 0.0,
                "command_echo": command_echo
            }

        execution_time = round(time.perf_counter() - start_time, 3)

        if proc.returncode != 0:
            # Check if syntax error or runtime error
            status = "compilation_error" if "SyntaxError" in proc.stderr or "IndentationError" in proc.stderr else "runtime_error"
            return {
                "success": False,
                "status": status,
                "output": proc.stdout[:MAX_OUTPUT_LENGTH],
                "error_output": proc.stderr[:MAX_OUTPUT_LENGTH],
                "exit_code": proc.returncode,
                "execution_time": execution_time,
                "command_echo": command_echo
            }

        return {
            "success": True,
            "status": "success",
            "output": proc.stdout[:MAX_OUTPUT_LENGTH],
            "error_output": proc.stderr[:MAX_OUTPUT_LENGTH],
            "exit_code": 0,
            "execution_time": execution_time,
            "command_echo": command_echo
        }

    finally:
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except Exception:
            pass

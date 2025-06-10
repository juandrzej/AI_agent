import os
import subprocess


def run_python_file(working_directory: str, file_path: str) -> str:
    try:
        target_file: str = os.path.join(working_directory, file_path)

        # Get absolute paths for comparison
        working_abs: str = os.path.abspath(working_directory)
        target_abs: str = os.path.abspath(target_file)

        # Normalize paths to ensure consistent comparison
        working_abs: str = os.path.normpath(working_abs)
        target_abs: str = os.path.normpath(target_abs)

        # Check if target is outside working directory
        if os.path.commonpath([working_abs, target_abs]) != working_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        # Check if target file exits
        if not os.path.exists(target_abs):
            return f'Error: File "{file_path}" not found.'

        # Check if target is python file
        if not target_abs.lower().endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        result = subprocess.run(
            ["python3", target_abs], timeout=30, capture_output=True, text=True
        )
        stdout: str = result.stdout
        stderr: str = result.stderr
        exit_code: int = result.returncode

        if not stdout and not stderr:
            return "No output produced."
        clean_result: str = f"STDOUT: {stdout} \nSTDERR: {stderr}"
        if exit_code != 0:
            clean_result += f"\nProcess exited with code {exit_code}"
        return clean_result

    except Exception as e:
        return f"Error: executing Python file: {e}"

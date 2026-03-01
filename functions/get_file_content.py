import os
from google.genai import types
from config import MAX_CHARS


def get_file_content(working_directory, file_path, line_start=1, line_end=None):
    try:
        # guardrail
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # read all lines
        with open(abs_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total_lines = len(lines)
        
        start_idx = max(0, line_start - 1)
        end_idx = total_lines if line_end is None else min(total_lines, line_end)

        if start_idx >= total_lines:
            return f"Error: line_start ({line_start}) exceeds total lines ({total_lines})"
        
        selected_lines = lines[start_idx:end_idx]
        content = "".join(selected_lines)

        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f"\n[...Content truncated at {MAX_CHARS} characters]"

        header = f"--- File: {file_path} (Lines {start_idx + 1} to {end_idx} of {total_lines}) ---\n"
        return header + content

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)
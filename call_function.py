from google.genai import types

from config import WORKING_DIR
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

# Map function names to actual implementations
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(function_call):
    function_name = function_call.name or ""
    if function_name not in function_map:
        return {"error": f"Unknown function: {function_name}"}
    
    args = {}
    if function_call.args:
        args = {k: v for k, v in function_call.args.items()}

    args["working_directory"] = WORKING_DIR

    try:
        function_result = function_map[function_name](**args)
        return function_result
    except Exception as e:
        return {"error": str(e)}
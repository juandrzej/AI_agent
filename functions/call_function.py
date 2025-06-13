from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .write_file import write_file
from .run_python_file import run_python_file


WORKING_DIRECTORY: str = "./calculator"
FUNCTIONS_DICT: dict = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


def call_function(
    function_call_part: types.FunctionCall, verbose=False
) -> types.Content:
    attr_err: bool = False
    try:
        function_name: str = function_call_part.name
        function_args: dict = dict(function_call_part.args)
        function_args.pop("working_directory", None)
    except AttributeError:
        function_name: str = function_call_part
        attr_err = True

    if function_name not in FUNCTIONS_DICT or attr_err:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    function = FUNCTIONS_DICT[function_name]
    function_result = function(working_directory=WORKING_DIRECTORY, **function_args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


if __name__ == "__main__":
    print(call_function("test"))

import os

MAX_CHARS: int = 10000


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        target_file: str = os.path.join(working_directory, file_path)

        # Get absolute paths for comparison
        working_abs: str = os.path.abspath(working_directory)
        target_abs: str = os.path.abspath(target_file)

        # Normalize paths to ensure consistent comparison
        working_abs: str = os.path.normpath(working_abs)
        target_abs: str = os.path.normpath(target_abs)

        # Check if target is outside working directory
        # The target should either be the working directory itself or start with working_directory + separator
        if not target_abs.startswith(working_abs + os.sep):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if target is actually a file
        if not os.path.isfile(target_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_abs, "r") as f:
            content = f.read(MAX_CHARS)
            # Try to read one more character to see if there's more content
            remaining_content = f.read(1)

            if remaining_content:  # If there's any content left, the file was truncated
                content += f'[...File "{file_path}" truncated at 10000 characters]'

            return content

    except Exception as e:
        return f"Error: {str(e)}"

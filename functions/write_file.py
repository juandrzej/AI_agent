import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
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
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Check if the directory exist, if not create it
        target_dir: str = os.path.split(target_abs)[0]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with open(target_abs, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"

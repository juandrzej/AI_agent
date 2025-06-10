import os


def get_files_info(working_directory, directory=None):
    try:
        # If directory is None, use the working directory
        if directory is None:
            target_directory = working_directory
        else:
            # Join the directory with working_directory to get the full path
            target_directory = os.path.join(working_directory, directory)

        # Get absolute paths for comparison
        working_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(target_directory)

        # Normalize paths to ensure consistent comparison
        working_abs = os.path.normpath(working_abs)
        target_abs = os.path.normpath(target_abs)

        # Check if target is outside working directory
        # The target should either be the working directory itself or start with working_directory + separator
        if target_abs != working_abs and not target_abs.startswith(
            working_abs + os.sep
        ):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Check if target is actually a directory
        if not os.path.isdir(target_abs):
            return f'Error: "{directory}" is not a directory'

        # Get directory contents
        items = os.listdir(target_abs)
        result_lines = []

        for item in items:
            item_path = os.path.join(target_abs, item)
            file_size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)

            line = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            result_lines.append(line)

        return "\n".join(result_lines)

    except Exception as e:
        return f"Error: {str(e)}"

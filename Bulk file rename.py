import os
import shutil
from pathlib import Path

def backup_files(directory, backup_directory):
    """
    Create a backup of files in the specified directory.

    Args:
        directory (str): Source directory to backup files from.
        backup_directory (str): Directory where the backup will be stored.

    Returns:
        None
    """
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)

    for entry in os.scandir(directory):
        if entry.is_file():
            shutil.copy2(entry.path, backup_directory)
            print(f"Backed up: {entry.name}")

def restore_files(directory, backup_directory):
    """
    Restore files from the backup directory to the specified directory.

    Args:
        directory (str): Target directory to restore files to.
        backup_directory (str): Directory containing the backup files.

    Returns:
        None
    """
    for entry in os.scandir(backup_directory):
        if entry.is_file():
            new_filename = os.path.splitext(entry.name)[0]
            old_filepath = entry.path
            new_filepath = os.path.join(directory, new_filename)
            try:
                os.rename(old_filepath, new_filepath)
                print(f"Restored: {entry.name} --> {new_filename}")
            except Exception as e:
                print(f"Error restoring {entry.name}: {str(e)}")

def bulk_rename(directory, prefix, extension_filter=None, preview=False, interactive=False, backup=False):
    """
    Bulk rename files in the specified directory.

    Args:
        directory (str): Directory where the files to be renamed are located.
        prefix (str): Prefix to be added to the new filenames.
        extension_filter (str, optional): Filter for specific file extensions. Defaults to None.
        preview (bool, optional): If True, preview the renaming without actually renaming the files. Defaults to False.
        interactive (bool, optional): If True, prompt for user confirmation in case of conflicts. Defaults to False.
        backup (bool, optional): If True, create a backup of the original files. Defaults to False.

    Returns:
        None
    """
    directory_path = Path(directory)
    backup_directory = directory_path / "backup"

    if backup:
        os.makedirs(backup_directory, exist_ok=True)
        backup_files(directory, backup_directory)

    renamed_files = []
    counter = 1

    for entry in os.scandir(directory_path):
        if entry.is_file():
            file_extension = entry.suffix
            if not extension_filter or file_extension.lower() == extension_filter.lower():
                new_filename = f"{prefix}_{counter:03}{file_extension}"
                new_filepath = directory_path / new_filename
                if preview:
                    print(f"Preview - Renaming: {entry.name} --> {new_filename}")
                else:
                    if interactive and new_filepath.exists():
                        choice = input(f"Conflict: {new_filename} already exists. Replace it? (y/n): ")
                        if choice.lower() != 'y':
                            print(f"Skipped: {entry.name}")
                            continue
                    try:
                        os.rename(entry.path, new_filepath)
                        renamed_files.append((entry.name, new_filename))
                        print(f"Renamed: {entry.name} --> {new_filename}")
                    except Exception as e:
                        print(f"Error renaming {entry.name}: {str(e)}")
                counter += 1

    if not preview and len(renamed_files) > 0:
        print("\nSummary:")
        for old_name, new_name in renamed_files:
            print(f"{old_name} --> {new_name}")

    if backup:
        restore_option = input("Do you want to restore the original filenames? (y/n): ")
        if restore_option.lower() == "y":
            restore_files(directory, backup_directory)
        shutil.rmtree(backup_directory)

def filter_files_by_size(directory, size_limit):
    """
    Filter files in the specified directory based on their size.

    Args:
        directory (str): Directory to filter files from.
        size_limit (int): Maximum size in bytes for the files to be included.

    Returns:
        List[str]: List of file paths that meet the size criteria.
    """
    filtered_files = []

    for entry in os.scandir(directory):
        if entry.is_file() and entry.stat().st_size <= size_limit:
            filtered_files.append(entry.path)
            print(f"Filtered: {entry.name} (Size: {entry.stat().st_size} bytes)")

    return filtered_files

def sort_files(directory):
    """
    Sort and print files in the specified directory.

    Args:
        directory (str): Directory to sort files in.

    Returns:
        None
    """
    file_list = sorted(Path(directory).iterdir())
    for entry in file_list:
        if entry.is_file():
            print(entry.name)

def count_files(directory):
    """
    Count and print the total number of files in the specified directory.

    Args:
        directory (str): Directory to count files in.

    Returns:
        None
    """
    file_count = sum(1 for entry in os.scandir(directory) if entry.is_file())
    print(f"Total files: {file_count}")

# Example usage
directory_path = "/path/to/directory"  # Replace with the target directory path
new_prefix = "new_prefix"  # Replace with the desired prefix
file_extension_filter = ".txt"  # Replace with the desired file extension filter (e.g., ".txt", ".jpg"). Set to None to disable filtering.
preview_mode = True  # Set to True to preview the renaming without actually performing it, or False to perform the renaming.
interactive_mode = True  # Set to True to prompt for user confirmation in case of conflicts, or False to automatically replace conflicting files.
backup_mode = True  # Set to True to create a backup of the original files, or False to skip the backup.

bulk_rename(directory_path, new_prefix, file_extension_filter, preview_mode, interactive_mode, backup_mode)

# Additional function usage
filtered_files = filter_files_by_size(directory_path, 1024)  # Filter files smaller than or equal to 1KB
sort_files(directory_path)  # Sort files in the directory
count_files(directory_path)  # Count the total number of files in the directory
import os
import shutil

def backup_files(directory, backup_directory):
    if not os.path.exists(backup_directory):
        os.makedirs(backup_directory)
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            shutil.copy2(os.path.join(directory, filename), backup_directory)
            print(f"Backed up: {filename}")

def restore_files(directory, backup_directory):
    for filename in os.listdir(backup_directory):
        if os.path.isfile(os.path.join(backup_directory, filename)):
            new_filename = os.path.splitext(filename)[0]
            old_filepath = os.path.join(backup_directory, filename)
            new_filepath = os.path.join(directory, new_filename)
            try:
                os.rename(old_filepath, new_filepath)
                print(f"Restored: {filename} --> {new_filename}")
            except Exception as e:
                print(f"Error restoring {filename}: {str(e)}")

def bulk_rename(directory, prefix, extension_filter=None, preview=False, interactive=False, backup=False):
    counter = 1
    renamed_files = []
    backup_directory = None

    if backup:
        backup_directory = os.path.join(directory, "backup")
        backup_files(directory, backup_directory)

    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            file_extension = os.path.splitext(filename)[1]
            if extension_filter is None or file_extension.lower() == extension_filter.lower():
                new_filename = f"{prefix}_{counter:03}{file_extension}"
                old_filepath = os.path.join(directory, filename)
                new_filepath = os.path.join(directory, new_filename)
                if preview:
                    print(f"Preview - Renaming: {filename} --> {new_filename}")
                else:
                    if interactive and os.path.exists(new_filepath):
                        choice = input(f"Conflict: {new_filename} already exists. Replace it? (y/n): ")
                        if choice.lower() != 'y':
                            print(f"Skipped: {filename}")
                            continue
                    try:
                        os.rename(old_filepath, new_filepath)
                        renamed_files.append((filename, new_filename))
                        print(f"Renamed: {filename} --> {new_filename}")
                    except Exception as e:
                        print(f"Error renaming {filename}: {str(e)}")
                counter += 1
    
    if not preview and len(renamed_files) > 0:
        print("\nSummary:")
        for old_name, new_name in renamed_files:
            print(f"{old_name} --> {new_name}")

    if backup and backup_directory:
        restore_option = input("Do you want to restore the original filenames? (y/n): ")
        if restore_option.lower() == "y":
            restore_files(directory, backup_directory)
        shutil.rmtree(backup_directory)

# Example usage
directory_path = "/path/to/directory"  # Replace with the target directory path
new_prefix = "new_prefix"  # Replace with the desired prefix
file_extension_filter = ".txt"  # Replace with the desired file extension filter (e.g., ".txt", ".jpg"). Set to None to disable filtering.
preview_mode = True  # Set to True to preview the renaming without actually performing it, or False to perform the renaming.
interactive_mode = True  # Set to True to prompt for user confirmation in case of conflicts, or False to automatically replace conflicting files.
backup_mode = True  # Set to True to create a backup of the original files, or False to skip the backup.

bulk_rename(directory_path, new_prefix, file_extension_filter, preview_mode, interactive_mode, backup_mode)
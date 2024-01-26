import os
import datetime
import shutil
import plistlib
import xattr


def get_file_info(file_path, school):
    """
    Retrieve key information about a file including its size, creation time, name, type and the source of download if available.

    Args:
        file_path: The path to the file.
        school: the name of the school to check in the file's download source (can be None).

    Returns:
        A dictionary containing file information.
    """
    file_size = os.path.getsize(file_path)
    file_create_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
    file_name, file_type = os.path.splitext(file_path)
    file_download_from = ""
    try:
        # Extract extended attributes to find out the file's download source if available
        attr_data = plistlib.loads(
            xattr.getxattr(file_path, "com.applemetadata:kMDItemWhereFroms")
        )
        file_download_from = attr_data[0]
        if school in file_download_from:
            file_download_from = "School"
    except OSError as error:
        print(error)

    return {
        "File Size": file_size,
        "File Created Time": file_create_time,
        "File Name": os.path.basename(file_name),
        "File Type": file_type,
        "File Downloaded From": file_download_from,
    }


def create_directory(path):
    """
    Create a new directory if it doesn't exist.

    Args:
        path : The path where the directory is to created.

    Returns:
        True if derectory is created or exists, False if an error occurred.
    """
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError as error:
        print(f"Cannot create folder at {path}: {error}")
        return False
    return True


def move_file(source, destination):
    """
    Move a file from the source path to the destination path.

    Args:
        source : Path of the source file.
        destination : Path where the file needs to be moved.
    """
    try:
        shutil.move(source, destination)
        print(f"File moved from {source} to {destination}")
    except OSError as error:
        print(error)


def category_file(directory_path, source_path, file_type, file_from):
    """
    Categorize and move a file based on its type and download source.

    Args:
        directory_path : The base directory path where files are being stored.
        source_path : The source path of the file.
        file_type : The type of the file.
        file_from : The source from where the file was downloaded if available.
    """
    destination_path = ""
    file_formats = {
        "Image": [".JPEG", ".PNG", ".GIF", ".BMP", ".SVG"],
        "Audio": [".MP3", ".WAV", ".AAC", ".FLAC"],
        "Video": [".MP4", ".AVI", ".MOV", ".WMV"],
        "Document": [".PDF", ".DOC", ".PPT", ".DOCX", ".PPTX"],
        "Other": [".ZIP", ".HTML", ".XML", ".RAR"],
    }

    # Determine the destination path based on the file type and source
    if file_from == "School":
        destination_path = os.path.join(directory_path, "School")
    else:
        for category, ftype in file_formats.items():
            if file_type.upper() in ftype:
                destination_path = os.path.join(directory_path, category)
        if destination_path == "":
            destination_path = os.path.join(directory_path, "Other")

    # Create the destination directory and move the file
    if create_directory(destination_path):
        move_file(source_path, destination_path)


def list_files_in_folder(directory_path, school_name):
    """
    List and categorize all files in a given folder.

    Args:
        directory_path : The path of the directory to organize.
        school_name : The name of the school to check if file was downloaded from a education domain.
    """
    if os.path.exists(directory_path):
        for file_name in os.listdir(directory_path):
            full_path = os.path.join(directory_path, file_name)
            if os.path.isfile(full_path):
                info = get_file_info(full_path, school_name)
                category_file(
                    directory_path, full_path, info["File Type"], info["File Downloaded From"]
                )
    else:
        print("Directory path doesn't exist")
    print("File move has finished")


if __name__ == "__main__":
    school_name = input("Please enter you school name: ")
    directory_path = input("Please enter the path of the folder you want to organize: ")
    list_files_in_folder(directory_path, school_name)

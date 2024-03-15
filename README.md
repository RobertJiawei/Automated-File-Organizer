# File Organizer

---

**The idea of this project is to tackle the issue of my Mac's download folder becoming cluttered. The goal is to create a program that helps organize the folder by automatically sorting files into sub-folders based on their type. Additionally, it will categorize files that are downloaded frm my school, making it easier to keep everything well-organized and accessible.**

*The File Organizer is a Python application with a Tkinter GUI that helps you to categorize and organize your files into folders based on their file type and, optionally, their download source.*

## Features

- **Directory Selection**: Easily select the folder you want to organize with a simple file dialog.
- **File Type Organization**: Choose from a range of file types such as images, documents, audio, and more to categorize files into folders.
- **School File Detection**: Input your school name to detect and organize files downloaded from your school's domain.
- **Output Log**: View real-time updates and outcomes of the organization process in the integrated output log window.

## Libraries

```python
import os, datetime, shutil, plistlib, xattr
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
```

## Usage

1. **Start Application**: Run the script using Python.

   ```python
   python file_organizer.py
   ```

2. **Select Directory**: Click the "Browse" button to choose the directory you want to organize.

3. **Enter School Name**: (Optional) Enter the name of your school to organize files downloaded from the school's domain.

4. **Select File Types**: Check the file types you want to organize.

5. **Organize Files**: Click the "Organize Files" button to start the organization process.

6. **View Output**: Check the output text field at the bottom of the application window for results and any error messages.

---

## Demo

https://github.com/RobertJiawei/File-Organizer/assets/29966757/5ece85b0-250f-4534-b119-4e9158d0ec5e

---

*I've set up a few pre-defined folders to store different file types.*

```python
file_formats = {
            "IMAGE": [".jpg",".jpeg",".png",".gif",".bmp",".tiff",".svg",".mov",".heic",".webm",".avif",],
            "DOCUMENT": [".doc",".docx",".pdf",".ppt",".pptx",".xls",".xlsx",".txt",".rtf"],
            "AUDIO": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
            "VIDEO": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
            "ARCHIVE": [".zip", ".rar", ".7z", ".tar.gz", ".tar"],
            "EXECUTABLE": [".exe", ".dmg", ".apk", ".deb", ".rpm"],
            "CODE": [".html",".css",".js",".py",".java",".cpp",".json",".xml",".md",".yml",".yaml",".go",".rb",".php",".swift",".c",".h",".pl",".lua",".scala",".ts"],
            "SPREADSHEET": [".csv", ".db", ".sqlite", ".sql"]
            }
```

*There's also a specific folder dedicated to files downloaded from my school's website.*

```python
# Extract extended attributes to find out the file's download source if available
attr_data = plistlib.loads(
            xattr.getxattr(file_path, "com.applemetadata:kMDItemWhereFroms")
        )
        file_download_from = attr_data[0]
```

import os
import datetime
import shutil
import plistlib
import xattr
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class FileOrganizerGUI:
    def __init__(self, master):
        master.title("File Organizer")
        master.geometry("600x600")

        self.label_directory = tk.Label(master, text="Select Directory:")
        self.label_directory.pack()

        self.entry_directory = tk.Entry(master, width=50)
        self.entry_directory.pack()

        self.button_browse = tk.Button(master, text="Browse", command=self.browse_directory)
        self.button_browse.pack()

        self.label_school_name = tk.Label(master, text="School Name:")
        self.label_school_name.pack()

        self.entry_school_name = tk.Entry(master)
        self.entry_school_name.pack()

        self.label_file_types = tk.Label(master, text="Select File Types to Organize:")
        self.label_file_types.pack()

        self.file_types = [
            "IMAGE",
            "DOCUMENT",
            "AUDIO",
            "VIDEO",
            "ARCHIVE",
            "EXECUTABLE",
            "CODE",
            "SPREADSHEET",
        ]
        self.file_types_vars = {}
        for ftype in self.file_types:
            self.file_types_vars[ftype] = tk.BooleanVar()
            ttk.Checkbutton(master, text=ftype, variable=self.file_types_vars[ftype]).pack()

        self.button_organize = tk.Button(
            master, text="Organize Files", command=self.organize_files
        )
        self.button_organize.pack()

        self.output_label = tk.Label(master, text="Output:")
        self.output_label.pack(pady=(10, 0))  # Add some padding above the label

        self.output_text = tk.Text(master, height=15, width=70)
        self.output_text.pack()

        self.scrollbar = tk.Scrollbar(master, command=self.output_text.yview)
        self.output_text.config(yscrollcommand=self.scrollbar.set)

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.entry_directory.delete(0, tk.END)
        self.entry_directory.insert(0, directory)

    def organize_files(self):
        directory = self.entry_directory.get()
        school_name = self.entry_school_name.get()
        file_formats = {
            "IMAGE": [
                ".jpg",
                ".jpeg",
                ".png",
                ".gif",
                ".bmp",
                ".tiff",
                ".svg",
                ".mov",
                ".heic",
                ".webm",
                ".avif",
            ],
            "DOCUMENT": [
                ".doc",
                ".docx",
                ".pdf",
                ".ppt",
                ".pptx",
                ".xls",
                ".xlsx",
                ".txt",
                ".rtf",
            ],
            "AUDIO": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
            "VIDEO": [".mp4", ".avi", ".mkv", ".mov", ".wmv"],
            "ARCHIVE": [".zip", ".rar", ".7z", ".tar.gz", ".tar"],
            "EXECUTABLE": [".exe", ".dmg", ".apk", ".deb", ".rpm"],
            "CODE": [
                ".html",
                ".css",
                ".js",
                ".py",
                ".java",
                ".cpp",
                ".json",
                ".xml",
                ".md",
                ".yml",
                ".yaml",
                ".go",
                ".rb",
                ".php",
                ".swift",
                ".c",
                ".h",
                ".pl",
                ".lua",
                ".scala",
                ".ts",
            ],
            "SPREADSHEET": [".csv", ".db", ".sqlite", ".sql"],
        }
        selected_file_types = [
            ftype for ftype, var in self.file_types_vars.items() if var.get()
        ]

        pass_file_type = {
            ftype: formats
            for ftype, formats in file_formats.items()
            if ftype in selected_file_types
        }

        if directory and selected_file_types:
            self.list_files_in_folder(directory, school_name, pass_file_type)
        else:
            messagebox.showwarning(
                "Warning", "Please select a directory and at least one file type."
            )

    def update_output(self, message):
        self.output_text.insert(tk.END, message + "\n\n")
        self.output_text.see(tk.END)

    def get_file_info(self, file_path, school):
        file_size = os.path.getsize(file_path)
        file_create_time = datetime.datetime.fromtimestamp(os.path.getctime(file_path))
        file_name, file_type = os.path.splitext(file_path)
        file_download_from = ""
        try:
            attr_data = plistlib.loads(
                xattr.getxattr(file_path, "com.applemetadata:kMDItemWhereFroms")
            )
            file_download_from = attr_data[0]
            if school in file_download_from:
                file_download_from = "School"
        except OSError as error:
            self.update_output(str(error))

        return {
            "File Size": file_size,
            "File Created Time": file_create_time,
            "File Name": os.path.basename(file_name),
            "File Type": file_type,
            "File Downloaded From": file_download_from,
        }

    def create_directory(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(path)
        except OSError as error:
            self.update_output(f"Cannot create folder at {path}: {str(error)}")
            return False
        return True

    def move_file(self, source, destination):
        try:
            shutil.move(source, destination)
            self.update_output(f"File moved from {source} to {destination}")
        except OSError as error:
            self.update_output(str(error))

    def category_file(self, directory_path, source_path, file_type, file_from, pass_file_type):
        destination_path = ""

        if file_from == "School":
            destination_path = os.path.join(directory_path, "School")
        else:
            for category, ftype in pass_file_type.items():
                if file_type.lower() in ftype:
                    destination_path = os.path.join(directory_path, category)
            if destination_path == "":
                destination_path = os.path.join(directory_path, "Other")

        if self.create_directory(destination_path):
            self.move_file(source_path, destination_path)

    def list_files_in_folder(self, directory_path, school_name, pass_file_type):
        if os.path.exists(directory_path):
            for file_name in os.listdir(directory_path):
                full_path = os.path.join(directory_path, file_name)
                if os.path.isfile(full_path):
                    info = self.get_file_info(full_path, school_name)
                    self.category_file(
                        directory_path,
                        full_path,
                        info["File Type"],
                        info["File Downloaded From"],
                        pass_file_type,
                    )
        else:
            messagebox.showerror("Error", "Directory path doesn't exist")
            self.update_output("Directory path doesn't exist")
        messagebox.showinfo("Success", "File organization has finished.")
        self.update_output("File organization has finished.")


def main():
    root = tk.Tk()
    app = FileOrganizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

# Automated File Organizer
---
**The idea of this project is to tackle the issue of my Mac's download folder becoming cluttered. The goal is to create a program that helps organize the folder by automatically sorting files into sub-folders based on their type. Additionally, it will categorize files that are downloaded frm my school, making it easier to keep everything well-organized and accessible.**

Python program will scan all files in a user-defined folder and categorizes these files by type (eg. Image, Audio, Video, Document) and then moves them to corresponding sub-folders.


*I've set up a few pre-defined folders to store different file types.*
```
file_formats = {
        "Image": [".JPEG", ".PNG", ".GIF", ".BMP", ".SVG"],
        "Audio": [".MP3", ".WAV", ".AAC", ".FLAC"],
        "Video": [".MP4", ".AVI", ".MOV", ".WMV"],
        "Document": [".PDF", ".DOC", ".PPT", ".DOCX", ".PPTX"],
        "Other": [".ZIP", ".HTML", ".XML", ".RAR"],
    }
```

*There's also a specific folder dedicated to files downloaded from my school's website.* 
```
# Extract extended attributes to find out the file's download source if available
attr_data = plistlib.loads(
            xattr.getxattr(file_path, "com.applemetadata:kMDItemWhereFroms")
        )
        file_download_from = attr_data[0]
```

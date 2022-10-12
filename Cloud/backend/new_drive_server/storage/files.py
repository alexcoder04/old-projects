from flask import request
import os
from ..config import config

TEMP_PATH = config.get("TEMP_PATH")
USER_FILES_PATH = config.get("USER_FILES_PATH")
IMAGE_FILE_EXTENSIONS = [
    "png", "jpg", "jpeg", "gif", "bmp"
]
MUSIC_FILE_EXTENSIONS = [
    "mp3", "wav", "ogg"
]
OTHER_FILE_EXTENSIONS = [
    "pdf", "txt", "md", "mp4", "mov", "avi", "mkv"
]
ALLOWED_FILE_EXTENSIONS = IMAGE_FILE_EXTENSIONS + MUSIC_FILE_EXTENSIONS + OTHER_FILE_EXTENSIONS
IMAGE_COMPRESSED_RESOLUTION = config.get("IMAGE_COMPRESSED_RESOLUTION")

def valid_file():
    if "file" not in request.files or request.files["file"].filename == "":
        return False
    if os.path.splitext(request.files["file"].filename)[1].lower() not in ALLOWED_FILE_EXTENSIONS:
        return False
    return True

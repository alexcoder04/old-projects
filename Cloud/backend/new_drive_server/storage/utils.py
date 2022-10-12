from flask import request
import os
from PIL import Image
from .files import *
from ..config import config
from ..database import db

def init_temp():
    for directory in [TEMP_PATH, os.path.join(TEMP_PATH, "users")]:
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass
    for user in db.get_all_users():
        try:
            os.mkdir(os.path.join(TEMP_PATH, "users", user))
        except FileExistsError:
            pass

def generate_thumbnail(user, folder, file):
    orig_img = Image.open(os.path.join(USER_FILES_PATH, user, folder, file))
    compressed_img = orig_img.resize(config.get("IMAGE_COMPRESSED_RESOLUTION"))
    directory = os.path.join(USER_FILES_PATH, user, "thumbnails", folder)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    compressed_img.save(
            os.path.join(directory, file),
            optimize=True,
            quality=5
        )

def delete_thumbnail(user, file):
    os.remove(os.path.join(USER_FILES_PATH, user, "thumbnails", file))

def get_file_type_by_extension(ext):
    ext = ext[1:]
    if ext in IMAGE_FILE_EXTENSIONS:
        return "image"
    if ext in MUSIC_FILE_EXTENSIONS:
        return "music"
    return ""

def compress_folder(user, path):
    foldername = path.split("/")[-1]
    path_to_folder = os.path.join(USER_FILES_PATH, user, path)
    path_to_out = os.path.join(TEMP_PATH, "users", user, foldername + ".zip")
    os.system(f"cd {USER_FILES_PATH}/{user}; zip $(realpath --relative-to=. {path_to_out}) $(realpath --relative-to=. {path_to_folder})/*")
    return os.path.join(TEMP_PATH, "users", user), foldername + ".zip"
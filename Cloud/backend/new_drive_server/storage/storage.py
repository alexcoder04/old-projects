from ..auth import login_manager
from .utils import delete_thumbnail, get_file_type_by_extension
from .files import *
import os
from shutil import rmtree

class Storage:
    def init_user(self, username: str):
        for directory in ["", "root", "thumbnails", "temp"]:
            os.mkdir(os.path.join(USER_FILES_PATH, username, directory))

    def listdir(self, user: str, dirname: str):
        raw_list = os.listdir(os.path.join(USER_FILES_PATH, user, dirname))
        content = []
        for e in raw_list:
            if os.path.isdir(os.path.join(USER_FILES_PATH, user, dirname, e)):
                content.append({ "name": e, "type": "folder", "size": None })
                continue

            content.append({
                "name": e,
                "type": get_file_type_by_extension(os.path.splitext(e)[1]),
                "size": os.path.getsize(os.path.join(USER_FILES_PATH, user, dirname, e)),
                "last_modified": os.path.getmtime(os.path.join(USER_FILES_PATH, user, dirname, e))
            })
            
        return content

    def create_folder(self, user: str, folder: str):
        if not os.path.exists(os.path.join(USER_FILES_PATH, user, folder)):
            os.mkdir(os.path.join(USER_FILES_PATH, user, folder))
        return None
    
    def delete_folder(self, user: str, folder: str):
        rmtree(os.path.join(USER_FILES_PATH, user, folder))
    
    def delete_file(self, user: str, file: str):
        if get_file_type_by_extension(os.path.splitext(file)[1]) == "image":
            delete_thumbnail(user, file)
        os.remove(os.path.join(USER_FILES_PATH, user, file))
    
    def get_user_magnans(self, user):
        return os.listdir(os.path.join(
            USER_FILES_PATH,
            user
        ))
    
    def exists(self, user, path):
        print(user, path)
        print(os.path.join(
            USER_FILES_PATH,
            user,
            path
        ))
        return os.path.exists(os.path.join(
            USER_FILES_PATH,
            user,
            path
        ))
    
    def isfile(self, user, path):
        return os.path.isfile(os.path.join(
            USER_FILES_PATH,
            user,
            path
        ))
    
    def isdir(self, user, path):
        return os.isdir(os.path.join(
            USER_FILES_PATH,
            user,
            path
        ))
    
    def rename(self, user, origin, destin):
        os.rename(
            os.path.join(USER_FILES_PATH, user, origin),
            os.path.join(USER_FILES_PATH, user, destin)
        )

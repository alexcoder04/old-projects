from flask import jsonify, request, redirect, url_for
import json
import os
from ..utils import message_success, message_error, get_path, verify_user
from ..storage import storage
from ..database import shared_files_db

def make_validation():
    data = request.get_json()
    path = get_path(data)
    user = verify_user(data)
    if not path or not user:
        valid = False
    else:
        valid = True
    return valid, data, path, user

def initialize_storage(app):
    # read
    @app.route("/storage/read/<action>", methods=["POST"])
    def storage_api_read(action):
        valid, data, path, user = make_validation()

        if not valid: return message_error("Bad request", 400)
        
        if action == "list-folder":
            content = storage.listdir(user, path)
            folders, files = [], []
            for el in content:
                if el["type"] == "folder":
                    folders.append(el)
                    continue
                files.append(el)
            return jsonify({ "files": files, "folders": folders })
        
        return message_error("Invalid action", 400)

    # create
    @app.route("/storage/create/<action>", methods=["POST"])
    def storage_api_create(action):
        valid, data, path, user = make_validation()

        if not valid: return message_error("Bad request", 400)

        if action == "folder":
            if ".." in path: return message_error("Bad folder name", 400)
            if path.startswith("/"): path = path[1:]
            storage.create_folder(user, path)
            return message_success(201)
        
        return message_error("Invalid action", 400)

    # delete
    @app.route("/storage/delete/<action>", methods=["POST"])
    def storage_api_delete(action):
        valid, data, path, user = make_validation()
        
        if not valid: return message_error("Bad request", 400)

        if ".." in path: return message_error("Bad file name", 400)
        if path in storage.get_user_magnans(user): return message_error("Bad file name", 400)
        if not storage.exists(user, path): return message_error("File does not exist", 400)
        if path.startswith("/"): path = path[1:]

        if action == "folder":
            storage.delete_folder(user, path)
            return message_success()
        
        if action == "file":
            storage.delete_file(user, path)
            return message_success()
        
        return message_error("Invalid action", 400)

    # move
    @app.route("/storage/move/<action>", methods=["POST"])
    def storage_api_move(action):
        valid, data, path, user = make_validation()
        destin = data["destination"]

        if not valid: return message_error("Bad request", 400)

        if action != "file" and action != "folder": return message_error("Invalid action", 400)

        if ".." in path: return message_error("Bad file name", 400)
        if path in storage.get_user_magnans(user): return message_error("Bad file name", 400)
        if not storage.exists(user, path): return message_error("File does not exist", 400)
        if path.startswith("/"): path = path[1:]

        if action == "file":
            if not storage.isfile(user, path):
                return message_error("Bad file name", 400)
            if os.path.splitext(path)[1] != os.path.splitext(destin)[1]:
                destin = destin + os.path.splitext(path)[1]
        
        if action == "folder":
            if not storage.isdir(user, path):
                return message_error("Folder does not exist", 400)

        storage.rename(user, path, destin)

        return message_success()

    # share
    @app.route("/storage/share", methods=["POST"])
    def storage_api_share():
        valid, data, path, user = make_validation()
        
        if not valid: return message_error("Bad request", 400)

        link = shared_files_db.create_link(user, path)
        return jsonify({
            "link": link
        })

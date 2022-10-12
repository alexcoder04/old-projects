from flask import Blueprint, send_from_directory, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import json
from ..auth import login_manager
from ..utils import message_error, message_success
from ..database import shared_files_db
from .utils import valid_file, generate_thumbnail, compress_folder
from .files import *
from . import *

app = Blueprint("storage", __name__)

@app.route("/file/<username>/<path:folder>/<filename>")
def file(username, folder, filename):
    if login_manager.is_logged_in():
        current_user = login_manager.get_username()
        if current_user == username:
            return send_from_directory(os.path.join(USER_FILES_PATH, username, folder), filename)
    return message_error("Not authorized", 401)

@app.route("/thumbnail/<username>/<path:folder>/<filename>")
def thumbnail(username, folder, filename):
    if not filename.rsplit(".", 1)[1].lower() in IMAGE_FILE_EXTENSIONS:
        return message_error("No preview available", 400)
    if username != login_manager.get_username():
        return message_error("Not authorized", 401)
    thumbnail_folder = os.path.join(USER_FILES_PATH, username, "thumbnails", folder)
    if not os.path.isfile(os.path.join(thumbnail_folder, filename)):
        generate_thumbnail(username, folder, filename)
    return send_from_directory(thumbnail_folder, filename)

@app.route("/download/folder/<user>/<path:path>")
def download(user, path):
    if user != login_manager.get_username():
        return message_error("Not authorized", 401)
    folder, file = compress_folder(user, path)
    return send_from_directory(folder, file)

@app.route("/shared/<uuid>")
def shared(uuid):
    data = shared_files_db.get_data_for_id(uuid)
    if data is None:
        return message_error("This file does not exist")
    path = data["path"].rsplit("/", 1)
    return send_from_directory(os.path.join(USER_FILES_PATH, data["user"], path[0]), path[1])

@app.route("/upload", methods=["POST"])
def upload():
    if not valid_file():
        return redirect(url_for("views.error", message="No file was specified"))
    
    file = request.files["file"]
    filename = secure_filename(file.filename)
    username = login_manager.get_username()
    folder = request.form.get("current_folder")

    if not username:
        return redirect(url_for("views.error", message="No username provided"))
     
    file.save(os.path.join(USER_FILES_PATH, username, folder, filename))
    return redirect(url_for("views.mystuff", path=folder))

@app.route("/")
def index():
    return message_error("Not found", 404)

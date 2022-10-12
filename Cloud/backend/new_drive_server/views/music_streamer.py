from flask import Blueprint, render_template, redirect, url_for, request, send_from_directory, jsonify
from ..storage import storage
from ..auth import login_manager
from ..config import config
from ..utils import get_server_ip
from random import choice
import os
import subprocess

MUSIC_FILES_DIR = config.get("MUSIC_FOLDER")
CUSTOM_MUSIC_FILES_DIR = os.path.join(MUSIC_FILES_DIR, ".pimusic")
if not os.path.isdir(CUSTOM_MUSIC_FILES_DIR): os.mkdir(CUSTOM_MUSIC_FILES_DIR)

app = Blueprint("streamer", __name__, template_folder="templates")

def get_all_songs():
    l = list(filter(
        lambda el: el.endswith(".mp3"), subprocess.check_output(['find', MUSIC_FILES_DIR]).decode("utf-8").split("\n")
    ))
    return l

@app.route("/stream")
def index():
    if not login_manager.is_logged_in():
        return redirect(url_for("views.login", next="/module/streamer/stream"))
    return render_template(
        "modules/music_streamer/index.html",
        songs=get_all_songs(),
        music_root=MUSIC_FILES_DIR,
        static_server=f"http://{get_server_ip()}:{config.get('STATIC_SERVER_PORT')}/magnan/"
    )

@app.route("/song")
def song():
    name = request.args.get("song")
    if not name.startswith(MUSIC_FILES_DIR) or ".." in name:
        return jsonify({ "status": "error" }), 400
    name = name.rsplit("/", 1)
    return send_from_directory(name[0], name[1])

@app.route("/dl")
def dl():
    url = request.args.get("url")
    if os.system(f"youtube-dl -x --audio-format 'mp3' -o '{CUSTOM_MUSIC_FILES_DIR}/%(title)s.%(ext)s' '{url}'") != 0:
        return jsonify({ "status": "error" }), 500
    return jsonify({ "status": "success" })

@app.route("/random-song")
def random_song():
    if not login_manager.is_logged_in():
        return redirect(url_for("views.login"))
    song = choice(get_all_songs())
    return redirect(url_for("streamer.song", song=song))

@app.route("/radio")
def radio():
    return render_template("modules/music_streamer/radio.html")

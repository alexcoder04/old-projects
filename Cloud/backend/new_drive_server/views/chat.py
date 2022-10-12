from flask import Blueprint, render_template, redirect, url_for, request
from ..utils import get_server_ip
from ..config import config
from ..auth import login_manager
from ..database import OpenDB
import os
import json
from datetime import datetime

app = Blueprint("chat", __name__, template_folder="templates", static_folder="static")

db = OpenDB("ChatRooms", [
    {
        "name": "uuid",
        "type": "VARCHAR(255)",
        "args": "UNIQUE NOT NULL"
    },
    {
        "name": "messages_file",
        "type": "VARCHAR(255)",
        "args": "NOT NULL"
    },
    {
        "name": "users",
        "type": "VARCHAR(255)",
        "args": ""
    }
])

def get_room_info(room_id):
    res = db.search({"uuid": room_id})
    return res

@app.route("/send", methods=["POST"])
def send():
    json.dump(request.form, open(os.path.join(config.get("LOGS_DIR"), "chat-msg-" + str(datetime.now())) + ".json", "w"))
    return redirect(url_for("views.index"))

@app.route("/room/<uuid>")
def room(uuid):
    return render_template("modules/chat/room.html", uuid=uuid)

@app.route("/feedback")
def index():
    if not login_manager.is_logged_in():
        return redirect(url_for("views.login", next=request.url))
    return render_template(
        "modules/chat/feedback.html",
        static_server=f"http://{get_server_ip()}:{config.get('STATIC_SERVER_PORT')}/magnan/",
        username=login_manager.get_username()
    )

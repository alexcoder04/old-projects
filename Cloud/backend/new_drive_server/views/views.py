from flask import Blueprint, render_template, redirect, url_for, send_from_directory, request
import os
from ..auth import login_manager
from ..storage import storage
from ..database import db, shared_files_db
from ..utils import get_server_ip, get_port, magnan_version
from ..config import config

#app = Blueprint("views", __name__, template_folder="templates", static_folder="static", static_url_path="/static/serviceWorkers")
app = Blueprint("views", __name__, template_folder="templates")
static_server = f"http://{get_server_ip()}:{config.get('STATIC_SERVER_PORT')}/magnan/"

@app.route("/")
def index():
    return render_template("index.html", ip=get_server_ip(), port=get_port(), static_server=static_server, magnan_version=magnan_version)

@app.route("/login")
def login():
    next = request.args.get("next")
    if not next: next = url_for("views.mystuff", path="root")
    if login_manager.is_logged_in():
        return redirect(next)
    return render_template("login.html", next=next, static_server=static_server)

@app.route("/signup")
def signup():
    if login_manager.is_logged_in():
        login_manager.logout()
    return render_template("signup.html", static_server=static_server)

@app.route("/mystuff/")
def mystuff_blank():
    return redirect(url_for("views.mystuff", path="root"))

@app.route("/mystuff/<path:path>")
def mystuff(path):
    if login_manager.is_logged_in():
        user = login_manager.get_username()
        if path == "shared":
            return render_template(
                "mystuff.shared.html",
                data={"username": user},
                files=shared_files_db.get_all_files_for(user),
                static_server=static_server
            )
        return render_template(
            "mystuff.html",
            data={
                "username": user,
                "folder": path,
            },
            static_server=static_server
        )
    return redirect(url_for("views.login", next=request.url))

@app.route("/settings")
def settings():
    if login_manager.is_logged_in():
        data = db.get_user(login_manager.get_username())
        return render_template("settings.html", data=data, static_server=static_server)
    return redirect(url_for("views.login", next="/settings"))

@app.route("/articles/<path:article_page>")
def article(article_page):
    return render_template(f"articles/{article_page}", static_server=static_server)

@app.route("/favicon.ico")
def send_favicon():
    return redirect(f"{static_server}img/favicon.ico")

@app.route("/error/<message>")
def error(message):
    return render_template("special/error.html", message=message, static_server=static_server)

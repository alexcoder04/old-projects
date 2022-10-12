from flask import Blueprint, render_template, redirect, url_for, request
import requests
import json
from ..auth import login_manager
from ..config import config
from ..cache import magnan_cache
from ..utils import get_server_ip

app = Blueprint("python", __name__, template_folder="templates", static_folder="static")

def get_languages():
    if not magnan_cache.get_cache("piston_langs"):
        magnan_cache.set_cache("piston_langs", json.loads(requests.get("https://emkc.org/api/v1/piston/versions").text))
    return get_cache("piston_langs")

@app.route("/")
def index():
    if not login_manager.is_logged_in():
        return redirect(url_for("views.login", next=request.path))
    temp = "modules/python.html"
    if request.args.get("new") == "yes":
        temp = "modules/python.new.html"
    return render_template(
        temp,
        static_server=f"http://{get_server_ip()}:{config.get('STATIC_SERVER_PORT')}/magnan/",
        languages=get_languages()
    )

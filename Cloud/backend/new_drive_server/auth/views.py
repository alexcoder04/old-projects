from flask import Blueprint, request, redirect, url_for, make_response, flash
from ..database import db
from ..storage import storage
from . import login_manager
from werkzeug.security import generate_password_hash, check_password_hash

app = Blueprint("auth", __name__)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("username")
    password = request.form.get("password")
    user = db.get_user(name)

    # user does not exist or password is wrong
    if not user["name"] or not check_password_hash(user["password"], password):
        flash("Wrong username or password")
        return redirect(url_for("views.login"))
    
    redir_to = request.form.get("next")
    if not redir_to: redir_to = url_for("views.mystuff", path="root")

    sessid = login_manager.login(name)
    resp = make_response(redirect(redir_to))
    resp.set_cookie('sessid', sessid, max_age=60*60*24)
    return resp

@app.route("/signup", methods=["POST"])
def signup():
    name = request.form.get("username")
    password = request.form.get("password")
    password_hash = generate_password_hash(password, method="sha512")
    email = request.form.get("email")

    if len(name) < 4 or len(password) < 5 or len(email) < 6 or "@" not in email:
        flash("Invalid input: too short username/password or invalid email")
        return redirect(url_for("views.signup"))
    
    db.create_user(name, password_hash, email)
    storage.init_user(name)
    
    sessid = login_manager.login(name)
    resp = make_response(redirect(url_for("views.mystuff", path="root")))
    resp.set_cookie('sessid', sessid, max_age=60*60*24)
    return resp

@app.route("/logout")
def logout():
    login_manager.logout()
    resp = make_response(redirect(url_for("views.index")))
    resp.set_cookie("sessid", "")
    return resp

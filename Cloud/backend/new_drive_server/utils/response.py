from flask import jsonify, redirect
from ..auth import login_manager
from ..database import logins_db, db

def message_success(code: int = 200):
    return jsonify({
        "status": "success"
    }), code

def message_error(msg: str = "something went wrong", code: int = 500, html=False):
    if html: return redirect(f"/error/{msg}")
    return jsonify({
        "status": "error",
        "message": msg
    }), code

def get_path(data: dict):
    try:
        return data["path"]
    except KeyError:
        return None

def verify_user(data: dict):
    for key in ["sessid", "user", "api_key"]:
        try:
            data[key] = data[key]
        except KeyError:
            data[key] = ""
    # check by sessid
    if logins_db.is_valid_session(data["sessid"]) and logins_db.get_user_by_id(data["sessid"]) == data["user"]:
        return data["user"]
    # check by api key
    if db.get_api_key_for(data["user"]) == data["api_key"]:
        return data["user"]
    return False

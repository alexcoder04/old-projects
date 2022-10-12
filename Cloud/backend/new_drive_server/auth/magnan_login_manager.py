from flask import session
from ..database import db, logins_db
from werkzeug.security import check_password_hash, generate_password_hash

class LoginManager:
    def get_id(self):
        try:
            return session["id"]
        except KeyError:
            return None

    def login(self, name):
        sessid = logins_db.create_session(name)
        session["id"] = sessid
        return sessid

    def is_logged_in(self):
        if logins_db.is_valid_session(self.get_id()):
            return True
        return False

    def get_username(self):
        if self.is_logged_in():
            return logins_db.get_user_by_id(self.get_id())
        return None

    def logout(self):
        if self.get_id():
            logins_db.delete_sessions(self.get_id())
        session.clear()

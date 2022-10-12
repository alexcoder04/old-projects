import sqlite3
from .magnan_db import MagnanDB
from datetime import datetime
from werkzeug.security import generate_password_hash
from random import random

FILE = "new_drive_server/database/logins.db"
TABLE = "Logins"

class LoginsDataBase(MagnanDB):
    def __init__(self):
        MagnanDB(self).__init__(FILE)
        self.FILE = FILE
        query = f"CREATE TABLE IF NOT EXISTS {TABLE} (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, username VARCHAR(255) NOT NULL, sessionid VARCHAR(255) NOT NULL, expires REAL NOT NULL)"
        self._run_query(query)
        current_time = datetime.now().timestamp()
        query = f"DELETE FROM {TABLE} WHERE expires < {current_time}"
        self._run_query(query)
    
    def create_session(self, user):
        query = f"INSERT INTO {TABLE} (username, sessionid, expires) VALUES (?, ?, ?)"
        current_time = datetime.now().timestamp()
        sessid = generate_password_hash(user + str(current_time) + str(random()), method="sha512")
        self._run_query(query, data=(user, sessid, current_time + 86400))
        return sessid
    
    def is_valid_session(self, sessid):
        query = f"SELECT expires FROM {TABLE} WHERE sessionid = (?)"
        results = self._run_query(query, (sessid,))
        if len(results) == 0:
            return False
        current_time = datetime.now().timestamp()
        if current_time < results[0][0]:
            return True
    
    def delete_sessions(self, user):
        query = f"DELETE FROM {TABLE} WHERE username = (?)"
        self._run_query(query, (user,))
    
    def get_user_by_id(self, id):
        query = f"SELECT username FROM {TABLE} WHERE sessionid = (?)"
        results = self._run_query(query, (id,))
        if len(results) > 0:
            return results[0][0]
        return None

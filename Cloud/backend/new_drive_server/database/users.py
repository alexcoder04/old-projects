import sqlite3
from .magnan_db import MagnanDB
from werkzeug.utils import secure_filename
from uuid import uuid4

FILE = "new_drive_server/database/users.db"
TABLE = "Users"

class UsersDataBase(MagnanDB):
    def __init__(self):
        MagnanDB(self).__init__(FILE)
        self.FILE = FILE
        query = f"CREATE TABLE IF NOT EXISTS {TABLE} (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR(255) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, email VARCHAR(255), api_key VARCHAR(255))"
        self._run_query(query)

    def create_user(self, name: str, password: str, email: str):
        name = secure_filename(name)
        query = f"INSERT INTO {TABLE} (name, password, email, api_key) VALUES (?, ?, ?, ?)"
        self._run_query(query, (name, password, email, self.create_api_key(),))

    def get_user(self, name: str):
        query = f"SELECT name, password, email, api_key FROM {TABLE} WHERE name=?"
        results = self._run_query(query, (name,))
        if len(results) > 0:
            return { "name": results[0][0], "password": results[0][1], "email": results[0][2], "api_key": results[0][3] }
        return { "name": None, "password": None, "email": None, "api_key": None }
    
    def get_all_users(self):
        query = f"SELECT name FROM {TABLE}"
        results = self._run_query(query)
        return [i[0] for i in results]
    
    def get_api_key_for(self, user):
        query = f"SELECT api_key FROM {TABLE} WHERE name=?"
        results = self._run_query(query, (user,))
        if len(results) == 0:
            return None
        return results[0][0]
    
    def create_api_key(self):
        return str(uuid4())

import sqlite3
from .magnan_db import MagnanDB
from uuid import uuid4

FILE = "new_drive_server/database/shared_files.db"
TABLE = "Files"

class SharedFilesdataBase(MagnanDB):
    def __init__(self):
        MagnanDB(self).__init__(FILE)
        self.FILE = FILE
        query = f"CREATE TABLE IF NOT EXISTS {TABLE} (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, username VARCHAR(255) NOT NULL, path VARCHAR(255) NOT NULL, uuid VARCHAR(255) NOT NULL)"
        self._run_query(query)
    
    def create_link(self, user, path):
        link = str(uuid4())
        query = f"INSERT INTO {TABLE} (username, path, uuid) VALUES (?, ?, ?)"
        self._run_query(query, (user, path, link,))
        return link
    
    def get_data_for_id(self, id):
        query = f"SELECT username, path FROM {TABLE} WHERE uuid = (?)"
        results = self._run_query(query, (id,))
        if len(results) == 0:
            return None
        return {
            "user": results[0][0],
            "path": results[0][1]
        }
    
    def get_all_files_for(self, user):
        query = f"SELECT path, uuid FROM {TABLE} WHERE username = (?)"
        results = self._run_query(query, (user,))
        if len(results) == 0:
            return None
        return [{ "path": i[0], "uuid": i[1] } for i in results]

import sqlite3
from .magnan_db import MagnanDB

FILE = "new_drive_server/database/open.db"

class OpenDB(MagnanDB):
    def __init__(self, client, columns):
        MagnanDB(self).__init__(FILE)
        self.FILE = FILE
        self.client = client
        query_columns = ["id INTEGER PRIMARY KEY NOT NULL UNIQUE"]
        for col in columns:
            query_columns.append(f"{col['name']} {col['type'].upper()} {col['args']}")
        query = f"CREATE TABLE IF NOT EXISTS {self.client} ({','.join(query_columns)})"
        print(query)
        self._run_query(query)
    
    def new_entry(self, entry):
        # entry = [ { "column": "name", "value": "Alex" }, ... ]
        rows = ",".join([e["column"] for e in entry])
        values = ",".join("?" for _ in range(len(entry)))
        query = f"INSERT INTO {self.client} ({rows}) VALUES ({values})"
        print(query)
        self._run_query(query, tuple([e["value"] for e in entry]))
    
    def search(self, data):
        # data = { "a": "b", "c": "d" }
        subquery = " AND ".join([ f"{key} = ?" for key in data ])
        query = f"SELECT * FROM {self.client} WHERE {subquery}"
        return self._run_query(query, tuple([data[i] for i in data]))
    
    def getall(self):
        return self._run_query(f"SELECT * FROM {self.client}")
    
    def delete(self):
        self._run_query(f"DROP TABEL IF EXISTS {self.client}")


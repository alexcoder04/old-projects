import sqlite3

class MagnanDB:
    def __init__(self, file):
        self.FILE = file
    
    def _run_query(self, query, data=None):
        conn = sqlite3.connect(self.FILE)
        cursor = conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        results = cursor.fetchall()
        conn.commit()
        conn.close()
        return results

import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="admin",
            password="01022005an",
            database="videocaller"
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

db = Database()
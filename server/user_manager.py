from server.db import Database
import mysql.connector

class UserManager:
    def __init__(self):
        # Tạo kết nối CSDL
        self.db = Database()

    def validate_user(self, username, password):
        """Kiểm tra đăng nhập"""
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        result = self.db.execute_query(query, (username, password))
        return len(result) > 0

    def register_user(self, username, password, email=None):
        """Đăng ký tài khoản mới"""
        # Kiểm tra trùng username
        check_query = "SELECT * FROM users WHERE username = %s"
        existing = self.db.execute_query(check_query, (username,))
        if len(existing) > 0:
            return False, "Username already exists"

        try:
            insert_query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            self.db.cursor.execute(insert_query, (username, email, password))
            self.db.conn.commit()
            return True, "User registered successfully"
        except mysql.connector.Error as err:
            return False, f"Database error: {err}"

# Singleton để dùng chung trong server
user_manager = UserManager()

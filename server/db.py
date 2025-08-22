# server/db.py
import sqlite3
import hashlib # Thư viện để băm mật khẩu

DATABASE_NAME = '../data/video_call.db' # Lưu file db trong thư mục data

def get_db_connection():
    """Tạo kết nối tới database"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    """Tạo bảng users nếu chưa tồn tại"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Mật khẩu sẽ được lưu dưới dạng hash để bảo mật
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    print("Bảng 'users' đã được tạo hoặc đã tồn tại.")

def hash_password(password):
    """Băm mật khẩu bằng SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password):
    """Thêm một user mới vào database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        print(f"Đã thêm user '{username}' thành công.")
        return True
    except sqlite3.IntegrityError:
        print(f"Lỗi: User '{username}' đã tồnTAIN.")
        return False
    finally:
        conn.close()

def check_user(username, password):
    """Kiểm tra thông tin đăng nhập của user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, hash_password(password))
    )
    
    user = cursor.fetchone()
    conn.close()
    
    return user is not None

# Chạy lần đầu để tạo bảng
if __name__ == '__main__':
    # Tạo thư mục data nếu chưa có
    import os
    if not os.path.exists('../data'):
        os.makedirs('../data')
    
    create_tables()
    # Thêm một vài user mẫu để test
    add_user('user1', 'pass1')
    add_user('user2', 'pass2')
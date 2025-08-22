import sqlite3
import hashlib # Để mã hóa mật khẩu

DB_PATH = 'data/video_call.db'

def hash_password(password):
    """Mã hóa mật khẩu bằng SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def db_connect():
    """Tạo kết nối đến cơ sở dữ liệu."""
    return sqlite3.connect(DB_PATH)

def setup_database():
    """Tạo bảng 'users' nếu nó chưa tồn tại."""
    conn = db_connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database setup complete. 'users' table is ready.")

def add_user(username, email, password):
    """Thêm một người dùng mới vào database."""
    conn = db_connect()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        return True, "Đăng ký thành công"
    except sqlite3.IntegrityError as e:
        # Lỗi xảy ra khi username hoặc email đã tồn tại
        if 'username' in str(e):
            return False, "Tên đăng nhập đã tồn tại."
        if 'email' in str(e):
            return False, "Email đã được sử dụng."
        return False, "Lỗi không xác định."
    finally:
        conn.close()

def check_user(username, password):
    """Kiểm tra thông tin đăng nhập của người dùng."""
    conn = db_connect()
    cursor = conn.cursor()
    password_hash = hash_password(password)
    cursor.execute(
        "SELECT * FROM users WHERE username = ? AND password_hash = ?",
        (username, password_hash)
    )
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Chạy một lần để khởi tạo DB khi bắt đầu
if __name__ == '__main__':
    setup_database()
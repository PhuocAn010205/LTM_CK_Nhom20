import sqlite3
import hashlib
import os

# Tự động tạo thư mục 'data' nếu chưa có để chứa file database
if not os.path.exists('data'):
    os.makedirs('data')

DB_PATH = 'data/video_call.db'

def hash_password(password):
    """Mã hóa mật khẩu bằng SHA-256 cho an toàn."""
    return hashlib.sha256(password.encode()).hexdigest()

def db_connect():
    """Tạo kết nối đến cơ sở dữ liệu."""
    # check_same_thread=False cần thiết khi dùng DB với multi-threading
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def setup_database():
    """
    Hàm này sẽ được gọi khi server khởi động.
    Nó tạo bảng 'users' nếu bảng chưa tồn tại.
    """
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
    print("[DB] Database setup complete. 'users' table is ready.")

def add_user(username, email, password):
    """Thêm một người dùng mới vào database, xử lý lỗi nếu trùng lặp."""
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
        # Bắt lỗi khi username hoặc email đã tồn tại (do constraint UNIQUE)
        if 'username' in str(e):
            return False, "Tên đăng nhập đã tồn tại."
        if 'email' in str(e):
            return False, "Email đã được sử dụng."
        return False, "Lỗi không xác định khi đăng ký."
    finally:
        conn.close()

def check_user(username, password):
    """Kiểm tra thông tin đăng nhập của người dùng với mật khẩu đã mã hóa."""
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
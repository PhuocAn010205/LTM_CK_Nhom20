from server import db

class UserManager:
    def __init__(self):
        """
        Khởi tạo và đảm bảo database đã sẵn sàng bằng cách gọi hàm setup.
        """
        db.setup_database()

    def handle_registration(self, username, email, password):
        """
        Xử lý logic đăng ký, kiểm tra đầu vào trước khi gọi đến db.
        """
        if not all([username, email, password]):
            return False, "Vui lòng nhập đầy đủ thông tin."
        return db.add_user(username, email, password)

    def handle_login(self, username, password):
        """
        Xử lý logic đăng nhập, kiểm tra đầu vào trước khi gọi đến db.
        """
        if not all([username, password]):
            return False, "Vui lòng nhập tên đăng nhập và mật khẩu."
        
        if db.check_user(username, password):
            return True, "Đăng nhập thành công"
        else:
            return False, "Tên đăng nhập hoặc mật khẩu không đúng"
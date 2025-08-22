import sys
from PyQt5.QtWidgets import QApplication
from client.auth_window import AuthWindow
from client.main_window import MainWindow
from client.network_client import NetworkClient

class Application:
    """
    Lớp điều phối chính, kết nối giao diện và logic mạng.
    Đây là file để chạy client.
    """
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        # Khởi tạo các thành phần cốt lõi của client
        self.network_client = NetworkClient()
        self.auth_window = AuthWindow()
        self.main_window = None

        # Kết nối các tín hiệu và khe cắm (signals & slots)
        self.connect_signals()

    def connect_signals(self):
        """
        Đây là phần quan trọng nhất, kết nối các sự kiện với hành động.
        Ví dụ: Khi nút đăng nhập được bấm (tín hiệu từ AuthWindow),
        nó sẽ gọi hàm xử lý đăng nhập (hàm trong NetworkClient).
        """
        # 1. Yêu cầu từ giao diện -> gửi đi bằng network_client
        self.auth_window.login_request.connect(self.network_client.attempt_login)
        self.auth_window.register_request.connect(self.network_client.attempt_register)

        # 2. Kết quả từ network_client -> cập nhật giao diện
        self.network_client.login_success.connect(self.on_login_success)
        self.network_client.auth_fail.connect(self.auth_window.on_auth_fail)
        self.network_client.register_success.connect(self.auth_window.on_register_success)
        self.network_client.connection_error.connect(self.auth_window.on_auth_fail)

    def run(self):
        """Bắt đầu chạy ứng dụng."""
        self.auth_window.show()
        self.network_client.connect_to_server() # Chủ động kết nối đến server ngay khi chạy
        sys.exit(self.app.exec_())

    def on_login_success(self, username):
        """Hàm được gọi khi tín hiệu login_success được phát ra từ NetworkClient."""
        print(f"Đăng nhập thành công với user: {username}")
        # Tạo cửa sổ chính
        self.main_window = MainWindow(username)
        self.main_window.show()
        # Đóng cửa sổ đăng nhập
        self.auth_window.close()

if __name__ == "__main__":
    app_instance = Application()
    app_instance.run()
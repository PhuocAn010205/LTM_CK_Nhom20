import sys
from PyQt5.QtWidgets import QApplication
from client.auth_window import AuthWindow
from client.main_window import MainWindow

class Application:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.auth_window = AuthWindow()
        self.main_window = None

        # Kết nối signal từ cửa sổ đăng nhập đến một hàm xử lý
        self.auth_window.login_successful.connect(self.show_main_window)

    def run(self):
        self.auth_window.show()
        sys.exit(self.app.exec_())

    def show_main_window(self, username):
        """Hàm này được gọi khi đăng nhập thành công."""
        # Tạo cửa sổ chính với thông tin username
        self.main_window = MainWindow(username)
        self.main_window.show()
        # Cửa sổ đăng nhập đã tự đóng lại rồi

if __name__ == "__main__":
    app_instance = Application()
    app_instance.run()
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLineEdit, QPushButton, QLabel, QStackedWidget, QMessageBox)
from PyQt5.QtCore import pyqtSignal
import socket
from common.protocol import Protocol

# Cấu hình server (thay đổi nếu cần)
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

class AuthWindow(QWidget):
    # Signal sẽ được phát ra khi đăng nhập thành công, mang theo thông tin username
    login_successful = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.client_socket = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Đăng nhập / Đăng ký')
        self.setGeometry(300, 300, 400, 250)

        self.stacked_widget = QStackedWidget()
        self.login_page = self._create_login_page()
        self.register_page = self._create_register_page()

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

    def _create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        layout.addWidget(QLabel('<h2>Đăng nhập</h2>'))

        self.login_username_input = QLineEdit()
        self.login_username_input.setPlaceholderText('Tên đăng nhập')
        layout.addWidget(self.login_username_input)

        self.login_password_input = QLineEdit()
        self.login_password_input.setPlaceholderText('Mật khẩu')
        self.login_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.login_password_input)

        login_button = QPushButton('Đăng nhập')
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        go_register_button = QPushButton('Chưa có tài khoản? Đăng ký')
        go_register_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.register_page))
        layout.addWidget(go_register_button)
        
        return page

    def _create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addWidget(QLabel('<h2>Đăng ký</h2>'))
        
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText('Tên đăng nhập')
        layout.addWidget(self.reg_username_input)

        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText('Email')
        layout.addWidget(self.reg_email_input)

        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText('Mật khẩu')
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.reg_password_input)

        register_button = QPushButton('Đăng ký')
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button)

        go_login_button = QPushButton('Đã có tài khoản? Đăng nhập')
        go_login_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.login_page))
        layout.addWidget(go_login_button)
        
        return page
        
    def connect_to_server(self):
        """Kết nối đến server nếu chưa có kết nối."""
        if self.client_socket is None:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((SERVER_HOST, SERVER_PORT))
            except Exception as e:
                QMessageBox.critical(self, 'Lỗi kết nối', f'Không thể kết nối đến server: {e}')
                self.client_socket = None
                return False
        return True

    def handle_login(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()

        if not username or not password:
            QMessageBox.warning(self, 'Thông báo', 'Vui lòng nhập đầy đủ thông tin.')
            return

        if not self.connect_to_server():
            return

        # Tạo và gửi gói tin đăng nhập
        login_packet = Protocol.create_login_packet(username, password)
        self.client_socket.sendall(login_packet)

        # Nhận phản hồi từ server (cần xử lý non-blocking trong ứng dụng thực tế)
        response_raw = self.client_socket.recv(1024)
        response = Protocol.decode_packet(response_raw)

        if response and response.get('type') == 'login_success':
            QMessageBox.information(self, 'Thành công', 'Đăng nhập thành công!')
            self.login_successful.emit(username) # Phát tín hiệu
            self.close() # Đóng cửa sổ đăng nhập
        else:
            error_msg = response.get('data', {}).get('message', 'Tên đăng nhập hoặc mật khẩu không đúng.')
            QMessageBox.critical(self, 'Thất bại', error_msg)
            self.client_socket.close() # Đóng kết nối nếu thất bại
            self.client_socket = None


    def handle_register(self):
        username = self.reg_username_input.text()
        password = self.reg_password_input.text()
        email = self.reg_email_input.text()

        if not username or not password or not email:
            QMessageBox.warning(self, 'Thông báo', 'Vui lòng nhập đầy đủ thông tin.')
            return

        if not self.connect_to_server():
            return
            
        # Tạo và gửi gói tin đăng ký
        register_packet = Protocol.create_register_packet(username, password, email)
        self.client_socket.sendall(register_packet)
        
        # Nhận phản hồi
        response_raw = self.client_socket.recv(1024)
        response = Protocol.decode_packet(response_raw)
        
        if response and response.get('type') == 'register_success':
            QMessageBox.information(self, 'Thành công', 'Đăng ký thành công! Vui lòng đăng nhập.')
            self.stacked_widget.setCurrentWidget(self.login_page) # Chuyển về trang đăng nhập
        else:
            error_msg = response.get('data', {}).get('message', 'Đăng ký thất bại.')
            QMessageBox.critical(self, 'Thất bại', error_msg)
        
        # Đóng kết nối sau khi đăng ký để người dùng đăng nhập lại
        self.client_socket.close()
        self.client_socket = None

# Dùng để chạy thử nghiệm file này một cách độc lập
if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_win = AuthWindow()
    auth_win.show()
    sys.exit(app.exec_())
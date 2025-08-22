from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, 
                             QLabel, QStackedWidget, QMessageBox, QFormLayout)
from PyQt5.QtCore import pyqtSignal, Qt

class AuthWindow(QWidget):
    """
    Cửa sổ giao diện đăng nhập/đăng ký.
    Nó không chứa logic mạng, chỉ phát tín hiệu khi người dùng tương tác.
    """
    
    # Tín hiệu sẽ được gửi đến lớp Application để xử lý
    login_request = pyqtSignal(str, str)
    register_request = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Video Call App')
        self.setFixedSize(400, 300)

        self.stacked_widget = QStackedWidget()
        self.login_page = self._create_login_page()
        self.register_page = self._create_register_page()

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)

    def _create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel('<h2>Đăng nhập</h2>')
        title.setAlignment(Qt.AlignCenter)
        
        form_layout = QFormLayout()
        self.login_username_input = QLineEdit()
        self.login_password_input = QLineEdit()
        self.login_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow('Tên đăng nhập:', self.login_username_input)
        form_layout.addRow('Mật khẩu:', self.login_password_input)

        login_button = QPushButton('Đăng nhập')
        login_button.clicked.connect(self.handle_login)
        
        go_register_button = QPushButton('Chưa có tài khoản? Đăng ký')
        go_register_button.setStyleSheet("border: none; color: blue;")
        go_register_button.setCursor(Qt.PointingHandCursor)
        go_register_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.register_page))

        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(login_button)
        layout.addWidget(go_register_button)
        return page

    def _create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel('<h2>Đăng ký tài khoản</h2>')
        title.setAlignment(Qt.AlignCenter)
        
        form_layout = QFormLayout()
        self.reg_username_input = QLineEdit()
        self.reg_email_input = QLineEdit()
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow('Tên đăng nhập:', self.reg_username_input)
        form_layout.addRow('Email:', self.reg_email_input)
        form_layout.addRow('Mật khẩu:', self.reg_password_input)

        register_button = QPushButton('Đăng ký')
        register_button.clicked.connect(self.handle_register)
        
        go_login_button = QPushButton('Đã có tài khoản? Đăng nhập')
        go_login_button.setStyleSheet("border: none; color: blue;")
        go_login_button.setCursor(Qt.PointingHandCursor)
        go_login_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.login_page))
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(register_button)
        layout.addWidget(go_login_button)
        return page
        
    def handle_login(self):
        """Phát tín hiệu yêu cầu đăng nhập với dữ liệu từ các ô input."""
        self.login_request.emit(
            self.login_username_input.text(), 
            self.login_password_input.text()
        )

    def handle_register(self):
        """Phát tín hiệu yêu cầu đăng ký."""
        self.register_request.emit(
            self.reg_username_input.text(), 
            self.reg_email_input.text(), 
            self.reg_password_input.text()
        )

    # Các hàm (slots) để hiển thị kết quả, sẽ được gọi bởi lớp Application
    def on_register_success(self, message):
        QMessageBox.information(self, 'Thành công', f'{message}\nBây giờ bạn có thể đăng nhập.')
        self.stacked_widget.setCurrentWidget(self.login_page)

    def on_auth_fail(self, message):
        QMessageBox.critical(self, 'Thất bại', message)
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLineEdit, QPushButton, 
                             QLabel, QStackedWidget, QMessageBox, QFormLayout,
                             QHBoxLayout, QGraphicsDropShadowEffect)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor, QFont

class AuthWindow(QWidget):
    """
    Cửa sổ giao diện đăng nhập/đăng ký với phong cách nữ tính, hiện đại.
    """
    
    login_request = pyqtSignal(str, str)
    register_request = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Video Call App')
        self.setFixedSize(400, 450)
        self.setStyleSheet("background-color: #FFF0F5;") # Màu nền hồng phấn (LavenderBlush)

        self.stacked_widget = QStackedWidget()
        self.login_page = self._create_login_page()
        self.register_page = self._create_register_page()

        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)

    def _apply_styles(self, title_label, form_layout, primary_button, secondary_button):
        """Hàm helper để áp dụng style chung."""
        
        # Style cho tiêu đề
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #8A2BE2;") # Màu tím (BlueViolet)

        # Style cho các ô input
        input_style = """
            QLineEdit {
                border: 1px solid #D8BFD8;
                border-radius: 15px;
                padding: 10px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #8A2BE2;
            }
        """
        for i in range(form_layout.rowCount()):
            widget = form_layout.itemAt(i, QFormLayout.FieldRole).widget()
            if isinstance(widget, QLineEdit):
                widget.setStyleSheet(input_style)

        # Style cho nút chính
        primary_button.setCursor(Qt.PointingHandCursor)
        primary_button.setStyleSheet("""
            QPushButton {
                background-color: #8A2BE2;
                color: white;
                border-radius: 15px;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #9932CC;
            }
        """)

        # Style cho nút phụ (link)
        secondary_button.setCursor(Qt.PointingHandCursor)
        secondary_button.setStyleSheet("QPushButton { border: none; color: #8A2BE2; font-size: 12px; }")

    def _create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        
        title = QLabel('Đăng Nhập')
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        self.login_username_input = QLineEdit()
        self.login_password_input = QLineEdit()
        self.login_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(self.login_username_input)
        form_layout.addRow(self.login_password_input)

        login_button = QPushButton('Đăng Nhập')
        login_button.clicked.connect(self.handle_login)
        
        go_register_button = QPushButton('Chưa có tài khoản? Đăng ký ngay')
        go_register_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.register_page))

        self._apply_styles(title, form_layout, login_button, go_register_button)

        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(login_button)
        layout.addWidget(go_register_button)
        return page

    def _create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel('Tạo Tài Khoản')
        
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        self.reg_username_input = QLineEdit()
        self.reg_username_input.setPlaceholderText('Tên đăng nhập')
        self.reg_email_input = QLineEdit()
        self.reg_email_input.setPlaceholderText('Email')
        self.reg_password_input = QLineEdit()
        self.reg_password_input.setPlaceholderText('Mật khẩu')
        self.reg_password_input.setEchoMode(QLineEdit.Password)
        form_layout.addRow(self.reg_username_input)
        form_layout.addRow(self.reg_email_input)
        form_layout.addRow(self.reg_password_input)

        register_button = QPushButton('Đăng Ký')
        register_button.clicked.connect(self.handle_register)
        
        go_login_button = QPushButton('Đã có tài khoản? Đăng nhập')
        go_login_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.login_page))
        
        self._apply_styles(title, form_layout, register_button, go_login_button)
        
        layout.addWidget(title)
        layout.addLayout(form_layout)
        layout.addWidget(register_button)
        layout.addWidget(go_login_button)
        return page
        
    def handle_login(self):
        self.login_request.emit(
            self.login_username_input.text(), 
            self.login_password_input.text()
        )

    def handle_register(self):
        self.register_request.emit(
            self.reg_username_input.text(), 
            self.reg_email_input.text(), 
            self.reg_password_input.text()
        )

    def on_register_success(self, message):
        QMessageBox.information(self, 'Thành công', f'{message}\nBây giờ bạn có thể đăng nhập.')
        self.stacked_widget.setCurrentWidget(self.login_page)

    def on_auth_fail(self, message):
        QMessageBox.critical(self, 'Thất bại', message)
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    """
    Cửa sổ chính của ứng dụng với giao diện nữ tính, sạch sẽ.
    """
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Video Call - Chào mừng, {self.username}')
        self.setGeometry(200, 200, 900, 600)
        self.setStyleSheet("background-color: #F8F8FF;") # Màu nền trắng ma (GhostWhite)

        # Widget trung tâm để chứa toàn bộ layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel danh sách bạn bè/phòng bên trái
        left_panel = QWidget()
        left_panel.setFixedWidth(300)
        left_panel.setStyleSheet("background-color: #FFF0F5;") # Màu hồng phấn
        left_panel_layout = QVBoxLayout(left_panel)
        left_panel_layout.setContentsMargins(15, 15, 15, 15)

        # -- Header Chào mừng
        welcome_label = QLabel(f'Xin chào,\n<b style="font-size: 20px;">{self.username}</b>')
        welcome_label.setStyleSheet("color: #8A2BE2;")
        welcome_label.setFont(QFont("Arial", 14))
        left_panel_layout.addWidget(welcome_label)
        left_panel_layout.addSpacing(20)

        # -- Danh sách người dùng/phòng
        list_header = QLabel("Danh sách bạn bè")
        list_header.setFont(QFont("Arial", 12, QFont.Bold))
        list_header.setStyleSheet("color: #4B0082;") # Màu chàm đậm (Indigo)
        left_panel_layout.addWidget(list_header)

        self.user_list = QListWidget()
        self.user_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #D8BFD8;
                border-radius: 10px;
                background-color: white;
            }
            QListWidget::item {
                padding: 15px;
            }
            QListWidget::item:hover {
                background-color: #E6E6FA; /* Lavender */
            }
            QListWidget::item:selected {
                background-color: #DDA0DD; /* Plum */
                color: white;
            }
        """)
        # Thêm vài người dùng mẫu
        for name in ["Ngọc Anh", "Thảo My", "Bảo Châu", "Phương Linh"]:
            item = QListWidgetItem(name)
            item.setFont(QFont("Arial", 11))
            self.user_list.addItem(item)
        left_panel_layout.addWidget(self.user_list)
        
        # Panel hiển thị video và điều khiển bên phải
        right_panel = QWidget()
        right_panel_layout = QVBoxLayout(right_panel)
        right_panel_layout.setContentsMargins(30, 30, 30, 30)

        # -- Khu vực video
        self.video_display_label = QLabel('Đang chờ cuộc gọi...')
        self.video_display_label.setStyleSheet("background-color: black; color: white; border-radius: 15px;")
        self.video_display_label.setAlignment(Qt.AlignCenter)
        self.video_display_label.setFont(QFont("Arial", 16))
        self.video_display_label.setMinimumSize(400, 300)
        right_panel_layout.addWidget(self.video_display_label, 1) # Chiếm phần lớn không gian

        # -- Khu vực nút điều khiển
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setSpacing(20)

        # Nút Bật/Tắt Mic và Camera (sẽ cần icon thật sau)
        mic_button = QPushButton("Tắt Mic")
        cam_button = QPushButton("Tắt Cam")
        end_call_button = QPushButton("Kết Thúc")

        button_style = """
            QPushButton {
                border-radius: 25px;
                padding: 15px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
        """
        mic_button.setStyleSheet(button_style + "background-color: #90EE90; color: black;") # Xanh lá nhạt
        cam_button.setStyleSheet(button_style + "background-color: #ADD8E6; color: black;") # Xanh dương nhạt
        end_call_button.setStyleSheet(button_style + "background-color: #FFB6C1; color: black;") # Hồng nhạt
        
        button_layout.addWidget(mic_button)
        button_layout.addWidget(cam_button)
        button_layout.addWidget(end_call_button)
        right_panel_layout.addLayout(button_layout)

        # Gắn các panel vào layout chính
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
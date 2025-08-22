from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    """
    Cửa sổ chính của ứng dụng, hiển thị sau khi người dùng đăng nhập thành công.
    """
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Video Call - Chào mừng, {self.username}')
        self.setGeometry(200, 200, 800, 600)

        # Widget trung tâm để chứa toàn bộ layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Panel điều khiển bên trái
        controls_panel = QWidget()
        controls_layout = QVBoxLayout(controls_panel)
        controls_panel.setFixedWidth(250)

        controls_layout.addWidget(QLabel(f'<h3>Xin chào, {self.username}</h3>'))
        controls_layout.addWidget(QLabel('<h4>Chọn phòng</h4>'))
        self.room_combo_box = QComboBox()
        self.room_combo_box.addItems(['Phòng chung', 'Phòng học tập', 'Phòng giải trí'])
        controls_layout.addWidget(self.room_combo_box)
        
        join_button = QPushButton('Vào phòng')
        controls_layout.addWidget(join_button)
        
        leave_button = QPushButton('Rời phòng')
        controls_layout.addWidget(leave_button)
        
        controls_layout.addStretch() # Đẩy các widget lên trên

        end_call_button = QPushButton('Kết thúc & Đăng xuất')
        end_call_button.setStyleSheet("background-color: #d9534f; color: white;")
        end_call_button.clicked.connect(self.close) # Đóng cửa sổ khi bấm
        controls_layout.addWidget(end_call_button)

        # Panel hiển thị video bên phải
        video_panel = QWidget()
        video_layout = QVBoxLayout(video_panel)
        
        video_display_label = QLabel('Khu vực hiển thị Video Stream')
        video_display_label.setStyleSheet("background-color: black; color: white; border: 1px solid gray;")
        video_display_label.setAlignment(Qt.AlignCenter)
        video_display_label.setMinimumSize(400, 300)
        video_layout.addWidget(video_display_label)

        # Gắn các panel vào layout chính
        main_layout.addWidget(controls_panel)
        main_layout.addWidget(video_panel)
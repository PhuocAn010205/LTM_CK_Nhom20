import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, QTextEdit)

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f'Video Call - Chào, {self.username}')
        self.setGeometry(200, 200, 800, 600)

        # Widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Panel điều khiển bên trái
        controls_panel = QWidget()
        controls_layout = QVBoxLayout(controls_panel)
        controls_panel.setFixedWidth(250)

        # -- Phần chọn phòng
        controls_layout.addWidget(QLabel('<h3>Chọn phòng</h3>'))
        self.room_combo_box = QComboBox()
        self.room_combo_box.addItems(['Phòng 1', 'Phòng 2', 'Phòng 3']) # Dữ liệu mẫu
        controls_layout.addWidget(self.room_combo_box)
        
        join_button = QPushButton('Vào phòng')
        join_button.clicked.connect(self.handle_join_room)
        controls_layout.addWidget(join_button)
        
        leave_button = QPushButton('Rời phòng')
        leave_button.clicked.connect(self.handle_leave_room)
        controls_layout.addWidget(leave_button)
        
        controls_layout.addStretch() # Đẩy các widget lên trên

        # -- Phần điều khiển cuộc gọi
        end_call_button = QPushButton('Kết thúc cuộc gọi')
        end_call_button.setStyleSheet("background-color: red; color: white;")
        end_call_button.clicked.connect(self.handle_end_call)
        controls_layout.addWidget(end_call_button)

        # Panel hiển thị video bên phải
        video_panel = QWidget()
        video_layout = QVBoxLayout(video_panel)
        
        self.video_display_label = QLabel('Khu vực hiển thị Video')
        self.video_display_label.setStyleSheet("background-color: black; color: white;")
        self.video_display_label.setMinimumSize(400, 300)
        video_layout.addWidget(self.video_display_label)

        # Thêm các panel vào layout chính
        main_layout.addWidget(controls_panel)
        main_layout.addWidget(video_panel)

    def handle_join_room(self):
        room_name = self.room_combo_box.currentText()
        print(f"[{self.username}] đang vào phòng: {room_name}")
        # TODO: Gửi gói tin `join_room` đến server

    def handle_leave_room(self):
        print(f"[{self.username}] đã rời phòng.")
        # TODO: Gửi gói tin `leave_room` đến server

    def handle_end_call(self):
        print(f"[{self.username}] đã kết thúc cuộc gọi.")
        # TODO: Xử lý kết thúc cuộc gọi, có thể đóng ứng dụng hoặc quay lại màn hình chọn phòng
        self.close()

# Dùng để chạy thử nghiệm file này một cách độc lập
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow("TestUser")
    main_win.show()
    sys.exit(app.exec_())
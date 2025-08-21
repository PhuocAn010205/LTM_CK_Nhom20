import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui_ui import Ui_MainWindow

class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Gắn sự kiện cho các nút
        self.loginButton.clicked.connect(self.handle_login)
        self.goRegisterButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.RegisterPage))
        self.backLoginButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.LoginPage))
        self.registerButton.clicked.connect(self.handle_register)
        self.joinRoomButton.clicked.connect(self.handle_join_room)
        self.leaveRoomButton.clicked.connect(self.handle_leave_room)
        self.endCallButton.clicked.connect(self.handle_end_call)

    def handle_login(self):
        username = self.usernameLineEdit.text()
        password = self.passwordLineEdit.text()
        print(f"Đăng nhập với {username}, {password}")
        # TODO: gọi API / socket đến server để xác thực
        self.stackedWidget.setCurrentWidget(self.RoomPage)

    def handle_register(self):
        user = self.regUsernameLineEdit.text()
        pw = self.regPasswordLineEdit.text()
        email = self.regEmailLineEdit.text()
        print(f"Đăng ký với {user}, {pw}, {email}")
        # TODO: gửi request đăng ký
        self.stackedWidget.setCurrentWidget(self.LoginPage)

    def handle_join_room(self):
        room = self.roomComboBox.currentText()
        print(f"Vào {room}")
        # TODO: kết nối đến server -> vào phòng
        self.stackedWidget.setCurrentWidget(self.VideoPage)

    def handle_leave_room(self):
        print("Rời phòng")
        self.stackedWidget.setCurrentWidget(self.RoomPage)

    def handle_end_call(self):
        print("Kết thúc call")
        self.stackedWidget.setCurrentWidget(self.RoomPage)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyApp()
    win.show()
    sys.exit(app.exec_())

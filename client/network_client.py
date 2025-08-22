from PyQt5.QtNetwork import QTcpSocket, QAbstractSocket
from PyQt5.QtCore import QObject, pyqtSignal, QByteArray
from common.protocol import Protocol

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432

class NetworkClient(QObject):
    """
    Quản lý toàn bộ giao tiếp mạng với server một cách bất đồng bộ.
    File này không có giao diện, chỉ xử lý logic mạng và phát tín hiệu.
    """
    
    # Tín hiệu thông báo kết quả về cho lớp Application điều phối
    login_success = pyqtSignal(str)
    auth_fail = pyqtSignal(str) # Dùng chung cho cả login và register fail
    register_success = pyqtSignal(str)
    connection_error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.socket = QTcpSocket(self)
        self.username = None
        self.buffer = QByteArray()
        self.expected_len = 0 # Độ dài gói tin đang chờ nhận

        # Kết nối tín hiệu sẵn có của QTcpSocket với hàm xử lý của chúng ta
        self.socket.readyRead.connect(self.on_ready_read)
        self.socket.errorOccurred.connect(
            lambda: self.connection_error.emit(self.socket.errorString())
        )

    def connect_to_server(self):
        if self.socket.state() == QAbstractSocket.UnconnectedState:
            print(f"[*] Client đang kết nối đến {SERVER_HOST}:{SERVER_PORT}...")
            self.socket.connectToHost(SERVER_HOST, SERVER_PORT)

    def send_request(self, packet_dict):
        """Gửi một yêu cầu đã được đóng gói đến server."""
        if self.socket.state() == QAbstractSocket.ConnectedState:
            framed_packet = Protocol.encode_and_frame_packet(packet_dict)
            self.socket.write(framed_packet)
            self.socket.flush()
            print(f"[*] Client gửi gói tin '{packet_dict.get('type')}'")
        else:
            self.connection_error.emit("Không có kết nối đến server.")
            self.connect_to_server() # Cố gắng kết nối lại

    def attempt_login(self, username, password):
        self.username = username
        packet = Protocol.create_packet("login", {"username": username, "password": password})
        self.send_request(packet)

    def attempt_register(self, username, email, password):
        packet = Protocol.create_packet("register", {"username": username, "password": password, "email": email})
        self.send_request(packet)

    def on_ready_read(self):
        """
        Hàm được tự động gọi bởi Qt event loop mỗi khi có dữ liệu mới từ server.
        Xử lý buffer để đọc các gói tin một cách chính xác.
        """
        self.buffer.append(self.socket.readAll())

        while True:
            # Nếu chưa biết độ dài, cố gắng đọc header (4 bytes)
            if self.expected_len == 0 and self.buffer.size() >= Protocol.HEADER_LENGTH:
                header = self.buffer.left(Protocol.HEADER_LENGTH)
                self.buffer.remove(0, Protocol.HEADER_LENGTH)
                self.expected_len = int.from_bytes(header, 'big')
            
            # Nếu đã biết độ dài và buffer đã có đủ dữ liệu, xử lý gói tin
            if self.expected_len > 0 and self.buffer.size() >= self.expected_len:
                json_data = self.buffer.left(self.expected_len)
                self.buffer.remove(0, self.expected_len)
                self.expected_len = 0 # Reset lại để chờ gói tin tiếp theo
                
                packet = Protocol.decode_json(json_data)
                if packet:
                    self.process_packet(packet)
            else:
                # Dữ liệu chưa đủ, thoát vòng lặp và đợi lần readyRead tiếp theo
                break

    def process_packet(self, packet):
        """Phân loại phản hồi từ server và phát tín hiệu tương ứng."""
        packet_type = packet.get('type')
        message = packet.get('data', {}).get('message', 'Lỗi không xác định.')
        
        print(f"[*] Client nhận phản hồi: {packet_type}")

        if packet_type == 'login_success':
            self.login_success.emit(self.username)
        elif packet_type == 'login_fail':
            self.auth_fail.emit(message)
        elif packet_type == 'register_success':
            self.register_success.emit(message)
        elif packet_type == 'register_fail':
            self.auth_fail.emit(message)
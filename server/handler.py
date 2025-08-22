import threading
import struct
from common.protocol import Protocol

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address, user_manager, room_manager):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.user_manager = user_manager
        self.room_manager = room_manager # Thêm RoomManager
        self.running = True
        
        # Thêm các thuộc tính để lưu trạng thái của người dùng
        self.username = None
        self.current_room = None
        
        print(f"[+] Kết nối mới từ {self.client_address}")

    def run(self):
        try:
            while self.running:
                # Bước 1: Đọc 4 bytes header để biết độ dài của gói tin sắp tới
                header = self.client_socket.recv(Protocol.HEADER_LENGTH)
                if not header:
                    break
                
                msg_len = struct.unpack('!I', header)[0]
                
                # Bước 2: Đọc chính xác số bytes của gói tin dựa vào độ dài đã biết
                full_msg = b''
                while len(full_msg) < msg_len:
                    chunk = self.client_socket.recv(msg_len - len(full_msg))
                    if not chunk:
                        raise ConnectionError("Client ngắt kết nối khi đang gửi dữ liệu.")
                    full_msg += chunk
                
                # Bước 3: Giải mã và xử lý gói tin
                packet = Protocol.decode_json(full_msg)
                if packet:
                    self.process_packet(packet)

        except (ConnectionResetError, ConnectionError):
            print(f"[!] Client {self.client_address} đã ngắt kết nối.")
        except Exception as e:
            print(f"[!] Lỗi nghiêm trọng ở {self.client_address}: {e}")
        finally:
            # Dọn dẹp tài nguyên khi client ngắt kết nối
            self.room_manager.leave_room(self)
            print(f"[-] Kết nối từ {self.client_address} (user: {self.username}) đã đóng.")
            self.client_socket.close()

    def process_packet(self, packet):
        """Phân loại và xử lý gói tin dựa vào 'type'."""
        packet_type = packet.get('type')
        data = packet.get('data', {})
        
        # --- Xử lý xác thực ---
        if packet_type == 'register':
            success, message = self.user_manager.handle_registration(
                data.get('username'), data.get('email'), data.get('password')
            )
            response_type = 'register_success' if success else 'register_fail'
            self.send_response(response_type, message)

        elif packet_type == 'login':
            success, message = self.user_manager.handle_login(
                data.get('username'), data.get('password')
            )
            response_type = 'login_success' if success else 'login_fail'
            if success:
                self.username = data.get('username') # Lưu lại username khi đăng nhập thành công
            self.send_response(response_type, message)
        
        # --- Xử lý phòng ---
        elif packet_type == 'get_rooms':
            rooms = self.room_manager.get_room_list()
            response_packet = Protocol.create_packet('room_list', {'rooms': rooms})
            self.send_packet(response_packet)

        elif packet_type == 'join_room':
            room_name = data.get('room_name')
            if room_name:
                # Rời phòng cũ (nếu có) trước khi vào phòng mới
                self.room_manager.leave_room(self)
                self.current_room = room_name
                self.room_manager.join_room(self, room_name)
        
        elif packet_type == 'leave_room':
            self.room_manager.leave_room(self)
            self.current_room = None

        # --- Xử lý media ---
        elif packet_type == 'media':
            # Thêm thông tin người gửi vào gói tin media trước khi broadcast
            packet['data']['sender'] = self.username
            self.room_manager.broadcast_media(self, packet)

    def send_packet(self, packet_dict):
        """Đóng gói và gửi một gói tin bất kỳ đến client này."""
        framed_packet = Protocol.encode_and_frame_packet(packet_dict)
        self.client_socket.sendall(framed_packet)

    def send_response(self, response_type, message):
        """Tạo và gửi một gói tin phản hồi đơn giản."""
        response_dict = Protocol.create_packet(response_type, {"message": message})
        self.send_packet(response_dict)
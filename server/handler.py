import threading
import struct
from common.protocol import Protocol

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address, user_manager, room_manager):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.user_manager = user_manager
        self.room_manager = room_manager
        self.running = True
        
        self.username = None
        self.current_room = None
        
        print(f"[+] Kết nối mới từ {self.client_address}")

    def run(self):
        try:
            while self.running:
                header = self.client_socket.recv(Protocol.HEADER_LENGTH)
                if not header:
                    break
                
                msg_len = struct.unpack('!I', header)[0]
                
                full_msg = b''
                while len(full_msg) < msg_len:
                    chunk = self.client_socket.recv(msg_len - len(full_msg))
                    if not chunk:
                        raise ConnectionError("Client ngắt kết nối khi đang gửi dữ liệu.")
                    full_msg += chunk
                
                packet = Protocol.decode_json(full_msg)
                if packet:
                    self.process_packet(packet)

        except (ConnectionResetError, ConnectionError):
            print(f"[!] Client {self.client_address} đã ngắt kết nối.")
        except Exception as e:
            print(f"[!] Lỗi nghiêm trọng ở {self.client_address}: {e}")
        finally:
            self.room_manager.leave_room(self)
            print(f"[-] Kết nối từ {self.client_address} (user: {self.username}) đã đóng.")
            self.client_socket.close()

    def process_packet(self, packet):
        packet_type = packet.get('type')
        data = packet.get('data', {})
        
        # --- Xử lý xác thực (luôn cho phép) ---
        if packet_type == 'register':
            success, message = self.user_manager.handle_registration(
                data.get('username'), data.get('email'), data.get('password')
            )
            response_type = 'register_success' if success else 'register_fail'
            self.send_response(response_type, message)
            return

        elif packet_type == 'login':
            success, message = self.user_manager.handle_login(
                data.get('username'), data.get('password')
            )
            response_type = 'login_success' if success else 'login_fail'
            if success:
                self.username = data.get('username')
            self.send_response(response_type, message)
            return

        # --- KIỂM TRA ĐĂNG NHẬP ---
        # Chỉ xử lý các gói tin bên dưới nếu người dùng đã đăng nhập thành công
        if not self.username:
            print(f"[!] Client {self.client_address} chưa đăng nhập đã cố gắng gửi gói tin '{packet_type}'.")
            return
        
        # --- Xử lý phòng (chỉ dành cho người đã đăng nhập) ---
        if packet_type == 'get_rooms':
            rooms = self.room_manager.get_room_list()
            response_packet = Protocol.create_packet('room_list', {'rooms': rooms})
            self.send_packet(response_packet)

        elif packet_type == 'join_room':
            room_name = data.get('room_name')
            if room_name:
                self.room_manager.leave_room(self)
                self.current_room = room_name
                self.room_manager.join_room(self, room_name)
        
        elif packet_type == 'leave_room':
            self.room_manager.leave_room(self)
            self.current_room = None

        # --- Xử lý media (chỉ dành cho người đã đăng nhập) ---
        elif packet_type == 'media':
            packet['data']['sender'] = self.username
            self.room_manager.broadcast_media(self, packet)

    def send_packet(self, packet_dict):
        framed_packet = Protocol.encode_and_frame_packet(packet_dict)
        self.client_socket.sendall(framed_packet)

    def send_response(self, response_type, message):
        response_dict = Protocol.create_packet(response_type, {"message": message})
        self.send_packet(response_dict)
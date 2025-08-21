import socket
import json
import threading
from common import protocol


class ClientHandler:
    def __init__(self, client_socket, addr, clients, room_manager, user_manager, db):
        self.client_socket = client_socket
        self.addr = addr
        self.clients = clients
        self.room_manager = room_manager
        self.user_manager = user_manager
        self.db = db
        self.stop = False

    def handle_client(self):
        while not self.stop:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                packet = json.loads(data.decode('utf-8'))
                self.process_packet(packet)
            except Exception as e:
                print(f"[ERROR] {e}")
                break

    def process_packet(self, packet):
        packet_type = packet.get("type")
        if packet_type == "login":
            self.handle_login(packet)
        elif packet_type == "register":  # 👈 thêm xử lý đăng ký
            self.handle_register(packet)
        elif packet_type == "join":
            self.handle_join(packet)
        elif packet_type == "leave":
            self.handle_leave(packet)
        elif packet_type == "media":
            self.handle_media(packet)

    def handle_login(self, packet):
        username = packet.get("username")
        password = packet.get("password")
        if self.user_manager.validate_user(username, password):
            response = {"type": "login", "status": "success"}
        else:
            response = {"type": "login", "status": "failure"}
        self.client_socket.send(json.dumps(response).encode('utf-8'))

    def handle_register(self, packet):
        """Xử lý đăng ký user mới"""
        username = packet.get("username")
        password = packet.get("password")
        email = packet.get("email")

        success, msg = self.user_manager.register_user(username, password, email)
        if success:
            response = {"type": "register", "status": "success", "message": msg}
        else:
            response = {"type": "register", "status": "failure", "message": msg}

        self.client_socket.send(json.dumps(response).encode("utf-8"))

    def handle_join(self, packet):
        room = packet.get("room")
        if self.room_manager.add_user_to_room(self.addr, room):
            response = {"type": "join", "status": "success"}
            self.broadcast({"type": "user_joined", "room": room, "addr": str(self.addr)})
        else:
            response = {"type": "join", "status": "failure"}
        self.client_socket.send(json.dumps(response).encode('utf-8'))

    def handle_leave(self, packet):
        room = packet.get("room")
        if self.room_manager.remove_user_from_room(self.addr, room):
            response = {"type": "leave", "status": "success"}
            self.broadcast({"type": "user_left", "room": room, "addr": str(self.addr)})
            if not self.room_manager.is_room_active(room):
                self.room_manager.close_room(room)
        else:
            response = {"type": "leave", "status": "failure"}
        self.client_socket.send(json.dumps(response).encode('utf-8'))

    def handle_media(self, packet):
        room = packet.get("room")
        if self.room_manager.is_user_in_room(self.addr, room):
            self.broadcast(packet, exclude=self.addr)

    def broadcast(self, packet, exclude=None):
        for client in self.clients:
            if client.addr != exclude:
                client.client_socket.send(json.dumps(packet).encode('utf-8'))

    def start(self):
        thread = threading.Thread(target=self.handle_client)
        thread.start()

    def stop(self):
        self.stop = True
        self.client_socket.close()

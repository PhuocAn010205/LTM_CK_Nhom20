import threading

class RoomManager:
    def __init__(self):
        # Dùng dictionary để lưu các phòng: {'tên phòng': {handler1, handler2, ...}}
        # Dùng set để thêm/xóa người dùng hiệu quả hơn
        self.rooms = {}
        self.lock = threading.Lock() # Để đảm bảo an toàn khi nhiều thread cùng truy cập

    def get_room_list(self):
        """Lấy danh sách các phòng hiện có."""
        with self.lock:
            # Trả về danh sách tên phòng và số lượng người trong mỗi phòng
            return {name: len(clients) for name, clients in self.rooms.items()}

    def join_room(self, client_handler, room_name):
        """Thêm một client vào phòng."""
        with self.lock:
            # Nếu phòng chưa tồn tại, tạo phòng mới
            if room_name not in self.rooms:
                self.rooms[room_name] = set()
            
            # Thêm client_handler vào phòng
            self.rooms[room_name].add(client_handler)
            print(f"[*] {client_handler.username} đã vào phòng '{room_name}'.")

    def leave_room(self, client_handler):
        """Xóa một client khỏi phòng hiện tại của họ."""
        if not client_handler.current_room:
            return

        room_name = client_handler.current_room
        with self.lock:
            if room_name in self.rooms:
                self.rooms[room_name].discard(client_handler)
                print(f"[*] {client_handler.username} đã rời phòng '{room_name}'.")
                # Nếu phòng trống, xóa phòng đó đi
                if not self.rooms[room_name]:
                    del self.rooms[room_name]
                    print(f"[*] Phòng '{room_name}' đã trống và được xóa.")
    
    def broadcast_media(self, sender_handler, media_packet):
        """Gửi gói tin media đến tất cả client khác trong cùng phòng."""
        room_name = sender_handler.current_room
        if not room_name:
            return

        with self.lock:
            if room_name in self.rooms:
                # Lặp qua tất cả client trong phòng
                for client in self.rooms[room_name]:
                    # Chỉ gửi cho những người khác, không gửi lại cho người gửi
                    if client is not sender_handler:
                        client.send_packet(media_packet)
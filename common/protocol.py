import json
import struct

class Protocol:
    """
    Định nghĩa cấu trúc và cách đóng gói tin.
    Mỗi gói tin gửi đi sẽ có cấu trúc: [Độ dài (4 bytes)][Nội dung JSON (bytes)]
    """
    HEADER_LENGTH = 4

    @staticmethod
    def create_packet(packet_type, data):
        """Tạo nội dung gói tin dưới dạng dictionary."""
        return {"type": packet_type, "data": data}

    @staticmethod
    def encode_and_frame_packet(packet_dict):
        """
        Mã hóa dictionary thành JSON, sau đó đóng gói với header độ dài.
        Trả về một chuỗi bytes sẵn sàng để gửi qua socket.
        """
        json_data = json.dumps(packet_dict).encode('utf-8')
        header = struct.pack('!I', len(json_data)) # '!I' là 4-byte unsigned integer
        return header + json_data

    @staticmethod
    def decode_json(json_bytes):
        """Giải mã chuỗi bytes JSON thành dictionary."""
        try:
            return json.loads(json_bytes.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None
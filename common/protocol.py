import json

class Protocol:
         @staticmethod
         def encode_packet(packet_type, data):
             """Encode a packet with type and data into JSON format."""
             packet = {
                 "type": packet_type,
                 "data": data
             }
             return json.dumps(packet).encode('utf-8')

         @staticmethod
         def decode_packet(raw_data):
             """Decode a raw data packet into a dictionary."""
             try:
                 return json.loads(raw_data.decode('utf-8'))
             except json.JSONDecodeError:
                 return None

         @staticmethod
         def create_login_packet(username, password):
             """Create a login packet."""
             return Protocol.encode_packet("login", {"username": username, "password": password})

         @staticmethod
         def create_join_packet(room):
             """Create a join room packet."""
             return Protocol.encode_packet("join", {"room": room})

         @staticmethod
         def create_leave_packet(room):
             """Create a leave room packet."""
             return Protocol.encode_packet("leave", {"room": room})

         @staticmethod
         def create_media_packet(room, media_data):
             """Create a media packet."""
             return Protocol.encode_packet("media", {"room": room, "media": media_data})           
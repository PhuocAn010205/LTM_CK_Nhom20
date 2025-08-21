import socket
import threading

# import handler & managers (code bạn đã có)
from server.handler import ClientHandler
from server import room_manager
from server import user_manager
from server import db

# ================== CONFIG ==================
IP = "0.0.0.0"
CONTROL_PORT = 1222
AUDIO_PORT = 1234

clients = []          # danh sách client control
audio_clients = []    # danh sách client audio


# ================== CONTROL SERVER ==================
def start_control_server():
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((IP, CONTROL_PORT))
        server_socket.listen(5)
        print(f"[SERVER] Control server listening on {IP}:{CONTROL_PORT}")
    except Exception as e:
        print(f"[ERROR] Failed to start control server: {e}")
        return

    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f"[CONTROL] New connection from {addr}")

            client_handler = ClientHandler(
                client_socket,
                addr,
                clients,
                room_manager.room_manager,
                user_manager.user_manager,
                db.db,
            )
            clients.append(client_handler)
            client_handler.start()
        except Exception as e:
            print(f"[ERROR] Control connection error: {e}")


# ================== AUDIO SERVER ==================
def handle_audio_client(conn, addr):
    print(f"[AUDIO] Connected {addr}")
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            # broadcast tới các audio client khác
            for c in audio_clients:
                if c != conn:
                    c.sendall(data)
    except Exception as e:
        print(f"[AUDIO ERROR] {e}")
    finally:
        conn.close()
        if conn in audio_clients:
            audio_clients.remove(conn)
        print(f"[AUDIO] Disconnected {addr}")


def start_audio_server():
    try:
        audio_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        audio_sock.bind((IP, AUDIO_PORT))
        audio_sock.listen(5)
        print(f"[SERVER] Audio server listening on {IP}:{AUDIO_PORT}")
    except Exception as e:
        print(f"[ERROR] Failed to start audio server: {e}")
        return

    while True:
        conn, addr = audio_sock.accept()
        audio_clients.append(conn)
        threading.Thread(target=handle_audio_client, args=(conn, addr), daemon=True).start()


# ================== MAIN ==================
if __name__ == "__main__":
    try:
        threading.Thread(target=start_control_server, daemon=True).start()
        threading.Thread(target=start_audio_server, daemon=True).start()
        print("[SERVER] Control + Audio servers are running...")

        # giữ main thread sống
        while True:
            pass
    except KeyboardInterrupt:
        print("[SERVER] Shutting down...")
        for client in clients:
            client.stop()

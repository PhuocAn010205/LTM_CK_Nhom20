import socket
from server.handler import ClientHandler
from server.user_manager import UserManager
from server.room_manager import RoomManager

HOST = '0.0.0.0'  # Lắng nghe trên tất cả các interface mạng
PORT = 65432      # Cổng mà server sẽ chạy

def main():
    # Khởi tạo các đối tượng quản lý trung tâm
    user_manager = UserManager()
    room_manager = RoomManager()

    # Thiết lập socket server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5) # Cho phép tối đa 5 kết nối trong hàng đợi
    print(f"[*] Server đang lắng nghe trên {HOST}:{PORT}")

    try:
        while True:
            # Chấp nhận kết nối mới từ client
            client_socket, client_address = server_socket.accept()
            
            # Tạo một luồng (thread) mới để xử lý client này
            # Truyền các đối tượng quản lý vào cho handler
            client_thread = ClientHandler(
                client_socket, 
                client_address, 
                user_manager, 
                room_manager
            )
            client_thread.start()

    except KeyboardInterrupt:
        print("\n[*] Server đang tắt...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox
import json
import socket
from client.video_audio_client import VideoAudioClient

class VideoCallGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng dụng Gọi Video")
        self.client = None
        self.sock = None
        self.audio_sock = None

        # ----------------- Khung Đăng nhập -----------------
        self.login_frame = tk.Frame(self.root)
        tk.Label(self.login_frame, text="Tên đăng nhập:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.login_frame, text="Mật khẩu:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self.login_frame, text="Đăng nhập", command=self.login).grid(row=2, column=0, columnspan=2, pady=5)
        tk.Button(self.login_frame, text="Đăng ký", command=self.show_register).grid(row=3, column=0, columnspan=2, pady=5)

        self.login_frame.pack()

        # ----------------- Khung Đăng ký -----------------
        self.register_frame = tk.Frame(self.root)
        tk.Label(self.register_frame, text="Tên đăng nhập mới:").grid(row=0, column=0, padx=5, pady=5)
        self.reg_username_entry = tk.Entry(self.register_frame)
        self.reg_username_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Mật khẩu mới:").grid(row=1, column=0, padx=5, pady=5)
        self.reg_password_entry = tk.Entry(self.register_frame, show="*")
        self.reg_password_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Xác nhận mật khẩu:").grid(row=2, column=0, padx=5, pady=5)
        self.reg_confirm_entry = tk.Entry(self.register_frame, show="*")
        self.reg_confirm_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.register_frame, text="Email:").grid(row=3, column=0, padx=5, pady=5)
        self.reg_email_entry = tk.Entry(self.register_frame)
        self.reg_email_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self.register_frame, text="Xác nhận", command=self.register).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(self.register_frame, text="Quay lại Đăng nhập", command=self.show_login).grid(row=5, column=0, columnspan=2, pady=5)

        self.register_frame.pack_forget()

        # ----------------- Khung Phòng -----------------
        self.room_frame = tk.Frame(self.root)
        tk.Label(self.room_frame, text="Chọn phòng:").grid(row=0, column=0, padx=5, pady=5)
        self.room_var = tk.StringVar(value="Phòng 1")
        tk.OptionMenu(self.room_frame, self.room_var, "Phòng 1", "Phòng 2", "Phòng 3").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.room_frame, text="Vào phòng", command=self.join_room).grid(row=1, column=0, columnspan=2, pady=10)
        tk.Button(self.room_frame, text="Rời phòng", command=self.leave_room).grid(row=2, column=0, columnspan=2, pady=5)
        self.room_frame.pack_forget()

        # ----------------- Khung Video -----------------
        self.video_frame = tk.Frame(self.root)
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack()
        tk.Button(self.video_frame, text="Kết thúc cuộc gọi", command=self.leave_room).pack(pady=5)
        self.video_frame.pack_forget()

    # ----------------- Chuyển khung -----------------
    def show_register(self):
        self.login_frame.pack_forget()
        self.register_frame.pack()

    def show_login(self):
        self.register_frame.pack_forget()
        self.login_frame.pack()

    # ----------------- Xử lý Đăng ký -----------------
    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()
        email = self.reg_email_entry.get()

        if not username or not password or not email:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin")
            return
        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu không khớp")
            return

        register_packet = {
            "type": "register",
            "username": username,
            "password": password,
            "email": email
        }
        packet = json.dumps(register_packet).encode("utf-8")

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", 1222))  # chỉnh IP/port theo server
            sock.sendall(packet)
            response = sock.recv(4096).decode("utf-8")
            response_data = json.loads(response)
            sock.close()

            if response_data.get("status") == "success":
                messagebox.showinfo("Thành công", "Đăng ký thành công, vui lòng đăng nhập")
                self.show_login()
            else:
                messagebox.showerror("Lỗi", "Đăng ký thất bại: " + response_data.get("message", ""))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Kết nối thất bại: {e}")

    # ----------------- Xử lý Đăng nhập -----------------
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu")
            return

        login_packet = {
            "type": "login",
            "username": username,
            "password": password
        }
        packet = json.dumps(login_packet).encode('utf-8')

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(("127.0.0.1", 1222))  # chỉnh IP/port theo server
            self.sock.sendall(packet)
            response = self.sock.recv(4096).decode('utf-8')
            response_data = json.loads(response)

            if response_data.get("status") == "success":
                messagebox.showinfo("Thành công", "Đăng nhập thành công")
                self.login_frame.pack_forget()
                self.room_frame.pack()
            else:
                messagebox.showerror("Lỗi", "Sai thông tin đăng nhập")
                self.sock.close()
                self.sock = None
        except Exception as e:
            messagebox.showerror("Lỗi", f"Kết nối thất bại: {e}")
            self.sock = None

    # ----------------- Vào phòng -----------------
    def join_room(self):
        room = self.room_var.get()
        if not self.sock or not self.audio_sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(("127.0.0.1", 1222))
            self.audio_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.audio_sock.connect(("127.0.0.1", 1234))
            self.client = VideoAudioClient("Client")
            self.client.start(self.sock, self.audio_sock)

        join_packet = {"type": "join", "room": room}
        packet = json.dumps(join_packet).encode("utf-8")
        self.sock.sendall(packet)
        response = self.sock.recv(4096).decode("utf-8")
        if json.loads(response).get("status") == "success":
            messagebox.showinfo("Thành công", f"Đã vào {room}")
            self.room_frame.pack_forget()
            self.video_frame.pack()
        else:
            messagebox.showerror("Lỗi", "Không thể vào phòng")

    # ----------------- Rời phòng -----------------
    def leave_room(self):
        if self.client and self.sock and self.audio_sock:
            leave_packet = {"type": "leave", "room": self.room_var.get()}
            packet = json.dumps(leave_packet).encode("utf-8")
            self.sock.sendall(packet)
            response = self.sock.recv(4096).decode("utf-8")
            if json.loads(response).get("status") == "success":
                self.client.end()
                self.sock.close()
                self.audio_sock.close()
                self.client = None
                self.sock = None
                self.audio_sock = None
                messagebox.showinfo("Thành công", "Đã rời phòng")
                self.video_frame.pack_forget()
                self.room_frame.pack()
            else:
                messagebox.showerror("Lỗi", "Không thể rời phòng")

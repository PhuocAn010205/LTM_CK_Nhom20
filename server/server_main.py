import socket, cv2, pickle
from threading import Thread
from time import sleep
import pyaudio
from array import array

HEADERSIZE = 10
chunk = 1024  
sample_format = pyaudio.paInt16  
channels = 2
fs = 44100  

class ClientHandler:
    def __init__(self, i, clientsocket, audiosocket):
        self.i = i
        self.threads = []
        self.stop = False
        self.clientsocket = clientsocket
        self.audiosocket = audiosocket
        self.p = pyaudio.PyAudio() 
        self.stream = self.p.open(format=sample_format, channels=channels, rate=fs,
                                  frames_per_buffer=chunk, input=True, output=True)

    def handle(self, clientsocket, audiosocket):
        print(f"[SERVER] Client {self.i} connected.")
        while not self.stop:
            try:
                # Nhận video
                data = b""
                msg_size = int(clientsocket.recv(HEADERSIZE))
                while len(data) < msg_size:
                    data += clientsocket.recv(4096)

                # Nhận audio
                audio_data = audiosocket.recv(4096)

                # Gửi lại cho client còn lại
                o = 1 if (self.i == 0) else 0
                clients[o].clientsocket.sendall(bytes("{:<{}}".format(len(data), HEADERSIZE), 'utf-8') + data)

                if len(audio_data) == 4096:
                    self.stream.write(audio_data)
                    clients[o].audiosocket.sendall(audio_data)

            except Exception as e:
                print(f"[ERROR] {e}")
                break
        print(f"[SERVER] Client {self.i} stopped.")

    def start(self):
        t = Thread(target=self.handle, args=(self.clientsocket, self.audiosocket))
        self.stop = False
        t.start()
        self.threads.append(t)

    def end(self):
        self.stop = True
        self.clientsocket.close()
        self.audiosocket.close()
        for t in self.threads:
            t.join()
        self.stream.close()
        self.p.terminate()


# ======================
# SERVER MAIN
# ======================
IP = "0.0.0.0"   # Lắng nghe tất cả IP
PORT_VIDEO = 1222
PORT_AUDIO = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT_VIDEO))
s.listen()

audio_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_s.bind((IP, PORT_AUDIO))
audio_s.listen()

print(f"[SERVER] Listening on VIDEO:{PORT_VIDEO}, AUDIO:{PORT_AUDIO}")

clients = []
for i in range(2):
    print(f"[SERVER] Waiting for client {i}...")
    clientsocket, addr = s.accept()
    print(f"[SERVER] Client {i} VIDEO connected from {addr}")
    audiosocket, addr = audio_s.accept()
    print(f"[SERVER] Client {i} AUDIO connected from {addr}")
    obj = ClientHandler(i, clientsocket, audiosocket)
    clients.append(obj)

clients[0].start()
clients[1].start()

input("[SERVER] Press ENTER to stop server...\n")
print("[SERVER] Closing all...")
for obj in clients:
    obj.end()
s.close()
audio_s.close()
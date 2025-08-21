import socket, cv2, pickle
from threading import Thread
from time import sleep
import pyaudio

HEADERSIZE = 10
chunk = 1024  
sample_format = pyaudio.paInt16  
channels = 2
fs = 44100  

class VideoAudioClient:
    def __init__(self, name):
        self.threads = []
        self.stop = False
        self.name = name
        self.p = pyaudio.PyAudio() 
        self.stream = self.p.open(format=sample_format,
                                  channels=channels,
                                  rate=fs,
                                  frames_per_buffer=chunk,
                                  input=True,
                                  output=True)

    def send_video(self, sock):
        cam = cv2.VideoCapture(0)
        cam.set(3, 320)
        cam.set(4, 240)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        while not self.stop:
            ret, frame = cam.read()
            if not ret:
                continue
            try:
                result, frame = cv2.imencode('.jpg', frame, encode_param)
            except:
                continue
            data = pickle.dumps(frame, 0)
            size = len(data)
            sock.sendall(bytes("{:<{}}".format(size, HEADERSIZE), 'utf-8') + data)
            sleep(0.05)
        cam.release()

    def recv_video(self, sock):
        while not self.stop:
            try:
                data = b""
                msg_size = int(sock.recv(HEADERSIZE))
                while len(data) < msg_size:
                    data += sock.recv(4096)
                frame = pickle.loads(data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow(self.name, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop = True
                    break
            except:
                continue
        cv2.destroyAllWindows()

    def send_audio(self, sock):
        while not self.stop:
            try:
                data = self.stream.read(chunk)
                sock.sendall(data)
            except:
                continue

    def recv_audio(self, sock):
        while not self.stop:
            try:
                data = sock.recv(4096)
                if data:
                    self.stream.write(data)
            except:
                continue

    def start(self, sock, audio_sock):
        t1 = Thread(target=self.send_video, args=(sock,))
        t2 = Thread(target=self.recv_video, args=(sock,))
        t3 = Thread(target=self.send_audio, args=(audio_sock,))
        t4 = Thread(target=self.recv_audio, args=(audio_sock,))
        self.stop = False
        for t in [t1, t2, t3, t4]:
            t.start()
            self.threads.append(t)

    def end(self):
        self.stop = True
        for t in self.threads:
            t.join()
        self.stream.close()
        self.p.terminate()


# ======================
# CLIENT MAIN
# ======================
# 👉 Thay IP này bằng IP thật của máy server (xem bằng ipconfig)
IP = "192.168.1.3"   
PORT_VIDEO = 1222
PORT_AUDIO = 1234

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT_VIDEO))
print("[CLIENT] Connected to video server")

audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
audio_socket.connect((IP, PORT_AUDIO))
print("[CLIENT] Connected to audio server")

obj = VideoAudioClient("Client")
obj.start(s, audio_socket)

input("Press ENTER to stop...\n")
obj.end()
s.close()
audio_socket.close()
File client_tw_av.py
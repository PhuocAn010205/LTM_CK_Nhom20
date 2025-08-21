import socket
import cv2
import pickle
import threading
import pyaudio
import numpy as np

HEADERSIZE = 10
CHUNK = 1024
SAMPLE_FORMAT = pyaudio.paInt16
CHANNELS = 2
FS = 44100

class VideoAudioClient:
    def __init__(self, name):
        self.name = name
        self.threads = []
        self.stop = False
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=SAMPLE_FORMAT, channels=CHANNELS, rate=FS,
                                 frames_per_buffer=CHUNK, input=True, output=True)
        self.sock = None
        self.audio_sock = None

    def send_video(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 320)
        cap.set(4, 240)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        while not self.stop:
            ret, frame = cap.read()
            if not ret:
                continue
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            data = pickle.dumps(frame, 0)
            size = len(data)
            self.sock.sendall(bytes(f"{size:<{HEADERSIZE}}", 'utf-8') + data)
        cap.release()

    def recv_video(self):
        while not self.stop:
            try:
                data = b""
                msg_size = int(self.sock.recv(HEADERSIZE))
                while len(data) < msg_size:
                    data += self.sock.recv(4096)
                frame = pickle.loads(data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow(self.name, frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop = True
            except:
                continue
        cv2.destroyAllWindows()

    def send_audio(self):
        while not self.stop:
            try:
                data = self.stream.read(CHUNK)
                self.audio_sock.sendall(data)
            except:
                continue

    def recv_audio(self):
        while not self.stop:
            try:
                data = self.audio_sock.recv(4096)
                if data:
                    self.stream.write(data)
            except:
                continue

    def start(self, sock, audio_sock):
        self.sock = sock
        self.audio_sock = audio_sock
        t1 = threading.Thread(target=self.send_video)
        t2 = threading.Thread(target=self.recv_video)
        t3 = threading.Thread(target=self.send_audio)
        t4 = threading.Thread(target=self.recv_audio)
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
        if self.sock:
            self.sock.close()
        if self.audio_sock:
            self.audio_sock.close()
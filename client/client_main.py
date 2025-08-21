import socket
from client import gui
from client.video_audio_client import VideoAudioClient

if __name__ == "__main__":
    root = gui.tk.Tk()
    app = gui.VideoCallGUI(root)
    root.mainloop()
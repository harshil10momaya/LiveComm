import socket
import pyaudio
import numpy as np
import threading

HOST = "172.20.10.6"
PORT = 5000
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK_SIZE = 2048

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")
audio = pyaudio.PyAudio()

def send_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK_SIZE)
    while True:
        try:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            client_socket.sendall(data)
        except:
            break
    stream.close()

def recv_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK_SIZE)
    while True:
        try:
            data = client_socket.recv(CHUNK_SIZE)
            if not data:
                break
            stream.write(data)
        except:
            break
    stream.close()

send_thread = threading.Thread(target=send_audio)
recv_thread = threading.Thread(target=recv_audio)
send_thread.start()
recv_thread.start()

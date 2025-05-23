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

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")
clients = []
audio = pyaudio.PyAudio()

def broadcast_audio(data, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(data)
            except:
                clients.remove(client)

def handle_client(client_socket):
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK_SIZE)
    while True:
        try:
            data = client_socket.recv(CHUNK_SIZE)
            if not data:
                break
            stream.write(data)
            broadcast_audio(data, client_socket)
        except:
            break
    client_socket.close()
    clients.remove(client_socket)
    stream.close()

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")
    clients.append(client_socket)
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()

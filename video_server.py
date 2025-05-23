import socket
import cv2
import pickle
import struct
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '172.20.10.6'
port = 9999
server_socket.bind((host_ip, port))
server_socket.listen()
print(f"Server is listening on {host_ip}:{port}")
clients = []
server_video = cv2.VideoCapture(0)

def handle_client(client_socket, addr):
    global clients
    print(f"New connection from {addr}")
    clients.append(client_socket)
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet:
                    break
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data)
            cv2.imshow(f"Client {addr}", frame)
            cv2.waitKey(1)
            broadcast(frame, client_socket)
        except:
            break
    print(f"Client {addr} disconnected")
    clients.remove(client_socket)
    client_socket.close()

def broadcast(frame, sender_socket):
    data = pickle.dumps(frame)
    message = struct.pack("Q", len(data)) + data
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message)
            except:
                clients.remove(client)

def send_server_video():
    while True:
        _, frame = server_video.read()
        if frame is None:
            break
        broadcast(frame, None)
        cv2.imshow("Server Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

server_video_thread = threading.Thread(target=send_server_video, daemon=True)
server_video_thread.start()

while True:
    client_socket, addr = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_socket, addr), daemon=True)
    client_thread.start()

import socket
import cv2
import pickle
import struct
import threading

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '172.20.10.6'
port = 9999
client_socket.connect((server_ip, port))
vid = cv2.VideoCapture(0)

def send_video():
    while vid.isOpened():
        _, frame = vid.read()
        if frame is None:
            break
        data = pickle.dumps(frame)
        message = struct.pack("Q", len(data)) + data
        client_socket.sendall(message)
        cv2.imshow("Your Video", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def receive_video():
    data = b""
    payload_size = struct.calcsize("Q")
    while True:
        try:
            while len(data) < payload_size:
                packet = client_socket.recv(4 * 1024)
                if not packet:
                    return
                data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size)[0]
            while len(data) < msg_size:
                data += client_socket.recv(4 * 1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("Others' Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except:
            break

send_thread = threading.Thread(target=send_video, daemon=True)
receive_thread = threading.Thread(target=receive_video, daemon=True)
send_thread.start()
receive_thread.start()
send_thread.join()
receive_thread.join()
client_socket.close()
vid.release()
cv2.destroyAllWindows()

# Real-Time Video & Audio Conferencing System

**Developed by:**  
23PT11 – Harshil Bhavik Momaya  
23PT37 – Vaishnavi V

## Abstract

This project is a **Real-Time Video & Audio Conferencing System** that enables bi-directional video and audio transmission between multiple clients over a network.

The system begins with the server initializing sockets for both video and audio streaming. Clients connect to the server, establishing a real-time communication channel for seamless video and voice interaction. Multiple users can communicate simultaneously.

---

## 🔑 Key Concepts Used

- **Multithreading:** Enables concurrent handling of multiple clients.
- **Socket Programming:** Facilitates communication between server and clients over TCP.
- **Serialization (Fragmentation):** `pickle` is used for video frame transmission.
- **Audio Processing:** `pyaudio` is used for capturing, transmitting, and playing real-time audio.
- **Video Processing:** `OpenCV` is used for webcam access and frame rendering.
- **TCP Communication:** Ensures reliable and ordered transmission of video and audio data.
- **Packetization:** Video and audio streams are broken into smaller packets for transmission.
- **Flow Control & Congestion Handling:** Prevents data loss and ensures smooth media streaming.
- **Error Detection & Recovery:** Mechanisms to handle packet loss and maintain stable connections.
- **Data Streaming:** Continuous transmission of video and audio without buffering delays.
- **Broadcasting:** The server distributes video and audio streams to all connected clients.

---

## 📦 Modules Used

- `socket`
- `cv2` (OpenCV)
- `pyaudio`
- `pickle`
- `struct`
- `threading`
- `numpy`

---

## 🚀 Future Scope & Improvements

- **Enhanced UI:** Implementing a graphical interface using Tkinter or PyQt.
- **Encryption:** Adding end-to-end encryption (E2EE) for secure transmission using TLS/SSL.
- **Screen Sharing & Chat Features:** Extending functionality beyond just video and audio.
- **Use UDP for Video Streaming:** Optimizing video/audio synchronization and latency.

---

This system serves as a foundation for a **Google Meet-like video conferencing solution**, providing a real-time communication experience over the network.


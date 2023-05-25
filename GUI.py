import cv2
import socket
import struct
import numpy as np

# Raspberry Pi IP address and port
HOST = '172.20.10.2'
PORT = 8000

def start_video_stream():
    # Initialize OpenCV video capture
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)  # Set width
    cap.set(4, 480)  # Set height

    # Create socket and bind it to the specified address and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print('Streaming server started')

    while True:
        # Accept a client connection
        client_socket, addr = server_socket.accept()
        print('Client connected:', addr)

        try:
            while True:
                # Capture frame from the camera
                ret, frame = cap.read()

                # Encode frame as JPEG
                _, encoded_frame = cv2.imencode('.jpg', frame)

                # Convert JPEG frame to bytes
                frame_data = np.array(encoded_frame).tobytes()

                # Get frame size and pack it into a struct
                frame_size = len(frame_data)
                frame_size_data = struct.pack('!L', frame_size)

                # Send frame size to the client
                client_socket.sendall(frame_size_data)

                # Send frame data to the client
                client_socket.sendall(frame_data)

        except ConnectionResetError:
            print('Client disconnected')
            client_socket.close()

    # Release resources
    server_socket.close()
    cap.release()
    print('Streaming server stopped')

if _name_ == '_main_':
    start_video_stream()
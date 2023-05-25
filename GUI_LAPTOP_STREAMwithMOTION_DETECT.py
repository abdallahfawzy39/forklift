import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import socket
import struct
import io

# Set up the GUI window
window = tk.Tk()
window.title("Raspberry Pi Camera Stream")

# Create a label to display the video stream
video_label = tk.Label(window)
video_label.pack()

# Raspberry Pi IP address and port
HOST = '192.168.1.13'
PORT = 8000

# Create a socket connection to the Raspberry Pi server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
connection = client_socket.makefile('rb')

# Parameters for motion detection
frame_difference_threshold = 30
min_contour_area = 5000

# Variable to store the previous frame
prev_frame = None

def detect_motion(frame):
    global prev_frame

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the grayscale image
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)

    # If there is no previous frame, store the current frame and return
    if prev_frame is None:
        prev_frame = blurred
        return False

    # Compute the absolute difference between the current frame and the previous frame
    frame_diff = cv2.absdiff(prev_frame, blurred)

    # Apply a threshold to the frame difference image
    _, threshold = cv2.threshold(frame_diff, frame_difference_threshold, 255, cv2.THRESH_BINARY)

    # Perform morphological operations to remove noise
    kernel = np.ones((5, 5), np.uint8)
    threshold = cv2.morphologyEx(threshold, cv2.MORPH_OPEN, kernel, iterations=2)
    threshold = cv2.dilate(threshold, kernel, iterations=2)

    # Find contours of the moving objects
    contours, _ = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contour satisfies the minimum area requirement
    large_object_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > min_contour_area:
            large_object_detected = True
            break

    # Update the previous frame with the current frame
    prev_frame = blurred

    return large_object_detected

def update_frame():
    try:
        # Read frame size from the server
        frame_size_data = connection.read(struct.calcsize('!L'))
        if not frame_size_data:
            return
        frame_size = struct.unpack('!L', frame_size_data)[0]

        # Read frame data from the server
        frame_data = connection.read(frame_size)
        if not frame_data:
            return

        # Convert frame data to a numpy array
        frame = np.frombuffer(frame_data, dtype=np.uint8)

        # Decode frame as JPEG
        img = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        # Detect motion of large objects
        motion_detected = detect_motion(img)

        # Display motion detection message if motion is detected
        if motion_detected:
            print("Motion detected!")

        # Convert the frame from BGR to RGB
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Create a PIL image from the frame
        pil_image = Image.fromarray(frame_rgb)

        # Resize the image to fit the window
        resized_image = pil_image.resize((640, 480))

        # Create an ImageTk object
        image_tk = ImageTk.PhotoImage(resized_image)

        # Update the video label with the new image
        video_label.configure(image=image_tk)
        video_label.image = image_tk

    except Exception as e:
        print("Error:", str(e))

    # Schedule the next frame update
    window.after(10, update_frame)

# Start updating the frames
update_frame()

# Start the GUI event loop
window.mainloop()

# Release resources
connection.close()
client_socket.close()
import RPi.GPIO as GPIO
import serial
import time

# Set up serial communication with Arduino for Motor 1
ser1 = serial.Serial('/dev/ttyACM0', 9600)  # Adjust the port name if needed

# Set up serial communication with Arduino for Motor 2
ser2 = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust the port name if needed
while True:
# Set GPIO mode and pin numbers for ultrasonic sensor 1
    if ser1.in_waiting > 0:
        message = ser1.readline().decode().strip()
        print("Received message from Arduino:", message)

        # Send a message to the second Arduino based on the message received from the first Arduino
        if message == "mid":
            ser2.write(b'a')
            print("Sent 'a' message to second Arduino")
        elif message == "stop":
            ser2.write(b'b')
            print("Sent 'b' message to second Arduino")
        elif message == "left":
            ser2.write(b'c')
            print("Sent 'c' message to second Arduino")
        elif message == "left left":
            ser2.write(b'd')
            print("Sent 'd' message to second Arduino")
        elif message == "right":
            ser2.write(b'e')
            print("Sent 'e' message to second Arduino")
        elif message == "right right":
            ser2.write(b'f')
            print("Sent 'f' message to second Arduino")

    time.sleep(0.3) # wait for 100 milliseconds before checking for new messages
import socket
import random

# Define the IP address and port to listen on
HOST = '172.20.10.2'  # Pi's IP address
PORT = 5000

# Create a server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print('Waiting for a connection...')

# Accept a client connection
client_socket, client_address = server_socket.accept()
print('Connected to:', client_address)

while True:
    # Generate a random number between 0 and 100
    number = random.randint(0, 100)

    # Send the number as a string
    client_socket.send(str(number).encode())

# Close the socket
client_socket.close()
server_socket.close()
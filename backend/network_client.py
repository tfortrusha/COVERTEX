import socket
import struct

SERVER_IP = "127.0.0.1"
PORT = 5000
FILE_PATH = "stego.png"

with open(FILE_PATH, "rb") as file:
    image_data = file.read()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with client:
    client.connect((SERVER_IP, PORT))

    # Send file size first
    client.sendall(struct.pack("!Q", len(image_data)))

    # Send the complete image
    client.sendall(image_data)

print(f"Sent {len(image_data)} bytes to Device B")
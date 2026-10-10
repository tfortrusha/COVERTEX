import socket
import struct

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print(f"Device B waiting on {HOST}:{PORT}...")

connection, address = server.accept()

with connection:
    print("Connected by:", address)

    # Receive the file size (8 bytes)
    size_data = connection.recv(8)

    if len(size_data) != 8:
        raise ValueError("Invalid file size header")

    file_size = struct.unpack("!Q", size_data)[0]

    # Receive the complete file
    received = bytearray()

    while len(received) < file_size:
        chunk = connection.recv(
            min(4096, file_size - len(received))
        )
        if not chunk:
            raise ConnectionError("Connection closed prematurely")
        received.extend(chunk)

    with open("received_stego.png", "wb") as file:
        file.write(received)

    print(f"Received {len(received)} bytes")
    print("Saved as received_stego.png")

server.close()
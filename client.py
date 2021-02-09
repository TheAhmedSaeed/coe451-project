# this is the player (client) file

import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DESCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)


def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))
    print(client.recv(2048).decode(FORMAT))


send("hi")

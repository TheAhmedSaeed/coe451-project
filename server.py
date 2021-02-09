# this is the game hosting (server) file

import socket
import threading

from gameLogic import checkInputValidity, calculateWinner, drawBoard, pickALocation

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DESCONNECT_MESSAGE = "!DISCONNECT"

innitial_board = ['1', '2', '3',
                  '4', '5', '6',
                  '7', '8', '9']

board = ['', '', '',
        '', '', '',
         '', '', '']


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)


def handle_client(connection, address):
    
    connection.send(f"[NEW Game] {address} is playing \n".encode(FORMAT))
    connection.send("I am X and you are O, please select a location to start playing\n".encode(FORMAT))
    connection.send(drawBoard(innitial_board).encode(FORMAT))
    connected = True
    while connected:
        location_selection = connection.recv(2048).decode()
        print(location_selection)
        # msg_length = connection.recv(HEADER).decode(FORMAT)
        # print(msg_length)
        # if(msg_length):
            # msg_length = int(msg_length)
            # msg = connection.recv(msg_length).decode(FORMAT)
            # if(msg == DESCONNECT_MESSAGE):
                # connected = False

            # print(f"[{ADDRESS}] {msg}")
            # connection.send("Message recieved".encode(FORMAT))


def start(): 
    server.listen()
    print(f"[LISTENING] Server is listening  {SERVER}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()

        # print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


def main():

    print("Server (game) is waiting to start...")
    start()


main()

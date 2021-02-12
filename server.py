# this is the game hosting (server) file

import socket
import threading

from gameLogic import checkInputValidity, calculateWinner, drawBoard, pickALocation,makeMove
from helper import getMsgLength,HEADER,SERVER_ADDRESS,FORMAT,SERVER,INNITIAL_BOARD,SERVER_PLAYER,CLIENT_PLAYER

# inoitial board
board = ['', '', '',
        '', '', '',
         '', '', '']


# conntecting server to the network
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)


def handle_client(connection, address):
    global board
    print("Game started with " + address)
    # startingMsg1 = f"[NEW Game] {address} is playing \n"
    


    startingMsg2 = drawBoard(INNITIAL_BOARD)
    startingMsgLength2 = getMsgLength(startingMsg2)
    connection.send(startingMsgLength2)
    connection.send(startingMsg2.encode(FORMAT))

    startingMsg = "I am X and you are O, please select a location to start playing\n"
    startingMsgLength = getMsgLength(startingMsg)
    connection.send(startingMsgLength)
    connection.send(startingMsg.encode(FORMAT))
    
    
    connected = True
    while connected:

        msg_length = connection.recv(HEADER).decode(FORMAT)
        if(msg_length):
            msg_length = int(msg_length)
            location_selection = connection.recv(msg_length).decode(FORMAT)
            if(checkInputValidity(location_selection, board)):
                
                #first we make the move for the player and check if they won and we send them back the board
                board = makeMove(int(location_selection) -1,CLIENT_PLAYER,board)
                connection.send(getMsgLength(drawBoard(board)))
                connection.send(drawBoard(board).encode(FORMAT))


                winner = calculateWinner(board)
                if(winner == CLIENT_PLAYER):
                    winningMsg = "You won, congrats 👏"
                    connection.send(getMsgLength(winningMsg))
                    connection.send(winningMsg.encode(FORMAT))
                
                # Then we make a move ourself and check if we won and send the board back to the player 
                makeMove(pickALocation(board),SERVER_PLAYER,board)
                connection.send(getMsgLength(drawBoard(board)))
                connection.send(drawBoard(board).encode(FORMAT))

                winner = calculateWinner(board)
                if(winner == SERVER_PLAYER):
                    winningMsg = "I won, good luck next time"
                    connection.send(getMsgLength(winningMsg))
                    connection.send(winningMsg.encode(FORMAT))
            
                promptingMsg = "It is your turn, please select a cell"
                connection.send(getMsgLength(promptingMsg))
                connection.send(promptingMsg.encode(FORMAT))

            else: 
                errorMsg = "Wrong choise.. please select a number from 1 to 9  and you can't select an already selected cell"
                connection.send(getMsgLength(errorMsg))
                connection.send(errorMsg.encode(FORMAT))
                



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

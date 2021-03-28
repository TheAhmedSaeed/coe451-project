# this is the game hosting (server) file

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

import socket
import threading

from gameLogic import checkInputValidity, calculateWinner, drawBoard, pickALocation,makeMove
from helper import getMsgLength,HEADER,SERVER_ADDRESS,FORMAT,SERVER,INNITIAL_BOARD,SERVER_PLAYER,CLIENT_PLAYER,KEYHEX,getMsgLengthForBytes

# inoitial board
board = ['', '', '',
        '', '', '',
         '', '', '']


# conntecting server to the network
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(SERVER_ADDRESS)


def handle_client(connection, address):
    global board

    initialMsg = f"Game started with {address} is playing"
    print(initialMsg)
    # startingMsg1 = f"[NEW Game] {address} is playing \n"
    
    ivMsg = "Server : Please send me the IV"
    connection.send(getMsgLength(ivMsg))
    connection.send(ivMsg.encode(FORMAT))
    
    
    connected = True
    hasIVBeenRecieved = False
    while connected:

       # We recieve the 1st msg that contains the length of the upconing msg. 
       # Both parties agree to recieve the header first which has an ugreed upon size (HEADER)
        if(not hasIVBeenRecieved):
            msg_length = connection.recv(HEADER).decode(FORMAT)
        else:
            msg_length = connection.recv(16)
        if(msg_length):
            


            if(not hasIVBeenRecieved):
                msg_length = int(msg_length)
                iv = connection.recv(msg_length)
                keyBytes = bytes.fromhex(KEYHEX)
                cipher = AES.new(keyBytes,AES.MODE_CBC,iv)
                print("iv has been recieved")
                hasIVBeenRecieved = True
                

                startingMsg2 = drawBoard(INNITIAL_BOARD)
                startingMsg2Ecrypted = cipher.encrypt(pad(str.encode(startingMsg2),AES.block_size))
                connection.send(startingMsg2Ecrypted)

                startingMsg = "I am X and you are O, please select a location to start playing\n"
                startingMsgEncrypted = cipher.encrypt(pad(str.encode(startingMsg),AES.block_size))

                connection.send(startingMsgEncrypted)




            else:    
                cipher = AES.new(keyBytes,AES.MODE_CBC,iv)
                location_selection =  unpad(cipher.decrypt(msg_length),AES.block_size)

                print(location_selection)
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

# this file contains function which help .. 
#  .. with anything other than the game logic

import socket

HEADER = 200
FORMAT = 'utf-8'
PORT = 3000
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)


INNITIAL_BOARD = ['1', '2', '3',
                  '4', '5', '6',
                  '7', '8', '9']
SERVER_PLAYER = "x"
CLIENT_PLAYER = "o"

# extends the message to match the header Size
def getMsgLength(msg):
    if(len(msg) > HEADER):
         raise Exception("Header Length can not exceed " + HEADER )
   
    if(len(msg) == HEADER):
        return msg
    
    msg = msg.encode(FORMAT)
    msgLength = len(msg)
    headerMsgLength = str(msgLength).encode(FORMAT)
    # we add spaces here to extend the header to match the agreed upon header length
    headerMsgLength += b' ' * (HEADER - len(headerMsgLength))
    
    return headerMsgLength
    

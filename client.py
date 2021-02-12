# this is the player (client) file
import socket

from helper import getMsgLength,HEADER,SERVER_ADDRESS,FORMAT


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)





def start():
    print("Player connected to ", SERVER_ADDRESS)
    client.connect(SERVER_ADDRESS)
    
    #recieving first 2 innitial messages
    
    connected = True
    while connected:
        # We recieve the 1st msg that contains the length of the upconing msg. 
       # Both parties agree to recieve the header first which has an ugreed upon size
        msg_length = client.recv(HEADER).decode(FORMAT)
        if(msg_length):
            msg_length = int(msg_length)
            recieveddMsg = client.recv(msg_length).decode(FORMAT)
            print(recieveddMsg)
            if("won" in recieveddMsg):
                print("Gamed ended")
                client.close()
                connected= False
            elif("select" in recieveddMsg): 
                location = input("Enter your selecetion: \n")
                locationLength = getMsgLength(location)
                client.send(locationLength)
                client.send(location.encode(FORMAT))


start()

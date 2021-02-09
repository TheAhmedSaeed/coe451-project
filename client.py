# this is the player (client) file

import socket

from helper import getMsgLength,HEADER,ADDRESS,FORMAT


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)





def start():
    client.connect(ADDRESS)
    
    #recieving first 2 innitial messages
    
    connected = True
    while connected:
        msg_length = client.recv(HEADER).decode(FORMAT)
        print(msg_length)
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

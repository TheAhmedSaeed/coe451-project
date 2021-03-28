# this is the player (client) file
import socket

from helper import getMsgLength,HEADER,SERVER_ADDRESS,FORMAT,KEYHEX,getMsgLengthForBytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto import  Random


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)





def start():
    print("Player connected to ", SERVER_ADDRESS)
    client.connect(SERVER_ADDRESS)
    
    
    iv = Random.new().read(AES.block_size)
    keyBytes = bytes.fromhex(KEYHEX)
    cipher = AES.new(keyBytes,AES.MODE_CBC,iv)

    
    connected = True
    ivWasSent = False
    wasStartingMsg1Recieved = False
    wasStartingMsg2Recieved = False
    while connected:

        if( ivWasSent and not wasStartingMsg1Recieved):
            recieveddMsg = client.recv(64)

            msg = unpad(cipher.decrypt(recieveddMsg),AES.block_size)
            print(msg.decode())
            wasStartingMsg1Recieved = True

        elif(ivWasSent and not wasStartingMsg2Recieved):
            recieveddMsg = client.recv(80)
            msg = unpad(cipher.decrypt(recieveddMsg),AES.block_size)
            print(msg.decode())
            wasStartingMsg2Recieved = True
            location = input("Enter your selecetion: \n")

            cipher = AES.new(keyBytes,AES.MODE_CBC,iv)
            locationEncrypted = cipher.encrypt(pad(str.encode(location),AES.block_size))
            client.send(locationEncrypted)



        else:

        # We recieve the 1st msg that contains the length of the upconing msg. 
       # Both parties agree to recieve the header first which has an ugreed upon size
            if(ivWasSent):
                msg_length = client.recv(HEADER)
            else:
                msg_length = client.recv(HEADER).decode(FORMAT)

            if(msg_length):    
                msg_length = int(msg_length)
                recieveddMsg = client.recv(msg_length).decode(FORMAT)
                print(recieveddMsg)
                if( "IV" in recieveddMsg):
                    ivLength = getMsgLengthForBytes(iv)
                    client.send(ivLength)
                    client.send(iv)
                    ivWasSent = True
                elif("won" in recieveddMsg):
                    print("Gamed ended")
                    client.close()
                    connected= False
                elif("select" in recieveddMsg): 
                    location = input("Enter your selecetion: \n")
                    cipher = AES.new(keyBytes,AES.MODE_CBC,iv)
                    locationEncrypted = cipher.encrypt(pad(str.encode(location),AES.block_size))
                    client.send(locationEncrypted)


start()

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

    # boolean vriables to control the flow of comminication
    ivWasSent = False
    startingMsg1WasRecieved = False
    startingMsg2WasRecieved = False


    # The server tells the client before hand that the first 
    # two handshakes (if you will) will have this length 
    FIRSTMSGLENGTH = 64
    SECONDMSGLENGTH = 80

    

    while connected:

        # If we have sent the IV but have not recieved the 1st message AS AGREED beforehand
        if( ivWasSent and not startingMsg1WasRecieved):
            recieveddMsg = client.recv(FIRSTMSGLENGTH)
            print("Ciphertext recieved from the server {}".format(recieveddMsg))
            msg = unpad(cipher.decrypt(recieveddMsg),AES.block_size)
            print("Plain text after decrypting\n {}".format(msg.decode()))
            startingMsg1WasRecieved = True

        # If we have sent the IV but have not recieved the 2nd message AS AGREED beforehand
        elif(ivWasSent and not startingMsg2WasRecieved):
            recieveddMsg = client.recv(SECONDMSGLENGTH)
            print("Ciphertext recieved from the server {}".format(recieveddMsg.hex()))
            msg = unpad(cipher.decrypt(recieveddMsg),AES.block_size)
            print("Pain text after decrypting")
            print(msg.decode())
            startingMsg2WasRecieved = True
            
            # This piece of code is executed only once. When we recieve the 2nd msg and start playing
            # In other words, this is only the first selecion

            location = input("Enter your selecetion: \n")
            cipher = AES.new(keyBytes,AES.MODE_CBC,iv)
            locationEncrypted = cipher.encrypt(pad(str.encode(location),AES.block_size))
            client.send(locationEncrypted)



        else:
        # We recieve the 1st msg that contains the length of the upconing msg. 
       # Both parties agree to recieve the header first which has an ugreed upon size
            if(ivWasSent):
                msg_length = client.recv(HEADER)
            
            #If we have:
            # 1. Sent the IV
            # 2. Recieved the first 2 messages
            else:
                msg_length = client.recv(HEADER).decode(FORMAT)

            if(msg_length):    
                msg_length = int(msg_length)
                recieveddMsg = client.recv(msg_length).decode(FORMAT)
                print(recieveddMsg)
                if( "IV" in recieveddMsg):
                    client.send(iv)
                    ivWasSent = True
                elif("won" in recieveddMsg):
                    print("Gamed ended")
                    client.close()
                    connected= False
                elif("select" in recieveddMsg): 
                    location = input("Enter your selecetion: \n")
                    print("Location selected {}".format(location))
                    cipher = AES.new(keyBytes,AES.MODE_CBC,iv)
                    locationEncrypted = cipher.encrypt(pad(str.encode(location),AES.block_size))
                    # Here we snd the encrypted location
                    client.send(locationEncrypted)


start()

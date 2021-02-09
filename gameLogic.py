# this file containts function which help with the game logic

# returns a string of the board to be printed to the user
from random import randrange
def drawBoard(board):
    printedBoard = ""
    if(len(board) != 9):
        print("Internal error")
    else: 
        for i in range(9):
            if(len(board[i]) > 0):
                printedBoard += (board[i] + " ")
            else: 
                printedBoard += ("  ")

            if(i==8):
                pass
            elif(i==2 or i == 5 ):
                printedBoard += ('\n---------\n')
            else: 
                printedBoard +=("|" + " ")

        printedBoard += "\n"
        return printedBoard


# a function to make a move
def makeMove(index,player,board):
    index = int(index)
    if(player == "x"):
        board[index] = player
    elif(player == "o"):
        board[index] = player
    
    return board


# calculates  the winner
def calculateWinner(board):
   
    if(board[0] == board[1] == board[2]):
        return board[0]
   
    elif(board[3] == board[4] == board[5]):
        return board[3]
   
    elif(board[6] == board[7] == board[8]):
        return board[6]
   
    elif(board[0] == board[3] == board[6]):
        return board[0]
   
    elif(board[1] == board[4] == board[7]):
        return board[1]
   
    elif(board[2] == board[5] == board[8]):
        return board[2]
        
    elif(board[1] == board[4] == board[7]):
        return board[3]
        
    elif(board[0] == board[4] == board[8]):
        return board[0]
        
    elif(board[2] == board[4] == board[6]):
        return board[2]
    
    # in case of no winner
    return ""


# checks for the chosen location validity 
def checkInputValidity(location,board):
    location = int(location)
    #index is location -1
    location -=1
    if(location > 9 or location < 0):
        return False
        
    elif(board[location] == "x" or board[location] == "o"):
        return False
    
    return True

# to be used by the server to pick a random location to play
def pickALocation(board):
    isPicked = False
    pickedLocation = -1
    while(not isPicked):
        temp = randrange(9)
        if(board[temp] != 'x' and board[temp] != 'o' ):
            pickedLocation = temp
            isPicked  = True
    
    return pickedLocation
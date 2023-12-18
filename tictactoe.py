import copy
import random

board_state = [['_'] * 3 for _ in range(3)] #Track board state, initialized empty

def draw_board(board_state):  

    #Draws the current state of the board  

    print("_{}_|_{}_|_{}_".format(board_state[0][0], board_state[0][1], board_state[0][2]))
    print("_{}_|_{}_|_{}_".format(board_state[1][0], board_state[1][1], board_state[1][2]))
    print(" {} | {} | {} ".format(' ' if board_state[2][0] == '_' else board_state[2][0],\
                                  ' ' if board_state[2][1] == '_' else board_state[2][1],\
                                  ' ' if board_state[2][2] == '_' else board_state[2][2]))
  
draw_board(board_state)

def player_choice():

    #Asks player whether they want to go first (X's) or second (O's)
    #and returns that choice

    player_input = ""

    while player_input not in ['X', 'O']:
        player_input = input("Would you like to go first (X) or second (O)?: ")
        
    return player_input

first_or_second = player_choice()           #Tracks if player is X's or O's


def three_in_a_row(board_state, X_or_O):

    #Checks each row, column and diagonal for three of the same symbol,
    #which is the win condition and returns True if so

    #Check if any row contains the same symbol in all cells
    for row in board_state:
        if all(cell == X_or_O for cell in row):
            return True
        
    #Check if any column contains the same symbol in all cells
    for col in range(3):
        if all(board_state[row][col] == X_or_O for row in range(3)):
            return True   

    #Check if any diagonal contains the same symbol in all cells
    if all(board_state[i][i] == X_or_O for i in range(3)) or all(board_state[i][2 - i] == X_or_O for i in range(3)):
        return True
    
    return False

player_turn = 'X'

def is_legal_move(board_state, row, col):

    #Determines if move is legal, based on whether the player has chosen
    #an empty square

    return -1 < row < 3 and -1 < col < 3 and board_state[row][col] == '_'

def switch_turn(X_or_O):

    #Returns the other player's symbol

    if X_or_O == 'X':                         #Switch current player
        return 'O'
    else:
        return 'X'
    
def collect_legal_moves(board_state, row ,col):

    #Creates and returns array for the computer to be able
    #to evaluate and choose moves

    legal_moves = []            #Determine remaining legal moves to see if there are game
    for row in range(3):     #ending moves and react accordingly
        for col in range(3):
            if is_legal_move(board_state, row ,col):
                legal_moves.append([row, col])

    return legal_moves

def find_win(board_state, legal_moves, X_or_O):

    #Finds and plays winning move for computer if available

    for move in legal_moves:
        temp_board_state = copy.deepcopy(board_state)   #Create temporary board_state to check for potential
        temp_board_state[move[0]][move[1]] = X_or_O     #winning moves
        if three_in_a_row(temp_board_state, X_or_O):                    
            draw_board(temp_board_state)
            print("{} wins!".format(X_or_O))
            return False
        
def find_block(board_state, legal_moves, X_or_O):

    #Finds and plays blocking move for computer if necessary

    for move in legal_moves:
        temp_board_state = copy.deepcopy(board_state)       #Create temporary board_state to check for potential winning moves
        temp_X_or_O = 'O' if X_or_O == 'X' else 'X'         #Envision board states with human's symbol played
        temp_board_state[move[0]][move[1]] = temp_X_or_O    
        if three_in_a_row(temp_board_state, temp_X_or_O):
            board_state[move[0]][move[1]] = X_or_O
            return switch_turn(X_or_O)

def find_corner(board_state, legal_moves, X_or_O):

    #Corner squares are the best position if the centre is occupied
    #and no winning move exists for either player

    corner_moves = [(0,0), (0,2), (2,0), (2,2)]     #Define all four corners
    legal_corner_moves = []                         #Find and collect
    for move in legal_moves:                        #available corner
        if tuple(move) in corner_moves:                    #moves
            legal_corner_moves.append(move)

    print(legal_moves, legal_corner_moves)

    if len(legal_corner_moves) > 0:                         #Play random corner if there
        random_corner = random.choice(legal_corner_moves)   #are any
        board_state[random_corner[0]][random_corner[1]] = X_or_O
        return switch_turn(X_or_O)

def next_move(board_state, turn, X_or_O):

    #Main game driver
    
    row, col = 3, 3             #Set row and col out of bounds so as not to trigger while condition

    if turn == X_or_O:          #Ask player for their move if it's their turn
        while not is_legal_move(board_state, row, col):
            row = int(input("Please input row"))
            col = int(input("Please input column"))
        
        board_state[row][col] = X_or_O

    else:
        if board_state[1][1] == '_':    #If the centre is not taken, taking it is the best move
            board_state[1][1] = X_or_O
        
        else:
            
            legal_moves = collect_legal_moves(board_state, row ,col)
            find_win(board_state, legal_moves, X_or_O)  
            find_block(board_state, legal_moves, X_or_O)          
            find_corner(board_state, legal_moves, X_or_O)            

    draw_board(board_state)
    
    if three_in_a_row(board_state, X_or_O):              #Check if anyone wins
        print("{} wins!".format(X_or_O))
        return False

    return switch_turn(X_or_O)

while True:
    first_or_second = next_move(board_state, player_turn, first_or_second)
    if not first_or_second:
        break
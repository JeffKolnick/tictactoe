
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


def three_in_a_row(X_or_O):

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

def next_move(board_state, turn, X_or_O):

    #Main game driver

    row, col = 3, 3

    if turn == X_or_O:          #Ask player for their move if it's their turn
        while not is_legal_move(board_state, row, col):
            row = int(input("Please input row"))
            col = int(input("Please input column"))

    print(row, col)
    board_state[row][col] = X_or_O
    draw_board(board_state)

next_move(board_state, player_turn, first_or_second)
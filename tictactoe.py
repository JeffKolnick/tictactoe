
def draw_board():  

    #Draws the empty board  

    print("__|___|__")
    print("__|___|__")
    print("  |   |  ")
  
draw_board()

def player_choice():

    #Asks player whether they want to go first (X's) or second (O's)
    #and returns that choice

    player_input = ""

    while player_input not in ['X', 'O']:
        player_input = input("Would you like to go first (X) or second (O)?: ")
        
    return player_input

first_or_second = player_choice()           #Tracks if player is X's or O's
board_state = [[' '] * 3 for _ in range(3)] #Track board state, initialized empty

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

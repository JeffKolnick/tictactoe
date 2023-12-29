import copy
import random
import logging

board_state = [['_'] * 3 for _ in range(3)] # Track board state, initialized empty
X_or_O = 'X'                                # Track whose turn it is; X is always first
move_made = [False]                         # Track if Computer move is made so it won't make multiple
first_or_second = ""                        # Track whether player is first (X) or second (O)
allowed_symbols = {'_', 'X', 'O'}           # Dictionary for error-handling in board_state
allowed_choices = {'X', 'O'}                # Dictionary for error-handling in symbol selection
logging.basicConfig(level = logging.INFO)

def correct_board_state(board_state):
    """
    Helper function to ensure passed board_states are valid

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols

    Returns:
    - None

    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols    
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    if not isinstance(board_state, list) or len(board_state) != 3 or any(len(row) != 3 for row in board_state):
        raise ValueError("Invalid board_state. Must be 3x3 matrix.")
    
    if any(symbol not in allowed_symbols for row in board_state for symbol in row):
        raise ValueError("Unexpected symbols in board_state in three_in_a_row(). Must be ('_', 'X' or 'O').")

def draw_board(board_state):  
    """
    Draws the current state of the board  

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols

    Returns:
    - None

    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols
    - IndexError: For potential index and out of bounds errors
    - TypeError: For potential type errors, such as a non-string
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    correct_board_state(board_state)

    try:
        # Drawing board
        print("_{}_|_{}_|_{}_".format(board_state[0][0], board_state[0][1], board_state[0][2]))
        print("_{}_|_{}_|_{}_".format(board_state[1][0], board_state[1][1], board_state[1][2]))
        print(" {} | {} | {} ".format(' ' if board_state[2][0] == '_' else board_state[2][0],\
                                    ' ' if board_state[2][1] == '_' else board_state[2][1],\
                                    ' ' if board_state[2][2] == '_' else board_state[2][2]))
        
    except(IndexError, TypeError):
        raise IndexError("Index or out of bounds error in board_state in draw_board()")
 
def player_choice():

    """
    Asks player whether they want to go first (X's) or second (O's)
    and returns that choice

    Parameters:
    - None

    Returns:
    - 'X' or 'O' based on the player's input
    """

    while True:
        player_input = input("Would you like to go first (X) or second (O)?: ").strip().upper() # Allowances for superfluous spaces and lowercase inputs
        
        if player_input in allowed_choices:
            return player_input
        else:
            print("You must select 'X' or 'O'.")

def three_in_a_row(board_state, X_or_O):

    """
    Checks each row, column and diagonal for three of the same symbol,
    which is the win condition and returns True if so

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols
    - X_or_O (string): This is the symbol which is being checked for winning states

    Returns:
    - Boolean value indicating if the given symbol has three spaces in a row
    
    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols
    - IndexError: For potential index and out of bounds errors
    - TypeError: For potential type errors, such as a non-string
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    correct_board_state(board_state)

    try:
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
    
    except(IndexError, TypeError):
        raise IndexError("Index or out of bounds error in board_state in draw_board()")
    
    return False

def is_legal_move(board_state, row, col):

    """
    Determines if move is legal, based on whether an empty square has been chosen

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols
    - row (int): The selected row
    - col (int): The selected column

    Returns:
    - Boolean value indicating if the given row and column correspond to an empty square

    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols
    - IndexError: For potential index and out of bounds errors
    - TypeError: For potential type errors, such as a non-string
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    correct_board_state(board_state)

    return -1 < row < 3 and -1 < col < 3 and board_state[row][col] == '_'

def switch_turn(X_or_O):

    """
    Returns the other player's symbol

    Parameters:
    - X_or_O (string): This is the symbol which is being switched

    Return:
    - String indicating the symbol which is not passed 

    Raises:
    - ValueError: If X_or_O is not a valid symbol
    """
    # Ensure valid symbol      
    if X_or_O not in allowed_symbols:
        raise ValueError("Unexpected symbols in board_state in three_in_a_row(). Must be ('_', 'X' or 'O').")
                         
    return 'O' if X_or_O == 'X' else 'X'
    
def collect_legal_moves(board_state):

    """
    Creates and returns array for the computer to be able to evaluate and choose moves

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols

    Returns:
    - legal_moves (list): 1D array which tracks lists the moves which are still allowed

    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols
    - IndexError: For potential index and out of bounds errors
    - TypeError: For potential type errors, such as a non-string
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    correct_board_state(board_state)

    legal_moves = []         # Determine remaining legal moves to see if there are game
    for row in range(3):     # ending moves and react accordingly
        for col in range(3):
            try:
                if is_legal_move(board_state, row ,col):
                    legal_moves.append([row, col])
            except ValueError as e:
                logging.error(f"Error: {e}")

    return legal_moves
        
def find_win(board_state, legal_moves, X_or_O, move_made):

    """
    Finds and plays winning move for computer if available

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols
    - legal_moves (list): 1D array which tracks the moves which are still allowed
    - X_or_O (string): This is the symbol which the computer is playing
    - move_made (boolean): Prevents computer from making multiple moves

    Return:
    - Boolean to end game if winning move is found and made
   
    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols    
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    correct_board_state(board_state)

    if move_made[0]:                                       # Don't play if move already made
        return 
    
    for move in legal_moves:
        temp_board_state = copy.deepcopy(board_state)   # Create temporary board_state to check for potential
        temp_board_state[move[0]][move[1]] = X_or_O     # winning moves for computer and make them
        try:
            if three_in_a_row(temp_board_state, X_or_O):                  
                board_state[move[0]][move[1]] = X_or_O 
                move_made[0] = True
                return False
        except Exception as e:
            logging.error(f"Error: {e}")
        
def find_block(board_state, legal_moves, X_or_O, move_made):

    """
    Finds and plays blocking move for computer if necessary

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols
    - legal_moves (list): 1D array which tracks lists the moves which are still allowed
    - X_or_O (string): This is the symbol which the computer is playing
    - move_made (boolean): Prevents computer from making multiple moves

    Return:
    - Function to switch player if potential winning move is found and blocked
    
    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols    
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    correct_board_state(board_state)

    if move_made[0]:                                        # Don't play if move already made
        return 

    for move in legal_moves:
        temp_board_state = copy.deepcopy(board_state)       # Create temporary board_state to check for potential winning moves
        temp_X_or_O = 'O' if X_or_O == 'X' else 'X'         # Envision board states with human's symbol played
        temp_board_state[move[0]][move[1]] = temp_X_or_O    
        try:
            if three_in_a_row(temp_board_state, temp_X_or_O):
                board_state[move[0]][move[1]] = X_or_O
                move_made[0] = True
                return switch_turn(X_or_O)
        except Exception as e:
            logging.error(f"Error: {e}")

def find_corner(board_state, legal_moves, X_or_O, move_made):

    """
    Corner squares are the best position if the centre is occupied
    and no winning move exists for either player

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols
    - legal_moves (list): 1D array which tracks lists the moves which are still allowed
    - X_or_O (string): This is the symbol which the computer is playing
    - move_made (boolean): Prevents computer from making multiple moves

    Return:
    - Function to switch player if valid corner move is found and made
    
    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols    
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    correct_board_state(board_state)

    if move_made[0]:                                # Don't play if move already made
        return 

    corner_moves = [(0,0), (0,2), (2,0), (2,2)]     # Define all four corners
    legal_corner_moves = []                         # Find and collect
    for move in legal_moves:                        # available corner moves
        if tuple(move) in corner_moves:                    
            legal_corner_moves.append(move)
    
    if legal_corner_moves:                                  # Play random corner if there
        random_corner = random.choice(legal_corner_moves)   # are any
        board_state[random_corner[0]][random_corner[1]] = X_or_O
        move_made[0] = True
        return switch_turn(X_or_O)

def find_side(board_state, legal_moves, X_or_O, move_made):

    """
    Side squares are the only position if the centre is occupied,
    no winning move exists for either player and corners are occupied

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols
    - legal_moves (list): 1D array which tracks lists the moves which are still allowed
    - X_or_O (string): This is the symbol which the computer is playing
    - move_made (boolean): Prevents computer from making multiple moves

    Return:
    - Function to switch player if valid side move is found and made
    
    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols    
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    correct_board_state(board_state)

    if move_made[0]:                                # Don't play if move already made
        return 
    
    side_moves = [(0,1), (1,0), (1,2), (2,1)]       # Define all four sides
    legal_side_moves = []                           # Find and collect
    for move in legal_moves:                        # available corner moves
        if tuple(move) in side_moves:             
            legal_side_moves.append(move)
    
    if legal_side_moves:                                # Play random side if there
        random_side = random.choice(legal_side_moves)   # are any
        board_state[random_side[0]][random_side[1]] = X_or_O
        move_made[0] = True
        return switch_turn(X_or_O)
    
def next_move(board_state, X_or_O, first_or_second, move_made):

    """
    Main game driver   

    Parameters:
    - board_state (list): 2D array which tracks empty squares and squares with symbols
    - X_or_O (string): This is the symbol which the current player is playing
    - first_or_second (string): Track whether player is first (X) or second (O)
    - move_made (boolean): Prevents computer from making multiple moves

    Return:
    - X_or_O (string): Symbol of the next player. If this value is False it will end the program
    
    Raises:
    - ValueError: If board_state is not a 3x3 matrix or has unexpected symbols    
    """

    # Ensure board_state is 3x3 matrix with valid symbols
    correct_board_state(board_state)

    draw_board(board_state)
    legal_moves = collect_legal_moves(board_state)  # Determine remaining legal moves            
    if not legal_moves:                             # and end game if there are none
        print("Drawn game")
        return False
    
    if first_or_second == X_or_O:   # Ask player for their move if it's their turn
        while True:
            coords = input("Please input row (1-3) and column (1-3) (eg 1 3): ").strip().split()
            
            if len(coords) == 2 and coords[0].isdigit() and coords[1].isdigit(): 
                row, col = map(int, coords)
                row -= 1
                col -= 1
            
                if is_legal_move(board_state, row, col):
                    board_state[row][col] = X_or_O
                    break
                else:
                    print("That is not an available square.")

            else:
                print("Please enter two integers between 1 and 3 separated by a space.")

    else:
        if board_state[1][1] == '_':    # If the centre is not taken, taking it is the best move
            board_state[1][1] = X_or_O
        
        else:  
            move_made[0] = False                           # Track if Computer move is made so it won't make multiple
          
            find_win(board_state, legal_moves, X_or_O, move_made)       # Check if computer can win
            find_block(board_state, legal_moves, X_or_O, move_made)     # Check if human can win
            find_corner(board_state, legal_moves, X_or_O, move_made)    # Check if corner space is available
            find_side(board_state, legal_moves, X_or_O, move_made)      # Check if side space is available
   
    if three_in_a_row(board_state, X_or_O):              # Check if anyone wins
        print("{} wins!".format(X_or_O))
        draw_board(board_state)
        return False

    return switch_turn(X_or_O)

# Game loop
if __name__ == '__main__':
    first_or_second = player_choice()           #Tracks if player is X's or O's
    while True:
        X_or_O = next_move(board_state, X_or_O, first_or_second, move_made)
        if not X_or_O:
            break

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

first_or_second = player_choice()


from os import system, name 

board = [None] * 9          # Create an empty board
players = ['X','O']         # Symbols for the players
who = 0                     # Starting player (players[who])
over = False                # Indicate if the game is over
outcome = "It's a draw"     # Game is a draw until proven otherwise

# Winning combinations
COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],    #rows
    [0,3,6],[1,4,7],[2,5,8],    #cols
    [0,4,8],[6,4,2]             #diagonals
]

def clear(): 
    """
    https://www.geeksforgeeks.org/clear-screen-python/
    """

    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def display(board):
    """
    Prettify the TicTacToe board for display in terminal
    """
    b = list(board)
    for i,v in enumerate(b):
        if v == None:
            b[i] = " "

    print("+-----+-----+-----+")
    print("| ",b[0]," | ",b[1]," | ",b[2]," |")
    print("+-----+-----+-----+")
    print("| ",b[3]," | ",b[4]," | ",b[5]," |")
    print("+-----+-----+-----+")
    print("| ",b[6]," | ",b[7]," | ",b[8]," |")
    print("+-----+-----+-----+")

def freecells(board):
    """
    Returns the list of valid inputs to present to the user (free cells)
    """
    cells = []
    for i,v in enumerate(board):
        if v == None:
            cells.append(i+1)
    return cells

# Displays the HOW-TO
rule_board = [1,2,3,4,5,6,7,8,9]
display(rule_board)
print("When it's your turn, type in the number of the cell you want to play then press [Enter].")

# MAIN GAME LOOP
while not over:
    display(board)
    print()

    # Prompt the player to play
    valid = False
    while not valid:
        #Fool proof input
        print("Valid choices are ", freecells(board))
        cell = input("Player " + players[who] +", enter where you want to play:")
        if cell.isdigit():
            if int(cell) in freecells(board):
                cell = int(cell)
                valid = True


    # Play in that cell (-1 to match the cell index)
    board[cell - 1] =  players[who]

    # Is the board full? (no more empty cell)
    if len(list(filter(lambda x: x is  None, board))) == 0:
        over = True

    # Has the player ticked all cells of any winning combination?
    for combo in COMBOS:
        if all(list(map(lambda cell: board[cell] == players[who], combo))):
            outcome = players[who] + " wins!"
            over = True

    # Move to the next player
    who = (who + 1) % len(players)
    clear()

# Game is over, display the outcome and final board
display(board)
print()
print(outcome)


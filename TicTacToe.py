
board = [None] * 9          # Create an empty board
PLAYERS = ['X','O']         # Symbols for the players
who = 0                     # Starting player (PLAYERS[who])
over = False                # Indicate if the game is over
outcome = "It's a draw"     # Game is a draw until proven otherwise

# Winning combinations
COMBOS = [
    [0,1,2],[3,4,5],[6,7,8],    #rows
    [0,3,6],[1,4,7],[2,5,8],    #cols
    [0,4,8],[6,4,2]             #diagonals
]

# Just to make it pretty on the screen
def display(board):
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

# Displays the HOW-TO
rule_board = [1,2,3,4,5,6,7,8,9]
display(rule_board)
print("When it's your turn, type in the number of the cell you want to play then press [Enter].")

# MAIN GAME LOOP
while not over:
    display(board)
    print()

    # Prompt the player to play
    cell = int(input("Player " + PLAYERS[who] +", enter where you want to play:"))

    # -1 to match the cell index
    board[cell - 1] =  PLAYERS[who]

    # Is the board full? (no more empty cell)
    if len(list(filter(lambda x: x is  None, board))) == 0:
        over = True

    # Has the player ticked all cells of any winning combination?
    for combo in COMBOS:
        if all(list(map(lambda cell: board[cell] == PLAYERS[who], combo))):
            outcome = PLAYERS[who] + " wins!"
            over = True

    # Move to the next player
    who = (who + 1) % len(PLAYERS)

# Game is over, display the outcome and final board
display(board)
print()
print(outcome)


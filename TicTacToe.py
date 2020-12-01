# Create the board
board = [None] * 9

# Symbols for the players
players = ['X','O']

# Starting player
who = 0

# Indicate if the game is over
over = False

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

# Display the how-to
rule_board = [1,2,3,4,5,6,7,8,9]
display(rule_board)
print("When it's your turn, type in the number of the cell you want to play then press [Enter].")

while not over:
    display(board)

    # Prompt the player to play
    cell = int(input("Player " + players[who] +", enter where you want to play:"))

    # -1 to match the cell index
    board[cell - 1] =  players[who]

    # Check if over

    # Is the board full?
    if len(list(filter(lambda x: x is  None, board))) == 0:
        over = True

    # Is there a winner?
    p = players[who]
    if  (
        all([board[0] == p, board[1] == p, board[2] == p]) or   #row 1
        all([board[3] == p, board[4] == p, board[5] == p]) or   #row 2
        all([board[6] == p, board[7] == p, board[8] == p]) or   #row 3
        all([board[0] == p, board[3] == p, board[6] == p]) or   #col 1
        all([board[1] == p, board[4] == p, board[7] == p]) or   #col 2
        all([board[2] == p, board[5] == p, board[8] == p]) or   #col 3
        all([board[0] == p, board[4] == p, board[8] == p]) or   #diag 1
        all([board[6] == p, board[4] == p, board[2] == p])      #diad 2
    ):
        # A player has a wiining line, game is over
        over = True

    # Move to the next player
    who = (who + 1) % len(players)

# Game is over, display final board
display(board)


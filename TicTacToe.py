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

class Player :
    def __init__(self, name, mark, ai = False):
        self.name = name
        self.mark = mark
        self.ai = ai
        self.score = 0

    def wins(self):
        self.score =+ 1

player = [None] * 2
player[0] = Player("Michael","X")
player[1] = Player("WOPR","O", True) # Easter egg https://www.youtube.com/watch?v=fFJVspLBYCI

def clear(): 
    """Clear the terminal"""
    #https://www.geeksforgeeks.org/clear-screen-python/
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

def getcellfromplayer(board, player):
    """
    Asks the user to make a move
        Parameters:
            board (list):   A list of cells that represents 
                            the TicTacToe board
            player (str):   A player object 

        Returns:
            cell (integer): A valid cell number where the 
                            player can put his mark
    """
    valid = False
    while not valid:
        #Valid input consists of free cells only
        print("Valid choices are", freecells(board))
        cell = input(player.name +", select where you want to play:")
        if cell.isdigit():
            if int(cell) in freecells(board):
                cell = int(cell)
                valid = True
    return cell

def getcellfromAI(board, player,opponent):
    """
    Asks the user to make a move
        Parameters:
            board (list):   A list of cells that represents 
                            the TicTacToe board
            player (obj):   A player object
            opponent (obj): A player object

        Returns:
            cell (integer): A valid cell number where the 
                            player can put his mark
    """
    
    # HillClimb algorithm
    preferred_cell = None
    best_score_so_far = 0
    for c in freecells(board):   
        me = 0
        him = 0
        score = 0
        best_so_far = 0
        for combo in COMBOS:
            if c-1 in combo:
                #ignore combos that do not include said cell

                # Heuristics calculation below
                me = len(list(filter(lambda x: board[x] == player.mark, combo)))
                him = len(list(filter(lambda x: board[x] == opponent.mark, combo)))
                if me == 2:
                    score += 1024
                elif him == 2:
                    score += 512
                elif me == 1:
                    score += 256
                elif him == 1:
                    score += 128
                else:
                    score += 64

        # Flag the cell as preferred if it gets the player closer to victory
        if score > best_score_so_far:
            best_score_so_far = score
            preferred_cell = c

    return preferred_cell

# Displays the HOW-TO
clear()
rule_board = [1,2,3,4,5,6,7,8,9]
display(rule_board)
print("When it's your turn, type in the number of the cell you want to play then press [Enter].")
input("Press [Enter] to start.")
clear()

# MAIN GAME LOOP
while not over:
    display(board)
    print()

    # Prompt the player to play
    if player[who].ai:
        cell = getcellfromAI(board, player[who], player[(who + 1) % len(players)])
    else:
        cell = getcellfromplayer(board, player[who])

    # Play in that cell (-1 to match the cell index)
    board[cell - 1] =  player[who].mark

    # Is the board full? (no more empty cell)
    if len(list(filter(lambda x: x is  None, board))) == 0:
        over = True

    # Has the player ticked all cells of any winning combination?
    for combo in COMBOS:
        if all(list(map(lambda cell: board[cell] == player[who].mark, combo))):
            outcome = player[who].name + " wins the match!"
            player[who].wins()
            over = True

    # Move to the next player and clear the screen
    who = (who + 1) % len(players)
    clear()

# Game is over, display the outcome and final board
display(board)
print(outcome)
print(f"{player[0].name}:{player[0].score}")
print(f"{player[1].name}:{player[1].score}")


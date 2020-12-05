from os import system, name 

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
player[0] = Player("Michael","X", False)
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
            cells.append(i)
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
        print("Valid choices are", list(map(lambda x : x+1, freecells(board))))
        cell = input(player.name +", select where you want to play:")
        if cell.isdigit():
            if int(cell)-1 in freecells(board):
                cell = int(cell)
                valid = True
    return cell-1

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
    
    scores = []
    strat_1 = []
    strat_2 = []
    strat_3 = []
    strat_41 = []
    strat_42 = []
    strat_5 = []
    strat_6 = []
    strat_7 = []
    strat_8 = []

    # Evaluate each possible next move against the optimal strategy
    for c in freecells(board):   
        me = 0
        him = 0
        combo_stats = []

        # For line, row, diag that contains the evaluated move
        for combo in COMBOS:
            if c in combo:
                me = len(list(filter(lambda x: board[x] == player.mark, combo)))
                him = len(list(filter(lambda x: board[x] == opponent.mark, combo)))
                combo_stats.append((me,him))

        
        # Heuristics calculation below are based on the best strategy
        # See https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy

        # 1. WIN
        # If combo consists of 2 of the player's mark then fill the space
        if (2,0) in combo_stats: 
            strat_1.append(c)
            continue

        # 2. BLOCK
        # If combo consists of 2 of the opponent's mark then fill the space
        if (0,2) in combo_stats: 
            strat_2.append(c)
            continue         

        # 3. FORK
        # Create a double opportunity
        if combo_stats.count((1,0)) == 2: 
            strat_3.append(c)
            continue

        # 4. BLOCK FORK
        # Prevent a double opportunity
        if combo_stats.count((0,1)) == 2: 
            strat_42.append(c)
            if len(strat_42) >1:
                # find a valid move in a combo with (me/him) = (1,0) 
                # that contains none of the values of strat_42[]
                for combo in COMBOS:
                    if (    strat_42[0] not in combo and 
                            strat_42[1] not in combo and
                            len(list(filter(lambda x: board[x] == player.mark, combo))) == 1 and
                            len(list(filter(lambda x: board[x] == opponent.mark, combo))) == 0):
                        strat_41.extend(list(filter(lambda x: board[x] == None, combo)))
                
            continue

        # 5. CENTRE
        if board[4] == None: 
            strat_5.append(4)
            continue

        # 6. OPPOSITE CORNER
        if  ((c == 0 and board[9] == opponent.mark) or 
            (c == 9 and board[0] == opponent.mark) or 
            (c == 3 and board[7] == opponent.mark) or 
            (c == 7 and board[3] == opponent.mark)): 
            strat_6.append(c)
            continue
        
        # 7. EMPTY CORNER
        if c in (0, 3, 7, 9): 
            strat_7.append(c)
            continue
            
        # 8. EMPTY EDGE
        if c in (1, 4, 6, 8): 
            strat_8.append(c)
            continue

    scores.extend(strat_1)
    scores.extend(strat_2)
    scores.extend(strat_3)
    scores.extend(strat_41)
    scores.extend(strat_42)
    scores.extend(strat_5)
    scores.extend(strat_6)
    scores.extend(strat_7)
    scores.extend(strat_8)

    print(player.name, "played in ",scores[0]+1)
    return scores[0]
            




# Displays the HOW-TO
clear()
rule_board = [1,2,3,4,5,6,7,8,9]
display(rule_board)
print("When it's your turn, type in the number of the cell you want to play then press [Enter].")
input("Press [Enter] to start.")
clear()


# Prematch setup
board = [None] * 9  # Create an empty board
over = False        # Is the game over?
who = 0             # Which player starts?
outcome = "Draw"

# MATCH LOOP
while not over:
    display(board)
    print()

    # Prompt the player to play
    if player[who].ai:
        cell = getcellfromAI(board, player[who], player[(who + 1) % len(player)])
    else:
        cell = getcellfromplayer(board, player[who])

    # Play in that cell
    board[cell] =  player[who].mark

    # Is the board full? (no more empty cell)
    if board.count(None) == 0:
        over = True

    # Has the player ticked all cells of any winning combination?
    for combo in COMBOS:
        if all(list(map(lambda cell: board[cell] == player[who].mark, combo))):
            outcome = player[who].name + " wins the match!"
            player[who].wins()
            over = True

    # Move to the next player and clear the screen
    who = (who + 1) % len(player)
    #clear()

# Match is over, display the outcome and final board
display(board)
print(outcome)
print(f"{player[0].name}:{player[0].score}")
print(f"{player[1].name}:{player[1].score}")


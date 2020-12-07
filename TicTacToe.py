from os import system, name 

class Player():
    def __init__(self, name, mark, ai = False):
        self.name = name
        self.mark = mark
        self.ai = ai
        self.score = 0

    def wins(self):
        self.score =+ 1

class TicTacToe():
    def __init__(self):
        self.board = [None]*9
        self.history = []
        self.outcome = None
        self.over = False
        self.COMBOS = [
            [0,1,2],[3,4,5],[6,7,8],    #rows
            [0,3,6],[1,4,7],[2,5,8],    #cols
            [0,4,8],[6,4,2]             #diagonals
        ]

    def display(self):
        """
        Prettify the TicTacToe board for display in terminal
        """
        b = list(self.board)
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

    def freecells(self):
        """
        Returns the list of valid inputs to present to the user (free cells)
        """
        cells = []
        for i,v in enumerate(self.board):
            if v == None:
                cells.append(i)
        return cells

    def is_winner(self, player):
        # Has the player ticked all cells of any winning combination?
        for combo in self.COMBOS:
            if all(list(map(lambda cell: self.board[cell] == player.mark, combo))):
                return True
        return False

    def play(self, player, cell):
        self.board[cell] = player.mark
        self.history.append((cell,player))
        
        # Finish the game if no move can be made
        if len(self.freecells()) == 0:
            self.over = True

        #Declare a winner if any
        if self.is_winner(player):
            self.outcome = player.name
            self.over = True

def clear(): 
    """Clear the terminal"""
    #https://www.geeksforgeeks.org/clear-screen-python/
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def getcellfromplayer(game, player):
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
        print("Valid choices are", list(map(lambda x : x+1, game.freecells())))
        cell = input(player.name +", select where you want to play:")
        if cell.isdigit():
            if int(cell)-1 in game.freecells():
                cell = int(cell)
                valid = True
    return cell-1

def getcellfromAI(game, player,opponent):
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
    for move in game.freecells():   
        me = 0
        him = 0
        combo_stats = []

        # For line, row, diag that contains the evaluated move
        for combo in game.COMBOS:
            if move in combo:
                # assess the the number of marks each player has 
                me = len(list(filter(lambda x: game.board[x] == player.mark, combo)))
                him = len(list(filter(lambda x: game.board[x] == opponent.mark, combo)))
                combo_stats.append((me,him))

        
        # Heuristics calculation below are based on the best strategy
        # See https://en.wikipedia.org/wiki/Tic-tac-toe#Strategy

        # 1. WIN
        # If combo consists of 2 of the player's mark then fill the space
        if (2,0) in combo_stats: 
            strat_1.append(move)
            continue

        # 2. BLOCK
        # If combo consists of 2 of the opponent's mark then fill the space
        if (0,2) in combo_stats: 
            strat_2.append(move)
            continue         

        # 3. FORK
        # Create a double opportunity
        if combo_stats.count((1,0)) == 2: 
            strat_3.append(move)
            continue

        # 4. BLOCK FORK
        # Prevent a double opportunity
        if combo_stats.count((0,1)) == 2: 
            strat_42.append(move)
            if len(strat_42) >1:
                # find a valid move in a combo with (me/him) = (1,0) 
                # that contains none of the values of strat_42[]
                for combo in game.COMBOS:
                    if (    strat_42[0] not in combo and 
                            strat_42[1] not in combo and
                            len(list(filter(lambda x: game.board[x] == player.mark, combo))) == 1 and
                            len(list(filter(lambda x: game.board[x] == opponent.mark, combo))) == 0):
                        strat_41.extend(list(filter(lambda x: game.board[x] == None, combo)))
                
            continue

        # 5. CENTRE
        if game.board[4] == None: 
            strat_5.append(4)
            continue

        # 6. OPPOSITE CORNER
        if  ((move == 0 and game.board[9] == opponent.mark) or 
            ( move == 9 and game.board[0] == opponent.mark) or 
            (move == 3 and game.board[7] == opponent.mark) or 
            (move == 7 and game.board[3] == opponent.mark)): 
            strat_6.append(move)
            continue
        
        # 7. EMPTY CORNER
        if move in (0, 3, 7, 9): 
            strat_7.append(move)
            continue
            
        # 8. EMPTY EDGE
        if move in (1, 4, 6, 8): 
            strat_8.append(move)
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

    return scores[0]
            
# Prematch setup
player = [None]*2
player[0] = Player("Michael","X", False)
player[1] = Player("WOPR","O", True) # Easter egg https://www.youtube.com/watch?v=fFJVspLBYCI
who = 0             # Which player starts?
game = TicTacToe()

# MATCH LOOP
while not game.over:
    game.display()
    print()

    # Prompt the player to play
    if player[who].ai:
        cell = getcellfromAI(game, player[who], player[(who + 1) % len(player)])
    else:
        cell = getcellfromplayer(game, player[who])

    # Play in that cell
    game.play(player[who], cell)
    
    # Move to the next player and clear the screen
    who = (who + 1) % len(player)
    clear()
    
# Match is over, display the final board and the outcome
game.display()
print("Winner:",game.outcome)

from os import system, name

def minimax(node, depth, maxPlayer, maxTurn):
    if node.is_winner(maxPlayer):
        return 1 #Maximized player wins
    elif node.is_winner(maxPlayer.next()):
        return -1 #Minimized player wins
    # There is no winner and explored as far as desired, it's a draw
    elif depth == 0 :
        return 0

    scores = []

    # Pretend to play (recusively)
    for cell in node.freecells():
        # Who plays?
        if maxTurn:
            node.play(maxPlayer,cell)
        else:
            node.play(maxPlayer.next(),cell)

        #Keep track of the score for that move
        scores.append(minimax(node, depth - 1, maxPlayer, not maxTurn))

        # Rollback
        node.cancel()

    if maxTurn:
        return max(scores)
    else:
        return min(scores) 
        
class Player():
    instances = []
    def __init__(self, name, mark, ai = False):
        self.name = name
        self.mark = mark
        self.ai = ai
        self.instances.append(self)
        self.id = len(self.instances)-1

    def next(self): # Returns the next player object
        next = self.instances[(self.id + 1) % len(self.instances)]
        return next

class TicTacToe():
    def __init__(self, board = [None]*9):
        self.board = board
        self.history = []
        self.outcome = None
        self.over = False
        self.COMBOS = [
            [0,1,2],[3,4,5],[6,7,8],    #rows
            [0,3,6],[1,4,7],[2,5,8],    #cols
            [0,4,8],[6,4,2]             #diagonals
        ]
        self.children = []

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
                return player.name
        return None

    def play(self, player, cell):

        self.board[cell] = player.mark
        self.history.append(cell)
        
        # Finish the game if no move can be made
        if len(self.freecells()) == 0:
            self.over = True

        #Declare a winner if any
        if self.is_winner(player):
            self.outcome = player.name
            self.over = True

    def cancel(self):
        cell = self.history.pop()
        self.board[cell] = None

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
            game:   An instance of the TicTacToe object
            player:   A player object 

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
     
# Prematch setup
player = [None]*2
player[0] = Player("Michael","X", False)
player[1] = Player("WOPR","O", True) # Easter egg https://www.youtube.com/watch?v=fFJVspLBYCI
who = 0             # Which player starts?
game = TicTacToe()


# MATCH LOOP
while not game.over:

    # clear the screen
    clear()

    # display the board
    game.display()
    
    # Prompt the player to play
    if player[who].ai:
        scores = []
        for c in game.freecells():
            #create a new to break the reference to game.board
            node = TicTacToe(game.board)

            #pretend to play a cell to get a score
            node.play(player[who],c)
            scores.append(minimax(node, len(game.freecells()), player[who],False))
            node.cancel()
        
        #get the cell with the best score
        cell = game.freecells()[scores.index(max(scores))]

    else:
        cell = getcellfromplayer(game, player[who])

    # Play that cell
    game.play(player[who], cell)
    
    # Move to the next player
    who = (who + 1) % len(player)
    
# Match is over, display the final board and the outcome
game.display()
print("Winner:",game.outcome)

"""
@author:    Mitchell Sulz-Martin
@date:      02/19/18

This script is the set up for the game and players.
It will take the input from a Human player or call the alphabeta script
    to get the input for a Computer player.
"""
import numpy as np
from alpha_beta import AlphaBeta

class Connectfour:
    """A game of Connect4"""
    
    winner = None
    turn = None
    rounds = None
    over = None
    players = [None, None]
    gb = None

    def __init__(self):
       self.gb = np.full((6,7), " ") 
       self.chips = [chr(9679), chr(9675)] # [9679 -> ● , 9675 -> ○]
       self.rounds = 1
       self.over = False
      
    def new_player(self, chips):
        """Creates two new players"""
        
        name = input("Hello player one! What is your name? ")
        playerone = Player(name, chips[0])
        
        print("Alright", name, "would you like to play against the computer?")
        choice = str(input("Type 'Y' or 'N': "))
        if choice.lower() == "n" or choice == "no":
            print("Hello player two!")
            name = input("What is your name?")
            playertwo = Player(name, chips[1])
        else:
            print("\nYour opponent is Al Betaman", end="")
            playertwo = AIplayer("Al Betaman", chips[1])
            
            
        return [playerone, playertwo]
    
    def new_game(self):
        """ Starts a new game of Connect4 """
        self.players = self.new_player(self.chips)
        self.turn = self.players[0]
        self.print_gameboard()
        
        while not self.over:
            self.next_move()
        self.gameover()
        return 
    
    def next_move(self):
        """ Collects and verifies the current players input
                then places there corresponding game chip on the board """
        player = self.turn
        if self.rounds > 42:
            self.over = True
            return
        
        move = player.move(self.gb)
        for i in range(0, 6):
            if self.gb[5-i][move] == " ":
                self.gb[5-i][move] = player.chip
                player.moves_played.add((5-i, move))
                self.changeturn()
                self.checkwin((5-i, move), player)
                self.print_gameboard()
                return
            
        print("Invalid move... That column is full.")
        self.next_move()
        return
    
    def changeturn(self):
        """ Changes the turn to the opposing player """
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]
        self.rounds+=1
        return
    
    def gameover(self):
        """ Prints the results of a game which has ended """
        if self.winner is not None:
            print("\n"*30, self.winner.name, "has won the game in", self.rounds, "rounds!")
        else:
            print("\n"*30, "The game has ended in a tie!")
        self.print_gameboard()
        return 
    
    def print_gameboard(self):
        """ Prints the current state of the game board """
        if not self.over:
            print("\n"*30 +
                  "------------------------------------------------------"+
                  "\nRound:", self.rounds, "\n", self.turn.name, "it is your turn to play the",
                  self.turn.chip, "chip.\n" +
                  "------------------------------------------------------")
        border = "\n|===|===|===|===|===|===|===|\n"
        inner = " |\n|---|---|---|---|---|---|---|\n| "
        print(border + '| ' + inner.join([' | '.join([i for i in row]) 
                            for row in self.gb]) + ' |' + border +
                "| 1 | 2 | 3 | 4 | 5 | 6 | 7 |")
        return
    
    def checkwin(self, x, player):
        """ Checks if the current player has one the game on a given move """
        d = lambda i,j: ((i[0]-j[0]), (i[1]-j[1]))
        I = self.get_valid_neighbors(x, player)
        if len(I) == 0:
            self.over = False
            return
        else:
            while len(I) > 0:
                p = I.pop()
                D = d(x,p)
                N = set([x, p, (p[0]-D[0], p[1]-D[1])]) 
                if (x[0]+D[0], x[1]+D[1]) in player.moves_played:
                    N.add((x[0]+D[0], x[1]+D[1]))
                if player.moves_played.intersection(N) == N:
                    if len(N) >= 4:
                        self.over = True
                        self.winner = player
                        return
                    else:
                        N.add((p[0]-D[0]-D[0], p[1]-D[1]-D[1]))
                        if player.moves_played.intersection(N) == N:
                            self.over = True
                            self.winner = player
                            return
        return
    
    def get_valid_neighbors(self, move, player):
        """ Checks the surrounding 8 squares for previous plays
                made by a certain player """
        x, y = move
        N = set([(x-1, y+1), (x, y+1), (x+1, y+1), (x-1, y),
                 (x+1, y), (x-1, y-1), (x, y-1), (x+1, y-1)])
        return player.moves_played.intersection(N) 
    
class Player:
    """ A Human player in a game of Connect4 """
    name = None
    chip = None
    moves_played = None
    
    def __init__(self, name, chip):
        self.name = name
        self.chip = chip
        self.moves_played = set()
    
    def move(self, state):
        """Gathers and verifies the input for column selection """
        column = int(input("Please select a column to place your chip in: "))
        if column in range(1, 8):
            return column-1
        else:
            print("That is not a valid move!")
            self.move()

class AIplayer(Player):
    """A computer player in a game of Connect4
        Extends Player class and implements the Alpha-Beta Minimax algorithm"""
    difficulty = None
    
    def __init__(self, name, chip):
        self.name = name
        self.chip = chip
        self.difficulty = 7
        self.moves_played = set()
        
    def move(self, state):
        """ Takes the output of the Alpha-Beta Minimax algorithm and uses it
                to tell the game where to place it's chip """
        ab = AlphaBeta(state)
        move = ab.next_move(self.difficulty, state, self.chip)
        return move
    
    # **NOTE** Selecting a difficulty below 5 will not allow the algorithm
    #               enough depth to properly select a move 
    def changedifficulty(self):
        """ Changes the difficulty of an AI/computer player"""
        out = "How difficult would you like " + self.name + " to play? Type 1 - 7: "
        diff = int(input(out))
        if diff in range(1, 8):
            if diff%2 == 0:
                return int(diff)+1
            return int(diff)
        else:
            print("Sorry I dont understand..")
            self.changedifficulty()
            
            
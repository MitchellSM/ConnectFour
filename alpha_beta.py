"""
@author:    Mitchell Sulz-Martin
@date:      02/24/18

This script uses the game board (current state of the game) as input
    to the Alpha-Beta Minimax algorithm to decide the move for the 
    computer player. 
"""

import numpy as np
from random import shuffle

class AlphaBeta(object):
    """ An implementation of the Alpha-Beta Minimax algorithm used by a 
            computer player """
    board_state = None
    def __init__(self, gameboard):
        """ Put the actual game board into memory for soft copying """
        self.board_state = [i[:] for i in gameboard]
    
    def next_move(self, depth, state, currchip):
        """ Get all possible moves and evaluate them using Alpha Beta minimax """
        oppchip = chr(9675) if currchip == chr(9679) else chr(9679)
        legal = []
        alpha = -np.inf
        move = None
        for i in range(0, 7):
            if self.getlegal(i, state):
                tmp = self.move(i, state, currchip)
                legal.append((i, -self.alphabeta_search(depth-1, tmp, oppchip, -np.inf, np.inf)))
        shuffle(legal)
        for m, a in legal:
            if a >= alpha:
                alpha = a
                move = m
        return move

    def alphabeta_search(self, depth, state, currchip, alpha, beta):
        """ Implementation of the alpha beta minimax pruning algorithm """
        oppchip = chr(9675) if currchip == chr(9679) else chr(9679)
        legal = []
        
        #For the current state, get the next set of states
        for i in range(0, 7):
            if self.getlegal(i, state):
                tmp = self.move(i, state, currchip)
                legal.append(tmp)
        
        if depth == 0 or len(legal) == 0:
            return self.evaluate(state, currchip)
        
		#Max player
        if currchip == chr(9679):
            optimal = -np.inf
            for i in legal:
                optimal = max(optimal, -self.alphabeta_search(depth-1, i, oppchip, alpha, beta)) 
                if optimal >= beta:
                    return optimal
                alpha = max(alpha, optimal)
            return optimal
		#Min player
        else:
            optimal = np.inf
            for i in legal:     
                optimal = min(optimal, -self.alphabeta_search(depth-1, i, oppchip, alpha, beta))
                if optimal <= alpha:
                    return optimal
                beta = min(beta, optimal)
            return optimal
        
    def getlegal(self, col, state):
        """ Check if a move is currently legal to play
                i.e. not out of bounds """
        for i in range(0, 6):
            if state[5-i][col] == " ":
                return True
        return False
    
    def move(self, col, state, currchip):
        """ Create a soft copy of the current state and play the given move
                for a specific player """
        tmp = np.copy(state)
        for i in range(0, 6):
            if tmp[5-i][col] == " ":
                tmp[5-i][col] = currchip
                return tmp

    def evaluate(self, state, currchip):
        """ Get the previously played moves of a certain player from
                for a given state"""
        score = 0
        currentmoves = []
        for i in range(0, 6):
            for j in range(0, 7):
                if state[i][j] == currchip:
                    currentmoves.append((i, j))
        score += self.chainsize(currentmoves)
        return score
    
    def chainsize(self, moveset):
        """ Using the set of moves for a player, we can calculate how long
                of a chain each move is connected to 
                using it's set of neighbors 
                and scoring the current state based off of how many chains
                a player has and how long they are """
        d = lambda i,j: ((i[0]-j[0]), (i[1]-j[1]))
        score = 0
        played = set(moveset)   
        for x in moveset:
            I = self.get_valid_neighbors(x, played)
            while len(I) > 0:
                p = I.pop()
                D = d(x,p)
                N = set([x, p, (p[0]-D[0], p[1]-D[1]), (x[0]+D[0], x[1]+D[1]),
                             (x[0]+D[0]+D[0], x[1]+D[1]+D[1])]) 
                length = len(played.intersection(N))
                if length == 4:
                    score += 10000
                if length == 3:
                    score += 1000
                if length == 2:
                    score += 10
        return score  
       
    
    def get_valid_neighbors(self, move, moveset):
        """ Checks the surrounding 8 squares for previous plays """
        x, y = move
        N = set([(x-1, y+1), (x, y+1), (x+1, y+1), (x-1, y),
                 (x+1, y), (x-1, y-1), (x, y-1), (x+1, y-1)])
        return moveset.intersection(N) 
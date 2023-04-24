"""fonte:https://colab.research.google.com/drive/1PBS8wOLPqG0b251SjSbgMPrqpY8Jv1dC?usp=sharing#scrollTo=8GnEGyVrgRSk"""

import functools
cache = functools.lru_cache(10**6)

#from players import *

import playingStrategies
import random
from board import Board,draw_board
import multiprocessing
import time

#######################
import playerExampleRandom as playerXmodule
import playerExampleAlpha as playerOmodule
#######################


# Hadron Game
# The moves of player have the form (y,x), where y is the column number and x the row number (starting with 0)
# In the visualization, they are in the form (row, column) starting with 1.

class Game:
    """A game is similar to a problem, but it has a terminal test instead of
    a goal test, and a utility for each terminal state. To create a game,
    subclass this class and implement `actions`, `result`, `is_terminal`,
    and `utility`. You will also need to set the .initial attribute to the
    initial state; this can be done in the constructor."""

    def actions(self, state):
        """Return a collection of the allowable moves from this state."""
        raise NotImplementedError

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        raise NotImplementedError

    def is_terminal(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

    def utility(self, state, player):
        """Return the value of this final state to player."""
        raise NotImplementedError

class Hadron(Game):

    def __init__(self, height=9, width=9):
        self.height=height
        self.width=width
        self.squares = {(x, y) for x in range(width) for y in range(height)}
        self.initial = Board(height=height, width=width, to_move='X', utility=0)

    def actions(self, board):
        """Legal moves are any square not yet taken."""
        freeCells=set(self.squares)-set(board)
        ret=set()
        for b in freeCells:
            if(self.available(b, board)):
                ret.add(b)

        return ret

    def result(self, board, square):
        """Place a marker for current player on square."""
        player = board.to_move
        board = board.new({square: player}, to_move=('O' if player == 'X' else 'X'))
        win = len(self.actions(board))==0
        board.utility = (0 if not win else +1 if player == 'X' else -1)
        return board

    def utility(self, board, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return board.utility if player == 'X' else -board.utility

    def is_terminal(self, board):
        """A board is a terminal state if it is won"""
        return board.utility != 0 or len(board)==self.height*self.width

    def display(self, board):
        print(board)


    def available(self,square,board):
        i = square[0]
        j = square[1]

        count=0
        if (i > 0):
            sign=board.get((i-1,j))
            if(sign=='X'):
                count+=1
            elif (sign=='O'):
                count-=1
        if (i < self.height -1):
            sign = board.get((i + 1, j))
            if (sign == 'X'):
                count += 1
            elif (sign == 'O'):
                count -= 1
        if (j > 0):
            sign = board.get((i, j-1))
            if (sign == 'X'):
                count += 1
            elif (sign == 'O'):
                count -= 1
        if (j < self.width - 1):
            sign = board.get((i, j + 1))
            if (sign == 'X'):
                count += 1
            elif (sign == 'O'):
                count -= 1

        return count==0

# # The third argument is for debugging (it's a log of choices)
# def playerXyellow (conn,game,qX):
#     newState = game.initial
#     number_of_move = 1  # First move for X
#     while not game.is_terminal(newState):
#         (number_of_move,newState) = conn.recv()
#         # In this example, X plays randomly
#         if number_of_move == -1:
#             return
        
#         available_moves = list(game.actions(newState))
#         move = random.choice(available_moves)
#         qX.put((number_of_move,move,available_moves))
#         conn.send((number_of_move,newState,move))
#     return

# def playerOblack (conn,game,qO):
#     state = game.initial
#     newState = state
#     number_of_moveRec = 0
#     cutoff = 3  # cutoff depth for the search
#     move = None
#     while not game.is_terminal(state):
#         (number_of_moveRec,newState) = conn.recv()
#         while conn.poll():
#             (number_of_moveRec,newState) = conn.recv()
#         if number_of_moveRec == -1 :
#             return
        
#         # In this example, O plays with alphabetaSearch
#         value,move = playingStrategies.h_alphabeta_search(game,newState,playingStrategies.cutoff_depth(cutoff))
      
#         conn.send((number_of_moveRec,newState,move))
#         qO.put((number_of_moveRec,move))

#         state = newState
        
#     return



def play_game(game, playerX, playerO, verbose=False, timeout = 3):
    """Play a turn-taking game. `strategies` is a {player_name: function} dict,
    where function(state, game) is used to get the player's move."""
    state = game.initial
    number_of_move = 0
    move = (0,0)
    #number_of_movePl = 0
    while not game.is_terminal(state):
        player = state.to_move
        number_of_move += 1
        available_moves = list(game.actions(state))
        if player == 'X':
            parent_connX.send((number_of_move,state))
            if parent_connX.poll(timeout):
                (number_of_movePl, state_recv, move) = parent_connX.recv()
            else:
                move = random.choice(available_moves)
                print("Timeout, random choice for player X")
        else:
            parent_connO.send((number_of_move,state))
            if parent_connO.poll(timeout):
                (number_of_movePl, state_recv, move) = parent_connO.recv()
            else:
                move = random.choice(available_moves)
                print("Timeout, random choice for player O")

        # further check to avoid syncronization troubles
        if number_of_movePl != number_of_move:
            move = random.choice(available_moves)
            print("Different number of move, random choice for player ", player)         
         # further check to avoid wrong moves
        if move not in available_moves:
            print ("choices for ",player, available_moves, " move number", number_of_move)
            print("Wrong move", move, ", using random choice for player ", player)
            move = random.choice(available_moves)
       
        #move = strategies[player](game, state)
        state = game.result(state, move)
        if verbose:
            print('Player', player, 'move: (', move[1]+1,',',move[0]+1,')')
            print(state)
            if game.is_terminal(state):
                print ("Result for player yellow (X): ",game.utility(state,'X'))
        draw_board(state)
    
    # Send the final state to the players
    parent_connX.send((-1,state))
    parent_connO.send((-1,state))
    
    return state


#def random_player(game, state): return random.choice(list(game.actions(state)))

def player(search_algorithm):
    """A game player who uses the specified search algorithm"""
    return lambda game, state: search_algorithm(game, state)[1]


if __name__ == '__main__':
    game = Hadron()
    parent_connX, child_connX = multiprocessing.Pipe()
    parent_connO, child_connO = multiprocessing.Pipe()
    qX = multiprocessing.Queue()
    playerX = multiprocessing.Process(target=playerXmodule.playerStrategy, args=(child_connX,game,qX))
    qO = multiprocessing.Queue()
    playerO = multiprocessing.Process(target=playerOmodule.playerStrategy, args=(child_connO,game,qO))
    
    playerX.start()
    playerO.start()
    
    play_game(game, playerX, playerO, verbose=True)
    
    # print("Queue for X")
    # while not qX.empty():
    #     print(qX.get())
    # print("Queue for O",qO)
    # while not qO.empty():
    #     print(qO.get())



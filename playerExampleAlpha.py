import playingStrategies
import playingStrategies2
import playingStrategies3
#import random
import game
#from board import Board,draw_board
#import multiprocessing
#import time

# Hadron Game
# The moves of player have the form (y,x), where y is the column number and x the row number (starting with 0)
# In the visualization, they are in the form (row, column) starting with 1.

# If it receives - 1 as the number of moves, then the game is finished

def playerStrategy (conn,game,qO):
    state = game.initial
    newState = state
    number_of_moveRec = 0
    cutoff = 3  # cutoff depth for the search
    move = None
    while not game.is_terminal(state):
        (number_of_moveRec,newState) = conn.recv()
        while conn.poll():
            (number_of_moveRec,newState) = conn.recv()
        if number_of_moveRec == -1 :
            return
        
        # In this example, O plays with alphabetaSearch
        value,move = playingStrategies3.h_alphabeta_search(game,newState,playingStrategies3.cutoff_depth(cutoff))
        #move = playingStrategies2.h(game, newState)
        #value,move = playingStrategies2.h(game, newState)

        conn.send((number_of_moveRec,newState,move))
        qO.put((number_of_moveRec,move))

        state = newState
        
    return


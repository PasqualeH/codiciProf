#from collections import namedtuple, Counter, defaultdict
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt


import functools
cache = functools.lru_cache(10**6)

# A board encodes a state of the game, in Hadron and similar board games
class Board(defaultdict):
    """A board has the player to move, a cached utility value,
    and a dict of {(x, y): player} entries, where player is 'X' or 'O'."""
    empty = '.'
    off = '#'

    def __init__(self, width=8, height=8, to_move=None, **kwds):
        self.__dict__.update(width=width, height=height, to_move=to_move, **kwds)
        self.utility = 0 #todo check why this was not present before

    def new(self, changes: dict, **kwds) -> 'Board':
        "Given a dict of {(x, y): contents} changes, return a new Board with the changes."
        board = Board(width=self.width, height=self.height, **kwds)
        board.update(self)
        board.update(changes)
        return board

    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.empty
        else:
            return self.off

    def __hash__(self):
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)

    def __repr__(self):
        def row(y): return ' '.join(self[x, y] for x in range(self.width))

        return '\n'.join(map(row, range(self.height))) + '\n'
    
    
def draw_board(board):
    # create a new figure
    fig, ax = plt.subplots()

    # draw the board background
    ax.set_facecolor((0.5, 0.5, 1))

    # draw the squares on the board
    for row in range(board.height-1,board.height//2-1,-1):
        for col in range(board.width-1,-1,-1):
            rect = plt.Rectangle((col, row), 1, 1, facecolor=(0, 0, 1), edgecolor=(0, 0, 0))
            ax.add_patch(rect)

            # draw the player's pieces on the board
            if board[col,row] == 'X':
                #debug
                #print("col",col,"row",row,"board.height-1",board.height - 1)
                circle = plt.Circle((col + 0.5, board.height - 1 - row + 0.5), 0.4, color='y')
                ax.add_patch(circle)
            elif board[col,row] == 'O':
                circle = plt.Circle((col + 0.5, board.height - 1 - row + 0.5), 0.4, color='k')
                ax.add_patch(circle)
                
    # draw the squares on the board
    for row in range(board.height):
        for col in range(board.width):
            rect = plt.Rectangle((col, board.height - 1 - row), 1, 1, facecolor=(0, 0, 1), edgecolor=(0, 0, 0))
            ax.add_patch(rect)

            # draw the player's pieces on the board
            if board[col,row] == 'X':
                #debug
                #print("col",col,"row",row,"board.height-1",board.height - 1)
                circle = plt.Circle((col + 0.5, board.height - 1 - row + 0.5), 0.4, color='y')
                ax.add_patch(circle)
            elif board[col,row] == 'O':
                circle = plt.Circle((col + 0.5, board.height - 1 - row + 0.5), 0.4, color='k')
                ax.add_patch(circle)
       

    # set the limits of the axes
    ax.set_xlim([0, board.height])
    ax.set_ylim([0, board.width])

    # hide the tick labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # show the figure
    plt.show()

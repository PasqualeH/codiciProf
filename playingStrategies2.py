import math
import random

def minimax_search(game, state):
    """Search game tree to determine best move; return (value, move) pair."""

    player = state.to_move

    def max_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a))
            if v2 > v:
                v, move = v2, a
        return v, move

    def min_value(state):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a))
            if v2 < v:
                v, move = v2, a
        return v, move

    return max_value(state)

infinity = math.inf

def alphabeta_search(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    def max_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)



def cache1(function):
    "Like lru_cache(None), but only considers the first argument of function."
    cache = {}
    def wrapped(x, *args):
        if x not in cache:
            cache[x] = function(x, *args)
        return cache[x]
    return wrapped


def alphabeta_search_tt(game, state):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    @cache1
    def max_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta):
        if game.is_terminal(state):
            return game.utility(state, player), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity)

def cutoff_depth(d):
    """A cutoff function that searches to depth d."""
    return lambda game, state, depth: depth > d

def h_alphabeta_search(game, state, cutoff=cutoff_depth(2)):
    """Search game to determine best action; use alpha-beta pruning.
    As in [Figure 5.7], this version searches all the way to the leaves."""

    player = state.to_move

    @cache1
    def max_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player,game), None
        v, move = -infinity, None
        for a in game.actions(state):
            v2, _ = min_value(game.result(state, a), alpha, beta, depth+1)
            if v2 > v:
                v, move = v2, a
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    @cache1
    def min_value(state, alpha, beta, depth):
        if game.is_terminal(state):
            return game.utility(state, player), None
        if cutoff(game, state, depth):
            return h(state, player,game), None
        v, move = +infinity, None
        for a in game.actions(state):
            v2, _ = max_value(game.result(state, a), alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, a
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move

    return max_value(state, -infinity, +infinity, 0)



def h (state, player, game):
    min = 7
    max = 11
    player = state.to_move
    available_moves = list(game.actions(state))
    cont = len(available_moves)
    if cont > 13:
        val4 = 0
        val3 = 0
        val2 = 0
        val1 = 0
        #valM = 0

        if cont % 2 == 0:
            if casoTreUno(available_moves) == 3:
                valM = 115
                val3 = (-81 - 100 + cont) * cont * valM
            if casoTreUno(available_moves) == 1:
                valM = 100
                val3 = (-81 - 100 + cont) * cont * valM
            if casoTreUno(available_moves) == -1:
                valM = 100
                val3 = (-81 - 100 + cont) * cont * valM
            if casoQuattroDue(available_moves) == 4:
                valM = 75
                val3 = (-81 + 100 + cont) * cont * valM
            if casoQuattroDue(available_moves) == 2:
                valM = 100
                val3 = (-81 + 100 + cont) * cont * valM

            if val4 < val2 and val4 < val3 and val4 < val1:
                return val4
            elif val2 < val3 and val2 < val4 and val2 < val1:
                return val2
            elif val3 < val4 and val3 < val2 and val3 < val1:
                return val3
            elif val1 < val4 and val1 < val2 and val1 < val3:
                return val1
            else:
                return (-81 + 100 + cont) * cont * 40

        else:
            if casoTreUno(available_moves) == 3:
                valM = 120
                val3 = (-81 + 100 + cont) * cont * valM
            if casoTreUno(available_moves) == 1:
                valM = 100
                val3 = (-81 + 100 + cont) * cont * valM
            if casoTreUno(available_moves) == -1:
                valM = 100
                val3 = (-81 + 100 + cont) * cont * valM
            if casoQuattroDue(available_moves) == 4:
                valM = 100
                val3 = (-81 - 100 + cont) * cont * valM
            if casoQuattroDue(available_moves) == 2:
                valM = 75
                val3 = (-81 - 100 + cont) * cont * valM

            if val4 < val2 and val4 < val3 and val4 < val1:
                return val4
            elif val2 < val3 and val2 < val4 and val2 < val1:
                return val2
            elif val3 < val4 and val3 < val2 and val3 < val1:
                return val3
            elif val1 < val4 and val1 < val2 and val1 < val3:
                return val1
            else:
                return (-81 + 100 + cont) * cont * 40

    else:
        if cont % 2 == 1:
            if casoTreUno(available_moves) == 3:
                return (((cont * float(100)) / float(81)) * float(1000000) / 100) - float(1000000) + (random.randrange(max - min + 1) + min) * 25000
            elif casoTreUno(available_moves) == 1:
                return (((cont * float(100)) / float(81)) * float(1000000) / 100) - float(1000000) + (random.randrange(max - min + 1) + min) * 15000
            elif casoTreUno(available_moves) == -1:
                return (((cont * float(100)) / float(81)) * float(1000000) / 100) - float(1000000) + (random.randrange(max - min + 1) + min) * 15000

        else:
            if casoQuattroDue(available_moves) == 4:
                return (((cont * float(100)) / float(81)) * float(1000000) / 100) - float(1000000) + (random.randrange(max - min + 1) + min) * 35000
            elif casoQuattroDue(available_moves) == 2:
                return (((cont * float(100)) / float(81)) * float(1000000) / 100) - float(1000000) + (random.randrange(max - min + 1) + min) * 15000
            elif casoQuattroDue(available_moves) == 0:
                return (((cont * float(100)) / float(81)) * float(1000000) / 100) - float(1000000) + (random.randrange(max - min + 1) + min) * 25000

    return (((cont * float(100)) / float(81)) * float(1000000) / 100) - float(1000000) + (random.randrange(max - min + 1) + min) * 45000


def casoTreUno(available_moves):
    for i in range(9):
        for j in range(9):
            if ((i > 0 and i < 8) and (j > 0 and j < 8)):
                # casi per sbloccare 3 mosse
                if (i, j) in available_moves:  # -1 == mossa disponibile
                    if (i + 1, j) in available_moves and (i, j - 1) in available_moves and (i, j + 1) in available_moves:
                        return 3
                    if (i - 1, j) in available_moves and (i, j - 1) in available_moves and (i, j + 1) in available_moves:
                        return 3
                    if (i + 1, j) in available_moves and (i - 1, j) in available_moves and (i, j + 1) in available_moves:
                        return 3
                    if (i + 1, j) in available_moves and (i - 1, j) in available_moves and (i, j - 1) in available_moves:
                        return 3

                        # casi per sbloocare 1 mossa (corner)
                    if (i, j + 1) not in available_moves and (i + 1, j) not in available_moves:
                        return 1
                    if (i, j - 1) not in available_moves and (i + 1, j) not in available_moves:
                        return 1
                    if (i - 1, j) not in available_moves and (i, j + 1) not in available_moves:
                        return 1
                    if (i - 1, j) not in available_moves and (i, j - 1) not in available_moves:
                        return 1

                        # caso che mette una pedina in mezzo ad altre 4
                    if (i - 1, j) not in available_moves and (i + 1, j) not in available_moves and (i, j - 1) not in available_moves and (i, j + 1) not in available_moves:
                        return -1
    return 0

def casoQuattroDue(lista_mosse_disponibili):
    for i in range(9):
        for j in range(9):
            if (i, j) in lista_mosse_disponibili:
                #Caso per sbloccare 4 mosse
                if ((i >0 and i < 8) and (j > 0 and j < 8)):
                    if (i - 1, j) in lista_mosse_disponibili and  (i + 1, j) in lista_mosse_disponibili and (i,j-1) in lista_mosse_disponibili and (i, j + 1) in lista_mosse_disponibili:
                        return 4
                    #casi per sbloccare 2 mossa
                    if (i,j+1) in lista_mosse_disponibili and (i+1,j) in lista_mosse_disponibili:
                        return 2
                    if (i-1,j) in lista_mosse_disponibili and (i,j-1) in lista_mosse_disponibili:
                        return 2
                    if (i-1,j) in lista_mosse_disponibili and (i+1,j) in lista_mosse_disponibili:
                        return 2
                    if (i-1,j) in lista_mosse_disponibili and (i,j+1) in lista_mosse_disponibili:
                        return 2
                    if (i,j-1) in lista_mosse_disponibili and (i,j+1) in lista_mosse_disponibili:
                        return 2
                    if (i,j-1) in lista_mosse_disponibili and (i+1,j) in lista_mosse_disponibili:
                        return 2
    return 0



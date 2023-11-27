import copy
import math
import random
from math import log, sqrt, inf
from random import randrange
import numpy as np
from rich.table import Table
from rich.progress import track
from rich.console import Console
from rich.progress import Progress
#import classes.game as game
import classes.logic as logic

# When implementing a new strategy add it to the `str2strat`
# dictionary at the end of the file


class PlayerStrat:
    def __init__(self, _board_state, player):
        self.root_state = _board_state
        self.player = player

    def start(self):
        """
        This function select a tile from the board.

        @returns    (x, y) A tuple of integer corresponding to a valid
                    and free tile on the board.
        """
        raise NotImplementedError

class Node(object):
    """
    This class implements the main object that you will manipulate : nodes.
    Nodes include the state of the game (i.e. the 2D board), children (i.e. other children nodes), a list of
    untried moves, etc...
    """
    def __init__(self, board, move=(None, None),
                 wins=0, visits=0, children=None):
        # Save the #wins:#visited ratio
        self.state = board
        self.move = move
        self.wins = wins
        self.visits = visits
        self.children = children or []
        self.parent = None
        self.untried_moves = logic.get_possible_moves(board)

    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class Random(PlayerStrat):
    # Build here the class for a random player
    def init(self, _board_state, player):
        super().init(_board_state, player)

    def start(self):
        return random.choice(logic.get_possible_moves(self.root_state))

class MiniMax(PlayerStrat):
    # Build here the class implementing the MiniMax strategy
    def init(self, _board_state, player):
        super().init(_board_state, player)

    def minimax_search(self, _board_state, player):
        infinity = math.inf

        def utility(_board_state, player):
            """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
            player_opponent = 2 if player  == 1 else 1
            if logic.is_game_over(player, _board_state) == player:
                utility = 1
            elif logic.is_game_over(player_opponent, _board_state) == player_opponent:
                utility = -1
            else:
                utility = 0
            return utility

        def result(player, _board_state, move):
            """Place a marker for current player on square."""
            real_node = Node(copy.deepcopy(_board_state), move=move)
            (x, y) = real_node.move
            real_node.state[x][y] = player
            
            #_board_state[x][y] = player
            player = 1 if player == 2 else 2
            return _board_state

        def max_value(_board_state, player):
            if logic.is_game_over(player, _board_state):
                return utility( _board_state, player), None
            value = -infinity
            action = None
            actions = logic.get_possible_moves(_board_state)
            for a in actions:
                v2, a2 = min_value(result(player, _board_state, a),player)
                if v2 > value :
                    value = v2
                    action = a
            return value, action

        def min_value(_board_state, player):
            if logic.is_game_over(player, _board_state):
                return utility( _board_state, player), None
            value = infinity
            action = None
            actions = logic.get_possible_moves(_board_state)
            for a in actions:
                v2, a2 = max_value(result(player, _board_state, a),player)
                if v2 < value :
                    value = v2
                    action = a 
            return value, action

        return max_value(_board_state, player)

    def start(self):
        value, move = self.minimax_search(self.root_state, self.player)
        return move

str2strat = { #: dict[str, PlayerStrat] 
        "human": None,
        "random": Random,
        "minimax": MiniMax,
    }

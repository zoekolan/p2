import os
import pickle
import logging
from rich import print
from rich.logging import RichHandler

# Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
import pandas as pd

from classes.logic import player2str
from classes.game import Game

from classes import logic
from classes import strategy

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET",
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler()]
)


class Tournament:
    def __init__(self, args: list):
        """
        Initialises a tournament with:
           * the size of the board,
           * the players strategies, eg., ("human", "random"),
           * the game counter,
           * the number of games to play.
        """
        self.args = args
        (self.BOARD_SIZE, self.STRAT, self.GAME_COUNT,
         self.N_GAMES, self.USE_UI) = args

        if self.USE_UI:
            pygame.init()
            pygame.display.set_caption("Polyline")

    def single_game(self, black_starts: bool=True) -> int:
        """
        Runs a single game between two opponents.

        @return   The number of the winner, either 1 or 2, for black
                  and white respectively.
        """

        game = Game(board_size=self.BOARD_SIZE,
                    black_starts=black_starts,
                    strat=self.STRAT,
                    use_ui=self.USE_UI)
        game.print_game_info(
            [self.BOARD_SIZE, self.STRAT, self.GAME_COUNT]
        )
        while game.winner is None:
            game.play()

        print(f"{player2str[game.winner]} player ({self.STRAT[game.winner-1]}) wins!")

        return game.winner

    def championship(self):
        """
        Runs a number of games between the same two opponents.
        """
        scores = [0, 0]
        moves_to_win = [0, 0]

        for _ in range(self.N_GAMES):
            self.GAME_COUNT = _

            # First half of the tournament started by one player.
            # Remaining half started by other player (see "no pie
            #  rule")
            winner = self.single_game(
                black_starts=self.GAME_COUNT < self.N_GAMES / 2
            )
            scores[winner-1] += 1
            #moves_to_win[winner-1] += logic.get_nb_moves(BOARD, winner)


        log = logging.getLogger("rich")

        # TODO Design your own evaluation measure!
        # https://pyformat.info/
        """
        Compares the scores of two approaches and returns the evaluation measure.
        Soit :
         - on fait sur un grand nombre de jeux et on voit qui à tendance à gagner le plus
         - on regarde la vitesse d'exécution pour gagner
         - on regarde le nombre de coups joués pour gagner
        """
        log.info("Design your own evaluation measure!")

        if scores[0] == scores[1]:
            winner = 0
        elif scores[0] > scores[1]:
            winner = 1
        else:
            winner = 2

        approach1_wins = scores[0]
        approach2_wins = scores[1]
        # si eeval_measure est négative c'est que le joueur 2 est meilleur
        evaluation_measure = (approach1_wins - approach2_wins) / self.N_GAMES

        print("scores : ({a} - {b}) // Winner is Player {c}".format(a=scores[0], b=scores[1], c=winner))
        print("mesure d'evaluation : {a}".format(a=evaluation_measure))

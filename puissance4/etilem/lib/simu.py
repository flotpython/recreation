# coding: utf-8
# pylint: disable=c0103,r0903,r0913,c0301
"""
module de simulation à la demande
"""
from .game import Game
from .board import Board
from .config import WIDTH, HEIGHT, LENGTH

class Simu:
    """
    Simulation
    """
    def __init__(self, p1, p2, locale, width=WIDTH, height=HEIGHT, length=LENGTH):

        self.game = Game(Board(width, height), (p1, p2), length, locale)

    def start(self):
        """
        Démarre la simulation
        """
        while True:
            print(self.game.board)
            if self.game.board.is_full():
                print(self.game.say('deuce'))
                break
            case = self.game.player.play(self.game)
            self.game.update(case)
            if self.game.has_winner():
                print(self.game.board)
                x, _ = case
                print(self.game.say('has_played', self.game.player, f"c{x+1}"), self.game.say('has_won'))
                break
            self.game.next_move()

#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=c0103
"""
simulation aléatoire de partie
"""

from random import randint

from p4_config import HUMAN, MACHINE, WIDTH, HEIGHT, LENGTH
from p4_board import Board
from p4_player import Player
from p4_game import Game

game = Game(Board(WIDTH, HEIGHT), [Player(t) for t in (HUMAN, MACHINE)], LENGTH)

def start():
    """
    Démarre la simulation aléatoire
    """
    while True:
        if game.board.is_full():
            print(game.board)
            print("Egalité !")
            break
        col = randint(1, game.board.width)
        if game.update(col):
            if game.has_winner():
                print(game.board)
                print(f"{game.player}  a joué c{col} et gagne !")
                break
            game.next_move()

    print(f"\nLongueur du segment recherché : {LENGTH}")

if __name__ == "__main__":
    start()

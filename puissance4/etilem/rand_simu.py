#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=c0103
"""
simulation aléatoire de partie
"""

from random import randint

from lib import Game, Board, Player, WIDTH, HEIGHT, LENGTH

length = LENGTH
game = Game(Board(WIDTH, HEIGHT), (Player(), Player()), length)

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

    print(f"\nLongueur du segment recherché : {length}")

if __name__ == "__main__":
    start()

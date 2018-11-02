#!/usr/bin/env python3
# coding: utf-8
# pylint: disable=c0103
"""
simulation aléatoire de partie
"""

from lib import Game, Board, Random, WIDTH, HEIGHT, LENGTH

length = LENGTH
game = Game(Board(WIDTH, HEIGHT), (Random(), Random()), length)

def start():
    """
    Démarre la simulation aléatoire
    """
    while True:
        if game.board.is_full():
            print(game.board)
            print("Egalité !")
            break
        case = game.player.play(game.board)
        game.update(case)
        if game.has_winner():
            print(game.board)
            x, _ = case
            print(f"{game.player}  a joué c{x+1} et gagne !")
            break
        game.next_move()

    print(f"\nLongueur du segment recherché : {length}")

if __name__ == "__main__":
    start()

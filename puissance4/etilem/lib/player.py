# coding: utf-8
"""
module de joueur
"""

from random import choice, randint

from .contrib.search import has_won
from .sprite import Sprite

class Player():
    """
    Joueur
    """

    def __init__(self, color=Sprite.VOID):
        self.code = color

    def __str__(self):
        return Sprite(self.code).__str__()

class Human(Player):
    """
    Joueur interactif (utilisateur)
    """
    def __init__(self):
        Player.__init__(self)

    def play(self, game):
        """
        Joue une case candidate
        """
        columns = list((x+1 for x, _ in game.board.playable_cases()))
        col = 0
        while col not in columns:
            try:
                col = int(input(game.say('choice')))
            except ValueError:
                print(game.say('invalid'))
        for x, y in game.board.playable_cases():
            if x == col-1:
                return x, y

class Random(Player):
    """
    Joueur machine jouant au hasard
    """
    def __init__(self):
        Player.__init__(self)

    def play(self, game):
        """
        Joue une case candidate
        """
        return choice(list(game.board.playable_cases()))

class AI(Player):
    """
    Joueur IA
    """
    def __init__(self):
        Player.__init__(self)

    def play(self, game):
        """
        Joue une case candidate
        """
        best = -game.board.width * game.board.height * 1000
        a, b = best, -best
        best_play = ()
        for case in game.board.playable_cases():
            v = self.negamax(game.board, game.player, case, a, b, game.length, 3)
            if v > best:
                best = v
                best_play = case
        return best_play

    def negamax(self, board, player, case, alpha, beta, length, depth):
        """
        selon https://fr.wikipedia.org/wiki/%C3%89lagage_alpha-b%C3%AAta#Pseudocode

        fonction alphabeta(nœud, A, B) /* A < B */
           si nœud est une feuille alors
               retourner la valeur de nœud
           sinon
               meilleur = –∞
               pour tout fils de nœud faire
                   v = -alphabeta(fils,-B,-A)
                   si v > meilleur alors
                       meilleur = v
                       si meilleur > A alors
                           A = meilleur
                           si A ≥ B alors
                               retourner meilleur
               retourner meilleur
        """
        if depth == 0:
            return randint(1, length)
        clone = board.clone()
        clone.update(case, player)
        if clone.is_full():
            return 0
        for l in reversed(range(3, length+1)):
            if has_won(clone, player, l):
                return length * l
        best = -clone.width * clone.height * 1000
        for future in clone.playable_cases():
            v = -self.negamax(clone, player, future, -beta, -alpha, length, depth - 1)
            if v > best:
                best = v
                if best > alpha:
                    alpha = best
                    if alpha >= beta:
                        return best
        return best

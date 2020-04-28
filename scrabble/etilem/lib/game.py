
from .bag import Bag
from .player import Computer, Virtual
from .boards import Board
from itertools import cycle


class Game():

    bag = Bag()
    board = Board()
    players = (Computer("Alicia"), Computer("Robert"),
               Computer("Jeanne"), Computer("Alfred"))
    null = len(players)

    def play(self, player, move, score):
        word, vec = move
        for i, letter in enumerate(word):
            try:
                x, y, horiz = vec
                if horiz:
                    if self.board.is_free(x, y + i):
                        player.tiles.remove(letter)
                else:
                    if self.board.is_free(x + i, y):
                        player.tiles.remove(letter)
            except ValueError:
                player.tiles.remove('*')
        if self.board.is_scrabble(word, vec):
            print(player.name, "fait un scrabble !")
        self.board.place(word, vec)
        player.fill_tiles(self.bag, self.board.max_tiles)
        self.null = len(self.players)
        print("{} joue {} en {}{} et marque {} points".format(
            player.name, word, chr(64 + x + 1), y + 1, score))
        player.score += score
        print("Son score actuel est de", player.score)

    def cant_play(self, player):
        print(player.name, "passe son tour")
        print("Son score actuel est de", player.score)
        self.null -= 1

    def start(self):
        for current in cycle(self.players):
            print("==========================================\n")
            current.fill_tiles(self.bag, self.board.max_tiles)
            if self.bag.is_empty():
                print("Le sac est vide")
            print(current.name, "a les lettres :", current.get_tiles())
            try:
                move, score = current.find_best_move(self.board)
                self.play(current, move, score)
                if len(current.tiles) == 0:
                    if self.bag.is_empty():
                        print(current.name, "a fini la partie !")
                        print(self.board)
                        break
            except ValueError:
                self.cant_play(current)
                print(self.board)
                if self.null == 0:
                    print("\n", "Les joueurs sont bloqués,",
                          "la partie est terminée")
                    break
                continue
            print(self.board)
        print("\n", "Voici les scores :\n")
        win = Virtual("")
        for p in self.players:
            print(p.score, "points pour", p.name, end='')
            if len(p.tiles) > 0:
                print(", il lui restait : ", p.get_tiles())
            else:
                print(", qui a terminé en premier")
            if p.score > win.score:
                win = p
        print("\n", win.name, "a gagné la partie !")

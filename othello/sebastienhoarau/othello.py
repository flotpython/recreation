"""
    Othello.py (1re version, très naïve)
    Auteur : Sébastien Hoarau
    Date : 2018-10-11

    Ami lecteur attention sache que :
    1. Mon code n'est pas commenté (pas le temps)
    2. J'ai du mal encore avec la programmation objet
        notamment sur le découpage (ici l'objet Game et l'objet Othello)
        qui s'occupe de quoi, quel attribut, chez qui ? etc...
        Ce premier jet est donc très naïf, n'hésitez pas à commenter :)
        Typiquement je ne sais pas où mettre mon attribut player (joueur courant) :
        mon objet game qui gère le jeu (un peu le contrôleur) en a besoin (par exemple
        pour mettre à jour les scores mais l'objet métier Othello en a aussi besoin :
        faut-il dupliquer cette info ? la mettre dans Othello seulement ?)
"""

SIZE = 8
NOIR = 0
BLANC = 1
VIDE = -1
NOON = -1
LABELS = '\u25C9\u25CE.'
LETTRES = 'ABCDEFGH'
HUMAIN = 0
MACHINE = 1
QUIT = 'QUIT'
PASS = 'PASS'
DELTAS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1), (1, 1), (-1, -1))


def inside(x, y):
    return 0 <= x < SIZE and 0 <= y < SIZE


class Othello:

    def __init__(self):
        self.g = [[VIDE] * SIZE for _ in range(SIZE)]
        self.g[3][3:5] = [BLANC, NOIR]
        self.g[4][3:5] = [NOIR, BLANC]
        self.player = NOIR
        self.last_move = None
        self.candidats = [{},{}]


    def __str__(self):
        letters_line = '  ' + ' '.join([c for c in LETTRES])
        s = letters_line
        for idl in range(SIZE):
            s += f'\n{idl+1} '
            for idc in range(SIZE):
                s += f'{LABELS[self.g[idl][idc]]} '
            s += f'{idl+1}'
        s += f'\n{letters_line}'
        return s 


    def empty(self, idc, idl):
        return self.g[idl][idc] == VIDE

    def next_player(self):
        self.player = 1 - self.player

    def update_candidats(self):
        # for p in [NOIR, BLANC]:
        self.candidats[self.player] = {}
        for idc in range(SIZE): 
            for idl in range(SIZE):
                if self.empty(idc, idl):
                    tmp = []
                    for dc, dl in DELTAS:
                        nidc, nidl = idc + dc, idl + dl
                        nbajout = 0
                        while inside(nidc, nidl) and self.g[nidl][nidc] == 1 - self.player:
                            tmp.append((nidc, nidl))
                            nbajout += 1
                            nidc += dc
                            nidl += dl
                        if nbajout > 0 and (not inside(nidc, nidl) or self.empty(nidc, nidl)):
                            tmp[-nbajout:] = []
                    if tmp:
                        self.candidats[self.player][(idc, idl)] = tmp


    def update_g(self):
        idc, idl = self.last_move
        self.g[idl][idc] = self.player
        delta_score = 1
        for nidc, nidl in self.candidats[self.player][(idc, idl)]:
            self.g[nidl][nidc] = self.player
            delta_score += 1
        return delta_score

    def check_position(self, pos):
        idc, idl = pos
        idc = LETTRES.index(idc)
        idl = int(idl) - 1
        return idc, idl, (idc, idl) in self.candidats[self.player]

    def ia(self):
        l_move = list(self.candidats[self.player].items())
        l_move.sort(key=lambda c: len(c[1]), reverse=True)
        if l_move:
            move = f'{LETTRES[l_move[0][0][0]]}{l_move[0][0][1]+1}'
        else:
            move = PASS
        return move

    def no_moves(self):
        return self.candidats[self.player] == {}
    
    def passe(self):
        print(f'  {LABELS[self.player]} PASS')
        self.last_move = PASS

class Game:

    def __init__(self):
        self.othello = Othello()
        self.players = None
        self.scores = [2, 2]
        self.game_over = False
        self.winner = NOON
        self.othello.update_candidats()

    def __str__(self):
        s = '\n' + self.othello.__str__() + '\n\n'
        s += f'  {LABELS[NOIR]} {self.scores[NOIR]}\t{LABELS[BLANC]} {self.scores[BLANC]}'
        if self.game_over:
            results =[f'\n  {LABELS[NOIR]} gagne !\n', f'\n  {LABELS[BLANC]} gagne !\n', 
                        '\n  Partie nulle.\n']
            s += results[self.winner]
        return s

    def settings(self):
        print('Bienvenue sur OTHELLO')
        print('Qui joue ?')
        print(f'0. Humain {LABELS[NOIR]} vs Humain {LABELS[BLANC]}')
        print(f'1. Humain {LABELS[NOIR]} vs Machine {LABELS[BLANC]}')
        rep = ''
        while rep != 0 and rep != 1:
            try:
                rep = int(input('Votre choix : '))
            except:
                rep = ''
        self.players = (HUMAIN, rep)



    def get_position(self):
        def good_coord(c):
            return LETTRES[0] <= c[0] <= LETTRES[-1] and 1 <= int(c[1]) <= SIZE
        print(f'  {LABELS[self.othello.player]} joue... ', end='')
        if self.players[self.othello.player] == HUMAIN:
            print()
            r = input('  Quelle position ? (ex. A4 ou quit pour arrêter) ').upper()
            while r != QUIT and (len(r) != 2 or not good_coord(r)):
                r = input('  Pas compris... votre réponse : ').upper()
        else:
            r = self.othello.ia()
            print(r) 
        return r



    def opponent(self):
        return 1 - self.player

    def quit(self, abandon=False):
        self.game_over = True
        if abandon:
            self.winner = 1 - self.othello.player
        elif self.scores[NOIR] > self.scores[BLANC]:
            self.winner = NOIR
        elif self.scores[NOIR] < self.scores[BLANC]:
            self.winner = BLANC

    def passe(self):
        self.othello.passe()
        self.othello.next_player()                    
        self.othello.update_candidats()


    def update_scores(self, delta):
        player = self.othello.player
        self.scores[player] += delta
        self.scores[1 - player] -= delta - 1
    
    def update(self, idc, idl):
        self.othello.last_move = idc, idl
        delta_score = self.othello.update_g()
        self.update_scores(delta_score)
        self.othello.next_player()
        self.othello.update_candidats()


    def play(self):
        self.othello.update_candidats()
        while not self.game_over:
            print(self)
            if self.othello.no_moves():
                if self.othello.last_move == PASS:
                    self.passe()
                    self.quit()
                else:
                    self.passe()
            else:
                position = self.get_position()
                self.last_move = position
                if position == QUIT:
                    self.quit(abandon=True)
                else:
                    idc, idl, checked = self.othello.check_position(position)
                    if not checked:
                        print('  Position invalide')
                    else:
                        self.update(idc, idl)


    def fictiveGame(self, filename):
        self.scores[NOIR] = 0
        self.scores[BLANC] = 0
        with open(filename, 'r', encoding='utf8') as fgame:
            for idl, ligne in enumerate(fgame):
                ligne = ligne.split()
                for idc, val in enumerate(ligne):
                    val = int(val)
                    if val != VIDE:
                        self.othello.g[idl][idc] = val
                        self.scores[val] += 1


jeu = Game()
jeu.settings()
# jeu.fictiveGame('end_game.csv')
jeu.play()
print(jeu)

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

# -- CONSTANTES
# --

SIZE = 8                    # taille de l'échiquier
NOIR = 0                    # joueur X
BLANC = 1                   # joueur O
VIDE = -1                   # pour une case vide
NOON = -1                   # la valeur du winner quand y'en n'a pas :)
LABELS = '\u25C9\u25CE.'    # les étiquettes qui seront affichées
LETTRES = 'ABCDEFGH'        # numérotation des colonnes
HUMAIN = 0                  # qd c'est un joueur humain qui joue
MACHINE = 1                 # qd c'est la machine qui joue
QUIT = 'QUIT'               # le coup qu consiste à arrêter prématurément
PASS = 'PASS'               # quand on est bloqué, on doit passer
                            # quand y'a eu deux PASS consécutifs la partie est finie (comme au GO)

# Pour calculer les voisins d'une case            
DELTAS = ((1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1), (1, 1), (-1, -1))


def inside(x, y):
    """ True ssi (x, y) est dans notre grille 8x8 """
    return 0 <= x < SIZE and 0 <= y < SIZE


class Othello:

    def __init__(self):
        self.g = [[VIDE] * SIZE for _ in range(SIZE)]   # l'échiquier remplit de VIDE pour l'instant
        self.g[3][3:5] = [BLANC, NOIR]                  # on met les 2 pions NOIR et le 2 BLANC
        self.g[4][3:5] = [NOIR, BLANC]
        self.player = NOIR                              # joueur courant, initialisé avec NOIR
        self.last_move = None                           # le dernier coup joué
        self.candidats = {}                             # dict des cases jouables pour le joueur courant


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
        """ Calcule le dictionnaire des cases jouables pour le joueur
            courant sous la forme : {(idc, idl) : [(nidc, nidl),...]} où
            idc et idl représente les coordonnées colonne x ligne des cases
            vides jouables et nidc, nidl les coordonnées des cases qui seront
            retournées dès lors """
        self.candidats = {}
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
                            # on tombe sur une case vide ou sur la fin de la grille
                            # on enlève les case ajoutées car elles ne sont pas retournables en fait
                            tmp[-nbajout:] = []
                    if tmp:
                        # on a trouvé des cases à retourner, case valide on l'ajoute
                        self.candidats[(idc, idl)] = tmp


    def update_g(self):
        """ mise à jour de l'échiquier : on récupère les coordonnées du dernier coup
            on met à jour la case avec le numéro du joueur courant
            on met aussi à jour l'échiquier de toutes les cases retournables associées
            à la case jouée
            on retourne le nombre de cases obtenues pour le joueur courant 
            (pour la mise à jour des scores) """
        idc, idl = self.last_move
        self.g[idl][idc] = self.player
        for nidc, nidl in self.candidats[(idc, idl)]:
            self.g[nidl][nidc] = self.player
        return len(self.candidats[(idc, idl)]) + 1

    def memorise(self, idc, idl):
        self.last_move = idc, idl

    def check_move(self, pos):
        """ Teste qu'une pos style D4 est jouable ie qu'en transformant
            en coord (3, 3) ces coordonnées sont dans les cases candidates """
        idc, idl = pos
        idc = LETTRES.index(idc)
        idl = int(idl) - 1
        return idc, idl, (idc, idl) in self.candidats

    def ia(self):
        """ Une IA plus que basique : joue le coup qui maximise le gain de pion 
            si possible, passe sinon """
        l_move = list(self.candidats.items())
        l_move.sort(key=lambda c: len(c[1]), reverse=True)
        if l_move:
            move = f'{LETTRES[l_move[0][0][0]]}{l_move[0][0][1]+1}'
        else:
            move = PASS
        return move

    def no_moves(self):
        """ True ssi il n'y a plus de coups possibles pour le joueur courant """
        return self.candidats == {}
    
    def passe(self):
        """ Affiche que le joueur courant a passé et met à jour last_move """
        print(f'  {LABELS[self.player]} PASS')
        self.last_move = PASS


class Game:

    def __init__(self):
        self.othello = Othello()            # l'objet jeu Othello
        self.players = []                   # la liste des deux joueurs (HUMAIN ou MACHINE)
        self.scores = [2, 2]                # le tableau des scores
        self.game_over = False              # flag pour savoir si la partie est finie
        self.winner = NOON                  # le numéro du joueur gagnant NOON si aucun

    def __str__(self):
        s = '\n' + self.othello.__str__() + '\n\n'
        s += f'  {LABELS[NOIR]} {self.scores[NOIR]}\t{LABELS[BLANC]} {self.scores[BLANC]}'
        if self.game_over:
            results =[f'\n  {LABELS[NOIR]} gagne !\n', f'\n  {LABELS[BLANC]} gagne !\n', 
                        '\n  Partie nulle.\n']
            s += results[self.winner]
        return s

    def settings(self):
        """ Choix des joueurs """
        print('Bienvenue sur OTHELLO')
        for pion in [NOIR, BLANC]:
            print(f'Qui joue {LABELS[pion]} ?')
            print('  0. Humain')
            print('  1. Machine')
            rep = ' '
            while rep not in '01':
                rep = input('Votre choix : ')
            self.players.append(int(rep))



    def get_move(self):
        """ Demande au joueur courant un coup """
        def good_coord(c):
            return LETTRES[0] <= c[0] <= LETTRES[-1] and 1 <= int(c[1]) <= SIZE
        # on affiche c'est à qui de jouer (noir ou blanc)
        print(f'  {LABELS[self.othello.player]} joue... ', end='')
        # si le joueur est humain on lui demande
        if self.players[self.othello.player] == HUMAIN:
            print()
            r = input('  Quelle position ? (ex. A4 ou quit pour arrêter) ').upper()
            while r != QUIT and (len(r) != 2 or not good_coord(r)):
                r = input('  Pas compris... votre réponse : ').upper()
        # sinon c'est la machine qui fait appelle à son ia
        else:
            r = self.othello.ia()
            print(r) # on affiche ce que la machine a joué
        return r


    def quit(self, abandon=False):
        """ Pour quitter le jeu, éventuellement par abandon : le winner est 
            alors l'autre joueur, ie pas le joueur courant """
        self.game_over = True
        if abandon:
            self.winner = 1 - self.othello.player
        elif self.scores[NOIR] > self.scores[BLANC]:
            self.winner = NOIR
        elif self.scores[NOIR] < self.scores[BLANC]:
            self.winner = BLANC


    def passe(self):
        """ Quand on passe dans la partie, faut appeler la méthode passe du jeu
            passer au joueur suivant puis recalculer les candidats """
        self.othello.passe()
        self.othello.next_player()                    
        self.othello.update_candidats()


    def update_scores(self, delta):
        """ mise à jour des scores avec le delta de pion gagné par le joueur courant """
        player = self.othello.player
        self.scores[player] += delta
        self.scores[1 - player] -= delta - 1
    
    def update(self, idc, idl):
        """ mise à jour de la partie : mémorisation du dernier coup
            mise à jour de l'échiquier, mise à jour des scores
            ensuite on passe au joueur suivant, on met à jour les candidats """
        self.othello.memorise(idc, idl)
        delta_score = self.othello.update_g()
        self.update_scores(delta_score)
        self.othello.next_player()
        self.othello.update_candidats()


    def play(self):
        """ Jouer une partie :
            on commence par mettre à jour les candidats puisque 4 cases sont déjà jouées
            ensuite, tant que la partie n'est pas game over :
            on affiche la partie ie l'échiquier et les infos de scores et de joueur courant
            on vérifie pour le joueur courant si par hasard il n'est pas bloqué :
                si oui alors on passe et si c'est le 2e PASS c'est fini
                sinon on récupère le coup du joueur courant et on le traite """

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
                move = self.get_move()
                self.last_move = move
                if move == QUIT:
                    self.quit(abandon=True)
                else:
                    idc, idl, checked = self.othello.check_move(move)
                    if not checked:
                        print('  Position invalide')
                    else:
                        self.update(idc, idl)
        print(self)


    def fictiveGame(self, filename):
        """ Pour préremplir l'échiquier avec une partie déjà commencée """
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

# Othello

import numpy as np
# import tranche

import timeit

VIDE = 0
NOIR = 1
BLANC = -1
SIZE = 8
COLONNES = 'ABCDEFGH'
LIGNES = [str(i+1) for i in range(SIZE)]
DIRECTIONS = {'N':(-1,0),
              'S':(1,0),
              'E':(0,1), 
              'W':(0,-1), 
              'NE':(-1,1), 
              'SE':(1,1), 
              'NW':(-1,-1),
              'SW':(1,-1),
              }
JOUEURS = ['AI', 'Player']


class Othello:
    """ Le jeu du même nom """

    def __init__(self, jeu=None, couleur=NOIR):
        with open('log.txt', 'w', encoding='utf8') as f:
            f.write('LOG:\n')
        self.log = ''
        if jeu:
            self.jeu = jeu
        else:
            self.jeu = np.zeros((SIZE, len(COLONNES)), dtype=np.int8)
            self.jeu[3][4], self.jeu[4][3] = NOIR, NOIR
            self.jeu[3][3], self.jeu[4][4] = BLANC, BLANC
        self.couleur = couleur     # La couleur de Player
        self.joueur = 1 if self.couleur == NOIR else 0  # Le joueur dont c'est le tour de jouer (correspond à l'indice dans JOUEURS)
        self.dico_de_tranches = None
        self.update()

    def __str__(self):
        """ renvoie le plateau de jeu sous forme d'un tableau """
        return '\n'.join(';'.join(str(i) for i in ligne) for ligne in self.jeu)

    def write(self, file):
        """ Ecrit le plateau de jeu dans le fichier donné """
        with open(file, 'w', encoding='utf8') as f:
            f.write(str(self))
        
    def read(self, file):
        """ 
        Renvoie le plateau de jeu lu dans le fichier donné
        - un fichier qui a été écrit avec self.write(file) -
        """
        array = []
        with open(file, 'r', encoding='utf8') as f:
            for line in f:
                for i in line.split(';'):
                    array.append(int(i))
        jeu = np.array((array), dtype=np.int8)
        return jeu.reshape((SIZE, len(COLONNES)))

    def next(self):
        """
        Renvoie True si le jeu peut continuer et passe alors au joueur suivant,
        renvoie False sinon
        """
        if self.casesJouables(self.get_couleur(self.adversaire(self.joueur))):
            self.joueur = self.adversaire(self.joueur)
            return True
        else:
            return False

    def adversaire(self, joueur):
        """ L'indice de l'adversaire dans JOUEURS """
        return 1-joueur
        
    def get_couleur(self, joueur):
        """ La couleur du joueur """
        return self.couleur if JOUEURS[joueur] == 'Player' else -self.couleur
        
    def get_tranche(self, case, direction):
        """
        Renvoie une 'tranche' de la table à partir de la case donnée et dans la direction donnée
        """
        (l, c) = case
        if direction == 'E':
            return self.jeu[l, c:]
        elif direction == 'W':
            return self.jeu[l, :c+1]
        elif direction == 'N':
            return self.jeu[:l+1, c]
        elif direction == 'S':
            return self.jeu[l:, c]
        elif direction == 'SE':
            return self.jeu[l:].diagonal(c)
        elif direction == 'SW':  # A revoir
            return self.jeu[l:].transpose().diagonal(c)
            # return np.array([self.jeu[i, k] for i, k in zip(range(l, SIZE), range(c))])
        elif direction == 'NE': # A revoir
            return self.jeu[:l+1].transpose().diagonal(c)
            # return np.array([self.jeu[i, k] for i, k in zip(range(l+1), range(c, len(COLONNES)))])
        elif direction == 'NW': 
            return self.jeu[:l].diagonal(c-l)
        else:
            return np.array([0])
        
    def directions(self, dico, case):
        """
        Mets à jour le dictionnaire des directions de la case considérée 
        (key = une direction, value = tranche de jeu pour la case considérée)
        """
        for dir in DIRECTIONS:
            dico[case][dir] = self.get_tranche(case, dir)
            self.log = f'case:{case} -> {dir}={dico[case][dir]}\n'
            with open('log.txt', 'a', encoding='utf8') as f:
                f.write(self.log)
                
    
    def update(self):
        """
        Met à jour le dictionnaire de tranches qui donne pour chaque case le dictionnaire des directions
        """
        if not self.dico_de_tranches:
            self.dico_de_tranches = dict()
            for l in range(SIZE):
                for c in range(len(COLONNES)):
                    self.dico_de_tranches[(l,c)]=dict()
                    self.directions(self.dico_de_tranches, (l,c))
        else:
            for case in self.dico_de_tranches.keys():
                self.directions(self.dico_de_tranches, case)
        
    def isJouable(self, tranche, couleur):
        """ Booléen de jouabilité de la tranche selon la couleur """
        jouable = False
        if len(tranche)>1:
            if tranche[0]!=0:
                if couleur in tranche[1:]:
                    jouable = True
        return jouable
                

    def casesJouables(self, couleur):
        """ renvoie une liste des cases qui sont jouables par la couleur indiquée """
        liste = []
        for case in self.dico_de_tranches.keys():
            if self.jeu[case[0]][case[1]]==VIDE:   # on ne regarde que les cases qui sont vide 
                for tranche in self.dico_de_tranches[case].values():
                     # if tranche.description(couleur)[0]:
                     if self.isJouable(tranche, couleur):
                        liste.append(case)
                        break
        return liste
        
    def get_index(self, tranche, couleur):
        """ Renvoie l'index de la couleur cherchée dans la tranche considérée """
        index = 0
        if self.isJouable(tranche, couleur):
            index = tranche[1:].tolist().index(couleur) + 1
            if index > 1 and not 0 in self.tranche[1:index]:
                pass
            else: index = 0
        return index

    def meilleurCoup(self, couleur):
        """ renvoie la case de la liste des possibilities qui retourne le plus de jetons """
        possibilities = self.casesJouables(couleur)
        if possibilities:
            best = 0
            meilleureCase = possibilities[random(len(possibilities))] 
            for case in possibilities:
                num = 0
                for tranche in self.dico_de_tranches[case].values():
                    num += self.get_index(tranche, couleur)-1
                if num > best:
                    best = num
                    meilleureCase = case
        else: meilleureCase = None
        return meilleureCase

    def score(self):
        """ renvoie le score (NOIR, BLANC) """
        totN = 0
        totB = 0
        for l in self.jeu:
            for i in l:
                if i == NOIR:
                    totN += 1
                elif i == BLANC:
                    totB += 1
        return (totN, totB)

    def jouer(self, case, joueur):
        """
            ajoute le jeton de couleur sur la case,
            retourne les pions à retourner
            mets à jour le dictionnaire des tranches de jeu
        """
        (l, c) = case
        for (dir, tranche) in self.dico_de_tranches[case].items():
            if tranche.description(self.get_couleur(joueur))[0]:
                index = tranche.description(self.get_couleur(joueur))[1]
                for i in range(index):
                    self.jeu[l+DIRECTIONS[dir][0]*i][c+DIRECTIONS[dir][1]*i] = self.get_couleur(joueur)
        if self.next():
            self.update() 
            return self.toString(case)
        else:
            return 'EOG'

    def toString(self, case):
        c = COLONNES[case[0]]
        l = LIGNES[case[1]]
        return ''.join((c, l))

    def playAI(self):
        """ Détermine la case que jouera l'AI puis joue """
      #  self.log += '\n' + '* '*10 + 'AI is playing' + ' *'*10 + '\n'
        case = self.meilleurCoup(-self.couleur)
        if case:
            return self.jouer(case, 0)
        else:
            return 'EOG'

    def playJoueur(self, case):
        """ Verifie la jouablilité de la case """
       # self.log += '\n' + '* '*10 + 'Joueur is playing' + ' *'*10 + '\n'
        possibilities = self.casesJouables(self.couleur)
        if possibilities:
            if case in possibilities:
                return self.jouer(case, 1)
            else:
                return False
        else: 
            return 'EOG'
    
# oth = Othello()
# with open('log.txt', 'a', encoding='utf8') as f:
     # f.write(oth.log)
    
# oth = Othello()
# timeit.timeit('[Othello()]', globals=globals())

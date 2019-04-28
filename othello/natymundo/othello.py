# Othello

import numpy as np
import random
import re

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
        cases = None
        self.update(cases)

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

    def adversaire(self, joueur):
        """ L'indice de l'adversaire dans JOUEURS """
        return 1-joueur
        
    def get_couleur(self, joueur):
        """ La couleur du joueur """
        return self.couleur if JOUEURS[joueur] == 'Player' else -self.couleur
        
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
        
    def get_tranche(self, case, direction):
        """
        Renvoie une 'tranche' de la table à partir de la case donnée -incluse- et dans la direction donnée
        """
        (l, c) = case
        if direction == 'E':
            return self.jeu[l, c:]
        elif direction == 'W':
            return self.jeu[l, :c+1][::-1]
        elif direction == 'N':
            return self.jeu[:l+1, c][::-1]
        elif direction == 'S':
            return self.jeu[l:, c]
        elif direction == 'SE':
            return self.jeu[l:].diagonal(c)
        elif direction == 'SW':  # A revoir
            return np.rot90(self.jeu[l:, 0:c+1]).diagonal() 
        elif direction == 'NE': # A revoir
            return np.rot90(self.jeu[:l+1, c:], 3).diagonal() 
        elif direction == 'NW': 
            return self.jeu[:l+1].diagonal(c-l)[::-1]
        else:
            return np.array([0])
        
    # def directions(self, dico, case):
        # """
        # Mets à jour le dictionnaire des directions de la case considérée 
        # (key = une direction, value = tranche de jeu pour la case considérée)
        # """
        # for dir in DIRECTIONS:
            # dico[case][dir] = self.get_tranche(case, dir)                
    
    def update(self, cases):
        """
        Met à jour le dictionnaire de tranches qui donne pour chaque case le dictionnaire des directions
        """
        couleur = self.get_couleur(self.joueur)
        if self.dico_de_tranches:
            for key in self.dico_de_tranches.keys():
                dict.clear(self.dico_de_tranches[key])
        else:
            self.dico_de_tranches = dict()
        if not cases:
            cases = self.casesJouables(couleur)
        for case in cases:
            for dir in DIRECTIONS:
                t = self.get_tranche(case, dir)
                if self.isJouable(t, couleur):
                    if not case in self.dico_de_tranches:
                        self.dico_de_tranches[case] = dict()
                    self.dico_de_tranches[case][dir]=t
            self.log += f'self.dico_de_tranches[{case}]={self.dico_de_tranches[case]}\n'
        with open('log.txt', 'a', encoding='utf8') as f:
            f.write(self.log)
            self.log = '/'*10 + '\n'
        
    def isJouable(self, tranche, couleur): ### Utiliser des regex !!
        """ Booléen de jouabilité de la tranche selon la couleur """
        # jouable = False
        # if len(tranche)>1:
            # if tranche[0]==0 and tranche[1]==-couleur:
                # if couleur in tranche[2:]:
                    # index = self.get_index(tranche, couleur)
                    # j = 1
                    # while j < index: 
                        # if tranche[j]!=-couleur:
                            # j = index + 1 
                        # else:
                            # j += 1
                    # if j==index:
                        # jouable = True
        # return jouable
        if couleur == 1:
            pattern = '^0(-1+)(1+)'
        else:
            pattern = '^0(1+)(-1+)'
        txt = ''
        for i in tranche:
            txt += str(i)
        # self.log += f'{pattern} match {txt}: {re.match(pattern, txt)}\n'
        return re.match(pattern, txt)
        
                

    def casesJouables(self, couleur):  
        """ renvoie une liste des cases qui sont jouables par la couleur indiquée """
        liste = []
        for l in range(SIZE):
            for c in range(len(COLONNES)):
                if self.jeu[l][c]==VIDE:   # on ne regarde que les cases vides 
                    for dir in DIRECTIONS:
                        t = self.get_tranche((l,c), dir)
                        if self.isJouable(t, couleur) and not (l,c) in liste:
                            liste.append((l,c))
        return liste
        
    def get_index(self, tranche, couleur):
        """ Renvoie l'index de la couleur cherchée dans la tranche considérée """
        return tranche.tolist().index(couleur)

    def meilleurCoup(self, couleur):  ## utiliser le dico
        """ renvoie la case de la liste des possibilities qui retourne le plus de jetons """
        possibilities = self.casesJouables(couleur)
        if possibilities:
            best = 0
            meilleureCase = possibilities[random.randrange(len(possibilities))] 
            for case in possibilities:
                num = 0
                for tranche in self.dico_de_tranches[case].values():
                    num += self.get_index(tranche, couleur)-1
                if num > best:
                    best = num
                    meilleureCase = case
        else: 
            meilleureCase = None
        return meilleureCase
        
    def next(self):
        """
        Renvoie True si le jeu peut continuer et passe alors au joueur suivant,
        renvoie False sinon
        """
        cases = self.casesJouables(self.get_couleur(self.adversaire(self.joueur)))
        if cases:
            self.joueur = self.adversaire(self.joueur)
        return cases

    def jouer(self, case, joueur):
        """
            ajoute le jeton de couleur sur la case,
            retourne les pions à retourner
            mets à jour le dictionnaire des tranches de jeu
        """
        (l, c) = case
        self.log += f'Case jouée: {case}\n'
        for (dir, tranche) in self.dico_de_tranches[case].items():
            index = self.get_index(tranche, self.get_couleur(joueur))
            self.log += f'Tranche retournée: {dir}, index={index}\n'
            for i in range(index):
                self.jeu[l+DIRECTIONS[dir][0]*i][c+DIRECTIONS[dir][1]*i] = self.get_couleur(joueur)
        next_cases = self.next()
        if next_cases:
            self.update(next_cases) 
            return self.toString(case)
        else:
            return 'EOG'

    def toString(self, case):
        c = COLONNES[case[0]]
        l = LIGNES[case[1]]
        return ''.join((c, l))

    def playAI(self):
        """ Détermine la case que jouera l'AI puis joue """
        self.log += '\n' + '* '*10 + 'AI is playing' + ' *'*10 + '\n'
        case = self.meilleurCoup(-self.couleur)
        if case:
            return self.jouer(case, 0)
        else:
            return 'EOG'

    def playJoueur(self, case):
        """ Verifie la jouablilité de la case """
        self.log += '\n' + '* '*10 + 'Joueur is playing' + ' *'*10 + '\n'
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

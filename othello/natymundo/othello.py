# Othello

import numpy as np


VIDE = 0
NOIR = 1
BLANC = -1
SIZE = 8
COLONNES = 'ABCDEFGH'
LIGNES = [str(i+1) for i in range(SIZE)]
DIRECTIONS = {(a, b) for a in (-1, 0, 1) for b in (-1, 0, 1)}


class Othello:
    """
        Le jeu du même nom
    """

    def __init__(self, jeu=None):
        self.log = 'LOG: \n'
        if jeu:
            self.jeu = jeu
        else:
            self.jeu = np.zeros((SIZE, len(COLONNES)), dtype=np.int8)
            self.jeu[3][4], self.jeu[4][3] = NOIR, NOIR
            self.jeu[3][3], self.jeu[4][4] = BLANC, BLANC
        self.joueur = NOIR
        self.dico_de_cases = dict({(l,c):dict() for l in range(SIZE) for c in range(len(COLONNES))})
        self.mise_a_jour()

    def __str__(self):
        return '\n'.join(';'.join(str(i) for i in ligne) for ligne in self.jeu)

    def write(self, file):
        with open(file, 'w', encoding='utf8') as f:
            f.write(str(self))
        
    def read(self, file):
        array = []
        with open(file, 'r', encoding='utf8') as f:
            for line in f:
                for i in line.split(';'):
                    array.append(int(i))
        jeu = np.array((array), dtype=np.int8)
        return jeu.reshape((SIZE, len(COLONNES)))

    def next(self):
        self.joueur = -self.joueur

    def adversaire(self, couleur):
        return -couleur
        
    def directions(self, case):
        """
        Mets à jour le dictionnaire des directions de la case considérée (key = une direction, value = tranche de jeu pour la case considérée)
        ex: (1, 0):[self.joueur, BLANC, BLANC, NOIR, BLANC, VIDE]
        """
        for (a, b) in DIRECTIONS:
            if a==b and b==0:
                pass
            else:
                tranche = [self.jeu[case[0]][case[1]]]
                A, B = case[0]+a, case[1]+b
                while 0 <= A < SIZE and 0 <= B < len(COLONNES):
                    tranche.append(self.jeu[A][B])
                    A += a
                    B += b
                self.dico_de_cases[case][(a, b)] = self.direction_a_retourner(tranche)
                
        
    def direction_a_retourner(self, direction):
        """
        La direction est une tranche de jeu.
        Renvoie une liste des retournables pour la direction donnée,
        Le premier de la liste correspond à la case regardée, et sera un booléen pour savoir si cette direction est retournables
        Ensuite, -1 s'il faut retourner, 1 quand ça s'arrête
        En reprenant l'exemple de self.directions(jeu, case):
        en supposant que self.joueur = NOIR, alors on aurait [True, -1, -1, 1, BLANC, VIDE]
        """
        txt = ''
        direction[0] = True
        if self.joueur in direction[2:]:
            index = direction[1:].index(self.joueur) + 1
            txt += f'index={index} // '
            if index == 1:
                direction[0] = False
            direction[index] = 1
            for i in range(1, index):
                 txt += f'i={i} // '
                 if direction[i] == VIDE or index == 1:
                    direction[0] = False
                 else:
                    direction[i] = -1
        else:
            direction[0] = False
        if direction[0]:
            self.log += txt + f'direction: {direction}\n'
        return direction
            
        
    def mise_a_jour(self):
        """
        Met à jour le dictionnaire des cases qui donne pour chaque case le dictionnaire des directions
        """
        self.log += '\nMise à jour\n'
        for case in self.dico_de_cases.keys():
            if self.jeu[case[0]][case[1]]==VIDE:
                self.directions(case)
            else:
                for k in self.dico_de_cases[case].keys():
                    self.dico_de_cases[case][k]=[False,1]
        with open('test.txt', 'a') as f:
            f.write(self.log)
            

    def casesJouables(self):
        """
            renvoie une liste des cases qui sont jouables par le joueur actuel
        """
        liste = []
        for case in self.dico_de_cases.keys():
            for tranche in self.dico_de_cases[case].values():
                 if tranche[0]:
                    liste.append(case)
                    break
        return liste

    def meilleurCoup(self):
        """ renvoie la case de la liste des possibilities qui retourne le plus de jetons """
        possibilities = self.casesJouables()
        if possibilities:
            best = 0
            meilleureCase = possibilities[0]  # -> Changer 0 par un random!
            for case in possibilities:
                num = 0
                for tranche in self.dico_de_cases[case].values():
                    num += tranche.count(-1)
                    #self.log += f'{case}: num = {num}\n'
                if num > best:
                    best = num
                    meilleureCase = case
            self.log += f'meilleureCase= {meilleureCase}\n'
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

    def jouer(self, case):
        """
            ajoute le jeton de couleur sur la case,
            retourne les pions à retourner
            mets à jour le dictionnaire des tranches de jeu
        """
        (l, c) = case
        self.log += f'case jouée: {(l, c)}\n'
        for (dir, tranche) in self.dico_de_cases[case].items():
            if tranche[0]:
                index = tranche[1:].index(1)
                self.log += f'index des jetons à retourner dans {dir}:{tranche} = {index}\n'
                for i in range(index+1):
                    self.jeu[l+dir[0]*i][c+dir[1]*i] = self.joueur   
        self.next()
        self.mise_a_jour() 

    def toString(self, case):
        c = COLONNES[case[0]]
        l = LIGNES[case[1]]
        return ''.join((c, l))

    def playAI(self):
        """ Détermine la case que jouera l'AI """
        self.log += '\n' + '*'*10 + 'AI is playing...' + '*'*10 + '\n'
        case = self.meilleurCoup()
        if case:
            self.jouer(case)
            t = self.toString(case)
        else:
            t = 'EOG'
        return t

    def playJoueur(self, case):
        """ Verifie la jouablilité de la case """
        self.log += '\n' + '*'*10 + 'Joueur is playing...' + '*'*10 + '\n'
        possibilities = self.casesJouables()
        if possibilities:
            if case in possibilities:
                self.jouer(case)
                return self.toString(case)
            else:
                return False
        else: return 'EOG'
    
# oth = Othello()
# oth.playAI()
# oth.playJoueur((4,2))
 # with open('test.txt', 'w') as f:
     # f.write(oth.log)
    

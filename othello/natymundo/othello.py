# Othello

import numpy as np


VIDE = 0
NOIR = 1
BLANC = -1
JOUABLE = 'x'
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
                    txt += f'direction[{i}]=-1 // '
        else:
            direction[0] = False
        if direction[0]:
            self.log += txt + f'direction: {direction}\n'
        return direction
            
        
    def mise_a_jour(self):
        """
        Met à jour le dictionnaire des cases qui donne pour chaque case le dictionnaire des directions
        """
        for case in self.dico_de_cases.keys():
            self.directions(case)
            # for (k, v) in self.dico_de_cases[case].items():
                # self.log += f'{case}: {k}={v}\n'
            # self.log += '-'*10 + '\n'
            
            

    # ATTENTION: il est obligatoire de retourner au moins un pion adverse à chaque tour!
    def casesJouables(self, couleur):
        """
            retourne une copie du plateau de jeu
            avec le nb de jetons qui seront retournés en jouant sur la case en question
            ('x' si ce nombre vaut 1 pour ne pas le confondre avec NOIR)
        """
        # remarquez bien qu'à chaque appel de casesJouables
        # on réalloue un tableau de jeu complet, ça peut être une cause
        # de lenteur; avez-vous envisagé que ça puisse être à l'appelant
        # de passer un jeu en paramètre pour optimiser ces allocations ?
        ####
        #   Ce tableau n'est-il pas détruit à la fin de ma fonction??
        ####
        jouable = []
        for l in range(SIZE):
            jouable.append([])
            for c in range(len(COLONNES)):
                jouable[l].append(self.jeu[l][c])
                pos = self.isJouable(l, c, couleur)
                if pos:
                    jouable[l][c] = len(pos)
                    if jouable[l][c] == 1:
                        jouable[l][c] = 'x'
        return jouable

    def casesAdjacentes(self, ligne, colonne, couleur):
        """ renvoie les couleurs des cases adjacentes """
        couleurs = []
        for (a, b) in DIRECTIONS:
            if a == b or a == -b:
                pass
            else:
                if 0 <= ligne+a < SIZE and 0 <= colonne+b < len(COLONNES):
                    couleurs.append(self.jeu[ligne+a][colonne+b])
        return couleurs

    def retournera(self, ligne, colonne, couleur):
        """ renvoie un tableau des jetons à retourner """
        t = []
        for (a, b) in DIRECTIONS:
            if a == b == 0:
                pass
            else:
                A = a
                B = b
                tmp = []
                while 0 <= ligne+A < SIZE and 0 <= colonne+B < SIZE:
                    if self.jeu[ligne+A][colonne+B] == VIDE:
                        A = SIZE
                        B = SIZE
                        pass
                    elif self.jeu[ligne+A][colonne+B] == couleur:
                        if (A, B) in DIRECTIONS:  # 1er passage
                            A = SIZE
                            B = SIZE
                            pass
                        else:
                            for (l, c) in tmp:
                                t.append((l, c))
                            break
                    else:
                        tmp.append((ligne+A, colonne+B))
                        A += a
                        B += b
        return t

    def isJouable(self, ligne, colonne, couleur):
        """
            renvoie un tableau des cases qui seront retournées ou VIDE si le tableau est vide
        """
        pos = VIDE
        if self.jeu[ligne][colonne] not in (NOIR, BLANC):
            if self.adversaire(couleur) in self.casesAdjacentes(ligne, colonne, couleur):
                pos = self.retournera(ligne, colonne, couleur)
                if not pos:
                    pos = VIDE
        return pos

    def meilleurCoup(self, couleur):
        """ renvoie le couple (ligne, colonne) correspondant à la case qui retourne le plus de jetons """
        possibilities = self.casesJouables(couleur)
        maxSize = 0
        for l in range(SIZE):
            for c in range(len(COLONNES)):
                n = possibilities[l][c]
                if not n in (VIDE, NOIR, BLANC):
                    if n == 'x':
                        n = 1
                    if n > maxSize:
                        meilleureCase = (l, c)
                        maxSize = n
        return meilleureCase

    def score(self):
        """ renvoie le score (NOIR, BLANC) """
        totN = 0
        totB = 0
        for l in range(SIZE):
            for c in range(len(COLONNES)):
                if self.jeu[l][c] == NOIR:
                    totN += 1
                elif self.jeu[l][c] == BLANC:
                    totB += 1
        return (totN, totB)

    def jouer(self, ligne, colonne, casesARetourner):
        """
            ajoute le jeton de couleur sur la case,
            retourne les pions à retourner
            efface les autres cases jouables
        """
        self.jeu[ligne][colonne] = self.joueur
        for (l, c) in casesARetourner:
            self.jeu[l][c] = -self.jeu[l][c]
        for l in range(SIZE):
            for c in range(len(COLONNES)):
                if self.jeu[l][c] not in (VIDE, NOIR, BLANC):
                    self.jeu[l][c] = VIDE
        self.next()

    def toString(self, case):
        c = COLONNES[case[0]]
        l = LIGNES[case[1]]
        return ''.join((c, l))

    def playAI(self):
        """ Détermine la case que jouera l'AI """
        case = self.meilleurCoup(self.joueur)
        pos = self.isJouable(case[0], case[1], self.joueur)
        self.jouer(case[0], case[1], pos)
        return self.toString(case)

    def playJoueur(self, ligne, colonne):
        """ Verifie la jouablilité de la case """
        pos = self.isJouable(ligne, colonne, self.joueur)
        if pos:
            self.jouer(ligne, colonne, pos)
            return self.toString((ligne, colonne))
        else:
            return False
    
oth = Othello()
with open('test.txt', 'w') as f:
    f.write(oth.log)
    

# -*- coding: utf-8 -*-

# pour dire à pylint de ne pas vérifier la présence des docstring
# pylint: disable=c0111
# vérifier avec
# $ pip3 install pylint
# $ pylint othello.py
# il reste quelques identificateurs qui ne sont pas casher, je vous laisse
# choisir de les rectifier ou pas

"""
Created on Sun Oct  7 21:07:27 2018
Evolutions avec prise en compte compteur et fin de jeu , mais reste à debugguer ...
@author: JP
"""
import numpy as np


class Grille:
    # classe pour gerer la grille
    def __init__(self):
        self.tableau = np.zeros((8, 8))
        self.tableau[3][3], self.tableau[4][4] = 1, 1
        self.tableau[3][4], self.tableau[4][3] = 2, 2
        self.pions = [". ", "O ", "X "]

    def __str__(self):
        nom_col = "  A B C D E F G H\n"
        msg = "\n" + nom_col
        for i in range(8):
            msg += f"{i+1} "
            for j in range(8):
                msg += self.pions[int(self.tableau[i][j])]
            msg += f" {i+1}\n"
        msg += nom_col
        return msg

    @staticmethod
    def adjacents():
        # précédemment
        # adj = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
        #        (0, 1), (1, -1), (1, 0), (1, 1)]
        return [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]


    def pose(self, forme, ligne, colonne):
        # verifie si pose d'un pion forme permet ou pas de retouner
        # des pions del'autre forme

        # teste case jouee non vide
        if int(self.tableau[ligne][colonne]):
            print("erreur : case non vide")
            return False

        # init retour à False si pas de pions retournables
        retour = False

        # tuples des cellules adjacentes possibles en relatifs
        for dx, dy in self.adjacents():
            if not self.testcase(ligne+dx, colonne+dy):  # case adj hors grille
                continue
            formeadj = self.tableau[ligne+dx][colonne+dy]
            if not formeadj == 3-forme:  # case adj vide ou meme couleur
                continue

            # case adj de couleur differente, on teste les cases audelà ds cette direction
            i = 2
            while self.testcase(ligne+i*dx, colonne+i*dy):
                formeadj = self.tableau[ligne+i*dx][colonne+i*dy]
                if formeadj == 0:  # on tombe sur case vide = mauvaise direction
                    break  # on regarde les autres cases adjacentes
                if formeadj == forme:
                    self.remplitcases(ligne, colonne, i, dx, dy, forme)
                    retour = True  # on a retourne des pieces
                    break  # on regarde les autres cases adjacentes
                i += 1  # on continue dans la direction
        return retour  # True si on a retourné des pions False sinon

    def posetest(self, forme, ligne, colonne):
        # verifie si pose d'un pion forme permet ou pas de retouner
        # des pions del'autre forme
        # redondance de code avec pose : optimisation à voir

        for dx, dy in self.adjacents():
            if not self.testcase(ligne+dx, colonne+dy):  # case adj hors grille
                continue
            formeadj = self.tableau[ligne+dx][colonne+dy]
            if not formeadj == 3-forme:  # case adj vide ou meme couleur
                continue

            # case adj de couleur differente, on teste les cases audelà ds cette direction
            i = 2
            while self.testcase(ligne+i*dx, colonne+i*dy):
                formeadj = self.tableau[ligne+i*dx][colonne+i*dy]
                if formeadj == 0:  # on tombe sur case vide = mauvaise direction
                    break  # on regarde les autres cases adjacentes
                if formeadj == forme:
                    return True  # possible
                i += 1  # on continue dans la direction

        return False

    def testcase(self, x, y):
        # teste si une case est bien dans la grille
        return 0 <= x <= 7 and 0 <= y <= 7

    def remplitcases(self, ligne, colonne, i, dx, dy, forme):
        # remplit les cases qu'on peut retourner dans la direction validee
        for j in range(i):
            self.tableau[ligne+j*dx][colonne+j*dy] = forme

    def partie_terminee(self):
        # teste si toutes cases occupées : aucune case à 0 ou jeu bloqué pour les 2
        return self.tableaurempli() or self.jeubloque()

    def jeubloque(self):
        # teste si les 2 joueurs sont bloqués
        return not (self.testejeupossible(1) or self.testejeupossible(2))

    def testejeupossible(self, forme):
        # regarde si on poser un pion sur une des cases vides
        for i in range(8):
            for j in range(8):
                if not self.tableau[i][j]:  # case vide
                    if self.posetest(forme, i, j):  # verifie pose possible
                        #print (f" A Joueur {self.joueur[forme-1]} de jouer")
                        return True
        return False

    def tableaurempli(self):
        # teste si le tableau est rempli
        return np.count_nonzero(self.tableau == 0) == 0

    def compteformes(self):
        # renvoie un tuple des nombres de croix et de ronds
        return (np.count_nonzero(self.tableau == 1),
                np.count_nonzero(self.tableau == 2))


class Jeu:

    def __init__(self):
        self.grille = Grille()
        print(self.grille)
        self.colonnes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.lignes = [str(i+1) for i in range(8)]
        self.joueur = ["Rond", "Croix"]


    def partie(self):
        # partie principale
        forme = 2  # les X commencent
        condstop = False
        while not self.grille.partie_terminee() and not condstop:
            totalrond, totalcroix = self.grille.compteformes()

            print(f"Compteur : Rond = {totalrond} Croix = {totalcroix} ")

            while True:
                # teste si le joueur a une case possible pour poser sa forme
                # presque le meme code que pose en testant toutes les cases à 0
                # mais sans modifier

                if not self.jouetest(forme):
                    forme = 3-forme
                    break

                # saisie case valide
                case = self.entreevalide(forme)
                # condition arret
                if case == '00':
                    condstop = True
                    break

                # transcrit la saisie en ligne colonne du tableau
                idxlign, idxcol = case[1], case[0].upper()
                ligne = self.lignes.index(idxlign)
                colonne = self.colonnes.index(idxcol)

                # test si case permet de retourner des pions
                if self.joue(forme, ligne, colonne):
                    # ici il faudrait un compteur des formes X et O
                    forme = 3-forme  # changement de joueur
                    break
        totalrond, totalcroix = self.grille.compteformes()
        print(f"Compteur final : Rond = {totalrond} Croix = {totalcroix} ")


    def entreevalide(self, forme):
        # teste la validite de la saisie des cases par les joueurs
        while True:
            case = input(
                f"Joueur {self.joueur[forme-1]} quelle case(ex: A4 ? (00 pour arreter) ")
            if not len(case) == 2:
                print("ce n'est pas une case valide")
                continue
            if case == '00':  # condition sortie
                print("OK on arrete")
                return case

            if case[0].upper() not in self.colonnes or case[1] not in self.lignes:
                print("ce n'est pas une case valide")
                continue
            return case


    def joue(self, forme, ligne, colonne):
        # verifie si la case choisie permet de poser un pion
        # et si oui retourne les pions autre forme
        # verifie pose possible et retourne les pions
        if self.grille.pose(forme, ligne, colonne):
            print(self.grille)
            return True
        else:
            print("rejouez case non autorisée pour vous")
            return False


    def jouetest(self, forme):
        # verifie la possibilité de poser du joueur sinon passera son tour
        # verifie qu'au moins une case peut etre jouee
        if self.grille.testejeupossible(forme):
            return True

        print(f"Joueur {self.joueur[forme-1]} ne peut jouer")
        return False


jeu = Jeu()
jeu.partie()

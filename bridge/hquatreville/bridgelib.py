#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 14:34:46 2018
Fourni les classes suivantes :
    Longueur
        -> affichage d'une longueur dans une couleur donnée
        -> attribution d'une qualité (un honneur = 10)
           et d'une valeur en points H
    Main
        -> Une Main de bridge avec les 4 couleurs
        -> Affichage de cette main au standard d'un diagramme de bridge
        -> Méthode vertues renvoie un tableau de statistiques sur la Main
    Donne
        -> Les quatre mains + le donneur + la vulnérabilité
        -> Affichage du diagramme
        -> Distribution
        -> Codage et décodage pour transmission
    Filtre
        -> Filtre d'une main selon ses vertues
        -> Méthode filtre renvoyant un booléen
    Sequence
        -> Groupe de filtres s'appliquant à une donne 
        -> Méthode filtre renvoyant un booléen


@author: hubert
"""
from random import randint, shuffle
from itertools import product
from numpy.random import choice

DEBUG = False


class Longueur:
    '''Une longueur dans une couleur particulière'''

    def __init__(self, cartes):
        self.cartes = set(cartes)

    def __repr__(self):
        valeur = ['2', '3', '4', '5', '6', '7',
                  '8', '9', '10', 'V', 'D', 'R', 'A']
        return " ".join(valeur[x] for x in sorted(self.cartes, reverse=True))

    def __len__(self):
        return len(self.cartes)

    def qualite(self):
        honneur = [0, 0, 0, 0, 0, 0, 0, 1, 2, 5, 10, 10, 10]
        res = 0
        for x in self.cartes:
            res += honneur[x]
        return res

    def pointH(self):
        pointH = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4]
        return sum((pointH[x] for x in self.cartes), 0)


from enum import IntEnum


class Couleur(IntEnum):
    TREFLE = 0
    CARREAU = 1
    COEUR = 2
    PIQUE = 3

    def glyph(self):
        ''' glyphes en couleur en mode console'''
        glyphs = {Couleur.TREFLE: '\u2663',
                  Couleur.CARREAU: '\x1b[31;1m\u2666\x1b[39;0m',
                  Couleur.COEUR: '\x1b[31;1m\u2665\x1b[39;0m',
                  Couleur.PIQUE: '\u2660'}
        return glyphs[self]

    def nbglyph(self):
        ''' glyphes en noir et blanc'''
        nbglyphs = {Couleur.TREFLE: '\u2663',
                    Couleur.CARREAU: '\u2666',
                    Couleur.COEUR: '\u2665',
                    Couleur.PIQUE: '\u2660'}
        return nbglyphs[self]

    def teinte(self):
        ''' couleur du foreground pour tk'''
        teintes = {Couleur.TREFLE: 'black',
                   Couleur.CARREAU: 'red',
                   Couleur.COEUR: 'red',
                   Couleur.PIQUE: 'black'}
        return teintes[self]


class Main:

    '''Une Main de bridge avec les quatre couleurs'''

    def __init__(self, trefle, carreau, coeur, pique):
        self.couleurs = [
            Longueur(trefle),
            Longueur(carreau),
            Longueur(coeur),
            Longueur(pique)]
        self.trefle, self.carreau, self.coeur, self.pique = self.couleurs

    def __getitem__(self, couleur):
        """
        self[0] ou self[Couleur.TREFLE] retourne self.trefle
        """
        assert couleur in Couleur
        return self.couleurs[couleur]

    def affiche(self, decalage=0, autre_main=None):

        if autre_main:
            for couleur in Couleur:
                print(couleur.glyph(), self[couleur],
                      ' '*(26-len(str(self[couleur]))),
                      couleur.glyph(), autre_main.couleurs[couleur])
        else:
            for couleur in Couleur:
                print(' '*decalage, couleur.glyph(), self[couleur])

    def _codes(self):
        '''
        Renvoie la liste des cartes de la main codées entre 0 et 51
        Usage interne uniquement
        '''
        res = []
        for couleur in Couleur:
            for carte in self[couleur].cartes:
                res.append(couleur*13 + carte)
        # print(res)
        return res

    def vertues(self):
        pointD = [3, 2, 1, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        '''# XXX:  évalue la main selon les critères habituels des bridgeurs :
            0 : valeur de la main en points H
            1,2,3,4 : longueurs des 4 couleurs
            5,6,7,8 : qualité de ces couleurs
            9 : évaluation conventionnelle de la distibution D '''
        res = []
        points = self.trefle.pointH()
        points += self.carreau.pointH()
        points += self.coeur.pointH()
        points += self.pique.pointH()
        res.append(points)
        res.append(len(self.trefle))
        res.append(len(self.carreau))
        res.append(len(self.coeur))
        res.append(len(self.pique))
        res.append(self.trefle.qualite())
        res.append(self.carreau.qualite())
        res.append(self.coeur.qualite())
        res.append(self.pique.qualite())
        distribution = pointD[len(self.trefle)]
        distribution += pointD[len(self.carreau)]
        distribution += pointD[len(self.coeur)]
        distribution += pointD[len(self.pique)]
        res.append(distribution)
        return res


def decode_main(liste):
    ''' Creation d'une main à partir d'une liste de cartes codées de 0 à 51'''
    listes = [[] for i in range(4)]
    for carte in liste:
        listes[carte//13].append(carte % 13)
    return Main(*listes)


class Position(IntEnum):
    NORD = 0
    SUD = 1
    EST = 2
    OUEST = 3

    def name(self):
        names = ['Nord', 'Sud', 'Est', 'Ouest']
        return names[self]

    def visibilite(self):
        ''' Liste rendant visible une position donnée '''
        return [pos == self for pos in Position]

    def visibilite_ligne(self):
        ''' Liste rendant visible la ligne de la position donnée '''
        return [pos//2 == self//2 for pos in Position]


class Vulnerabilite(IntEnum):
    PERSONNE = 0
    NS = 1
    EO = 2
    TOUS = 3

    def name(self):
        vulnerabilites = ['Personne', 'NS', 'EO', 'Tous']
        return vulnerabilites[self]


class Donne:

    def __init__(self, sud=None, nord=None, est=None, ouest=None,
                 donneur=0, vul=0, identifiant=None):
        '''
        On peut créer une donne de trois façons. En entrant les quatre mains
        et optionnellement la vulnérabilité et le donneur, ou bien
        en la générant aléatoirement, ou encore en entrant un identifiant 
        unique associée à chaque donne possible. 
        Les syntaxes possibles sont

        1) Donne(nord=((2,5,6,10),(2,11),(0,12),(3,5,6,8,10)), 
        sud = cartes de sud, est = ..., ouest = ... ) 
        facultativement
        Donne(nord=..., sud = ..., est = ..., ouest = ..., donneur = , vul = )
        si on veut indiquer le donneur et la vulnérabilité

        2) Donne() pour distribuer une main aléatoirement ou

        3) Donne(identifiant = un nombre) pour retrouver une donne dont on a 
        conservé l'identifiant'''

        if sud:
            self.sud = Main(*sud)
            self.nord = Main(*nord)
            self.est = Main(*est)
            self.ouest = Main(*ouest)
            self.donneur = Position(donneur)
            self.vul = Vulnerabilite(vul)
            self._code()
        elif identifiant:  # Reconstitue la main à partir d'un identifiant un
            self._reconstitution(identifiant)
        else:
            # On distribue les cartes
            # print("distribution")
            melange = list(range(52))
            shuffle(melange)
            self.attributions = list(range(52))
            for i in range(52):
                self.attributions[melange[i]] = i//13
            self._decode()
            self.donneur = Position(randint(0, 3))
            self.vul = Vulnerabilite(randint(0, 3))

    def __getitem__(self, position):
        """
        self[0] ou self[Position.NORD] retourne self.nord
        """
        assert position in Position
        return [self.nord, self.sud, self.est, self.ouest][position]

    def _decode(self):
        ''' Reconstitue les quatre mains en fonction des attributions des cartes '''
        # print("decodage")
        liste_des_mains = [[] for i in range(4)]
        for n in range(52):
            liste_des_mains[self.attributions[n]].append(n)
        self.nord = decode_main(liste_des_mains[0])
        self.sud = decode_main(liste_des_mains[2])
        self.est = decode_main(liste_des_mains[1])
        self.ouest = decode_main(liste_des_mains[3])

    def _code(self):
        ''' Attribue à chaque carte la main dans laquelle elle a été distribuée'''
        self.attributions = list(range(52))
        for x in self.nord._codes():
            # print(x,0)
            self.attributions[x] = 0
        for x in self.sud._codes():
            # print(x,2)
            self.attributions[x] = 2
        for x in self.est._codes():
            # print(x,1)
            self.attributions[x] = 1
        for x in self.ouest._codes():
            # print(x,3)
            self.attributions[x] = 3

    def identifiant(self):
        ''' Calcul de l'identifiant unique de la donne. Le résultat est
        transformé en chaîne de caractères
        pour transmission par des fichiers textes'''

        mon_id = 0
        att = list(self.attributions)
        att.append(self.donneur)
        att.append(self.vul)
        for i in range(54):
            mon_id *= 4
            mon_id += att[i]
        return hex(mon_id)

    def _reconstitution(self, identifiant):
        ''' Decodage de l'identifiant unique'''
        mon_id = int(identifiant, 0)
        self.identifiant = identifiant
        self.vul = Vulnerabilite(mon_id % 4)
        mon_id //= 4
        self.donneur = Position(mon_id % 4)
        mon_id //= 4
        self.attributions = [0]*52
        for i in range(52):
            self.attributions[i] = (mon_id % 4)
            mon_id //= 4
        # self.attributions[0]=(mon_id%4)
        self.attributions.reverse()
        self._verification()
        self._decode()

    def _verification(self):
        ''' vérification de l'intégrité d'une donne '''
        compteur = [0, 0, 0, 0]
        for i in range(52):
            compteur[self.attributions[i]] += 1
        for i in range(4):
            if compteur[i] != 13:
                raise NameError('Une des mains ne comporte pas 13 cartes')

    def affiche(self):
        print(f' Donneur : {self.donneur.name()}   Vulnérabilité : {self.vul.name()}')
        print('                Nord')
        self.nord.affiche(15)
        print('Ouest                         Est')
        self.ouest.affiche(10, self.est)
        print('                Sud')
        self.sud.affiche(15)


class Filtre:
    ''' Filtres correspondant à des enchères classiques. Les filtres sont
    volontairement plus vastes que les critères habituels des bridgeurs
    de façon à correspondre à des styles différents'''

    def __init__(self, name,
                 pointH_min=0,
                 pointH_max=40,
                 trefle_min=0,
                 trefle_max=13,
                 carreau_min=0,
                 carreau_max=13,
                 coeur_min=0,
                 coeur_max=13,
                 pique_min=0,
                 pique_max=13,
                 trefle_qualite=0,
                 carreau_qualite=0,
                 coeur_qualite=0,
                 pique_qualite=0,
                 points_totaux_min=0,
                 points_totaux_max=58):
        self.name = name
        self.pointH_min = pointH_min
        self.pointH_max = pointH_max
        self.trefle_min = trefle_min
        self.trefle_max = trefle_max
        self.carreau_min = carreau_min
        self.carreau_max = carreau_max
        self.coeur_min = coeur_min
        self.coeur_max = coeur_max
        self.pique_min = pique_min
        self.pique_max = pique_max
        self.trefle_qualite = trefle_qualite
        self.carreau_qualite = carreau_qualite
        self.coeur_qualite = coeur_qualite
        self.pique_qualite = pique_qualite
        self.points_totaux_min = points_totaux_min
        self.points_totaux_max = points_totaux_max

    def __getattr__(self, nom):
        if nom == "min":
            return [self.trefle_min,
                    self.carreau_min,
                    self.coeur_min,
                    self.pique_min]
        if nom == "max":
            return [self.trefle_max,
                    self.carreau_max,
                    self.coeur_max,
                    self.pique_max]
        raise AttributeError()              # workaround for pickle

    def __repr__(self):
        return self.name

    def filtre(self, main):
        ''' Renvoie True si la main considérée correspond au filtre désirée,
        c'est à dire est proche d'une enchère classique'''
        valeurs = main.vertues()
        if self.pointH_min > valeurs[0]:
            # print(1)
            return False
        if self.pointH_max < valeurs[0]:
            # print(2)
            return False
        if self.trefle_min > valeurs[1]:
            # print(3)
            return False
        if self.trefle_max < valeurs[1]:
            # print(4)
            return False
        if self.carreau_min > valeurs[2]:
            # print(5)
            return False
        if self.carreau_max < valeurs[2]:
            # print(6)
            return False
        if self.coeur_min > valeurs[3]:
            # print(7)
            return False
        if self.coeur_max < valeurs[3]:
            # print(8)
            return False
        if self.pique_min > valeurs[4]:
            # print(9)
            return False
        if self.pique_max < valeurs[4]:
            # print(10)
            return False
        if self.trefle_qualite > valeurs[5]:
            # print(11)
            return False
        if self.carreau_qualite > valeurs[6]:
            # print(12)
            return False
        if self.coeur_qualite > valeurs[7]:
            # print(13)
            return False
        if self.pique_qualite > valeurs[8]:
            # print(14)
            return False
        if self.points_totaux_min > valeurs[0]+valeurs[9]:
            # print(15)
            return False
        if self.points_totaux_max < valeurs[0]+valeurs[9]:
            # print(16)
            return False
        return True

    def controle_couleurs(self):
        ''' Ajuste le filtre pour que les critères de distribution
        soient cohérents. En cas de problème, renvoie une chaîne de caractère
        indiquant la nature du problème'''
        if self.trefle_min + self.carreau_min + \
           self.coeur_min + self.pique_min > 13:
            return "Trop de cartes par couleur"
        else:
            trefle_test = 13
            carreau_test = 13
            coeur_test = 13
            pique_test = 13

            trefle_test -= self.pique_min
            carreau_test -= self.pique_min
            coeur_test -= self.pique_min

            trefle_test -= self.coeur_min
            carreau_test -= self.coeur_min
            pique_test -= self.coeur_min

            trefle_test -= self.carreau_min
            coeur_test -= self.carreau_min
            pique_test -= self.carreau_min

            carreau_test -= self.trefle_min
            coeur_test -= self.trefle_min
            pique_test -= self.trefle_min

            self.trefle_max = min(self.trefle_max, trefle_test, 11)
            self.carreau_max = min(self.carreau_max, carreau_test, 11)
            self.coeur_max = min(self.coeur_max, coeur_test, 11)
            self.pique_max = min(self.pique_max, pique_test, 11)
            # On interdit qu'une main puisse avoir plus de 11 cartes de la
            # même couleur car cela n'est JAMAIS arrivé.

        if self.trefle_max + self.carreau_max + \
                self.coeur_max + self.pique_max < 13:
            return "Pas assez de cartes par couleur"

    def controle_HLD(self):
        ''' Ajuste le filtre pour que les critères de points
        soient cohérents. En cas de problème, renvoie une chaîne de caractère
        indiquant la nature du problème'''
        def inf(courte, longue):
            ''' Valeur minimum de la distribution 
            courte : nombre minimum de carte
            longue : nombre macximum de cartes'''
            return max(0, courte-4, 3-longue)

        def sup(courte, longue):
            return max(longue-4, 3-courte)
        paires = ([self.trefle_min, self.trefle_max],
                  [self.carreau_min, self.carreau_max],
                  [self.coeur_min, self.coeur_max],
                  [self.pique_min, self.pique_max]
                  )
        inf_LD = sum(inf(*arg) for arg in paires)
        max_LD = sum(sup(*arg) for arg in paires)
        self.points_totaux_min = max(self.points_totaux_min,
                                     self.pointH_min + inf_LD)
        self.pointH_max = min(self.points_totaux_max - inf_LD,
                              self.pointH_max)
        if self.points_totaux_min > self.points_totaux_max:
            return "Incohérence entre Points H et points HLD"
        if self.pointH_min > self.pointH_max:
            return "Incohérence entre Points H et points HLD"
        self.pointH_min = max(self.pointH_min,
                              self.points_totaux_min - max_LD)
        self.points_totaux_max = min(self.points_totaux_max,
                                     self.pointH_max + max_LD)


class NulFiltre(Filtre):
    ''' Un Filtre qui laisse tout passer '''

    def __init__(self):
        ''' On interdit les paramètres'''
        Filtre.__init__(self, '_Null')

    def filtre(self, main):
        return True


class ErreurDeContrainte(Exception):
    ''' Difficulté de gestion des maximums par Couleur '''
    pass


class Quatuor:
    ''' Un filtre par position '''

    def __init__(self, filtres):
        self.filtres = filtres

    def __repr__(self):
        return repr(self.filtres)

    def is_valide(self):
        ''' 
        Contrôle de compatibilité entre les 4 filtres du quatuor.
        Optimisation de quelques paramètres dans le cas où les
        contrôles sont validés
        '''

        def controle(self, variablemin, variablemax, total):
            somme = sum(getattr(fil, variablemin) for fil in self.filtres)
            if somme > total:
                return True
            for fil in self.filtres:
                setattr(fil,
                        variablemax,
                        min(getattr(fil, variablemax),
                            total - somme + getattr(fil, variablemin)
                            )
                        )

            somme = sum(getattr(fil, variablemax) for fil in self.filtres)
            if somme < total:
                return True
            for fil in self.filtres:
                setattr(fil,
                        variablemin,
                        max(getattr(fil, variablemin),
                            total - somme + getattr(fil, variablemax)
                            )
                        )

        if controle(self, 'pointH_min', "pointH_max", 40):
            return False
        if controle(self, 'trefle_min', "trefle_max", 13):
            return False
        if controle(self, 'carreau_min', "carreau_max", 13):
            return False
        if controle(self, 'coeur_min', "coeur_max", 13):
            return False
        if controle(self, 'pique_min', "pique_max", 13):
            return False

        return True

    def distribue(self):
        ''' 
        Distribution d'une donne en fonction des filttres du Quatuor 
        '''
        def ventile(a, liste, correctif):
            '''
            a : nombre de position à ventiler
            liste = [x, y, z, t]
            Renvoie une liste
            [ax, ay, az, at] de sorte que
            ax <= x, ay <= y, az <= z, at <= t  ET ax+ay+az+at =a
            de façon plus ou moins équirépartie en tenant compte de correctif.
            Le correctif permet d'éviter que le résultat soit trop biaisé
            mais ne garanti pas une équité théorique correcte.
            '''
            if DEBUG:
                print('ventile')
                print(a, liste)
            ventilation = [0, 0, 0, 0]
            for i in range(a):
                x, y, z, t = liste
                a, b, c, d = correctif
                probas = [x * (13 - a)/(1+a),
                          y * (13 - b)/(1+b),
                          z * (13 - c)/(1+c),
                          t * (13 - d)/(1+d)
                          ]
                if sum(probas) == 0:
                    raise ErreurDeContrainte
                probas = [t / sum(probas) for t in probas]
                pos = choice(4, p=probas)
                ventilation[pos] += 1
                correctif[pos] += 1
                liste[pos] -= 1
            if DEBUG:
                print("ventilation", ventilation)
            return(ventilation)

        if DEBUG:
            print("Préparez le paracétamol")
        repartition = [[[] for col in Couleur] for pos in Position]
        # Les mains à remplir
        reservations = [fil.min for fil in self.filtres]
        # Les places résercées par couleur
        facultatif = [[fil.max[col]-fil.min[col] for fil in self.filtres]
                      for col in Couleur]
        # Les places libres par couleur
        free = [13 - sum(fil.min) for fil in self.filtres]
        # Les places restantes par position

        for col in Couleur:
            # On commencve par remplir les places réservées
            if DEBUG:
                print('repartition', repartition)
                print('reservation', reservations)
                print('facultatif', [[facultatif[p][c]
                                      for p in Couleur] for c in Position])
                print('free', free)
            cartes = list(range(13))
            shuffle(cartes)
            for pos in Position:
                for i in range(reservations[pos][col]):
                    repartition[pos][col].append(cartes.pop())
            # On ventile les places restantes
            reste = len(cartes)
            # On ajuste les probabilités pour une répartition correcte
            correctif = [reservations[pos][col] for pos in Position]
            liste = list(facultatif[col])
            ventilation = ventile(reste, liste, correctif)
            for pos in Position:
                for i in range(ventilation[pos]):
                    repartition[pos][col].append(cartes.pop())
                free[pos] -= ventilation[pos]
            for c in range(col+1, 4):
                for pos in Position:
                    facultatif[c][pos] = min(facultatif[c][pos], free[pos])

        donne = Donne(nord=repartition[0],
                      sud=repartition[1],
                      est=repartition[2],
                      ouest=repartition[3]
                      )
        return donne

    def affiche(self):
        attributs = ["pointH_min",
                     "pointH_max",
                     "trefle_min",
                     "trefle_max",
                     "carreau_min",
                     "carreau_max",
                     "coeur_min",
                     "coeur_max",
                     "pique_min",
                     "pique_max"
                     ]
        for position in Position:
            print('position : ', position.name())
            for att in attributs:
                print(att, ' : ', getattr(self.filtres[position], att))


class InvalidSequence(Exception):
    ''' Séquence invalide '''
    pass


class Sequence:
    ''' 
    Séquence de filtres pour une Donne. 
    Correspond à une séquence d'enchères 
    '''

    def __init__(self):
        self.positif = [[] for positionn in Position]
        self.negatif = [[] for positionn in Position]
        self.name = ''

    def __repr__(self):
        return self.name

    def set_filtre(self, position, filtre, normal=True):
        if normal:
            self.positif[position].append(filtre)
        else:
            self.negatif[position].append(filtre)

    def set_name(self, name):
        self.name = name

    def explode(self):
        ''' Transforme la séquence en liste de Quatuor'''
        def nullify(liste_de_filtres):
            if liste_de_filtres:
                return liste_de_filtres
            else:
                null = NulFiltre()
                return [null]
        goodlistes = map(nullify, self.positif)
        quatuors = [Quatuor(x) for x in product(*goodlistes)]
        return [x for x in quatuors if x.is_valide()]

    def is_invalide(self):
        return not (self.explode())

    def distribue(self):
        quatuors = self.explode()
        if quatuors:
            choix = randint(1, len(quatuors))
            test = False
            compteur = 0
            overflow = 50_000
            while not test:
                compteur += 1
                if compteur > overflow:
                    raise InvalidSequence
                try:
                    tentative = quatuors[choix-1].distribue()
                    test = self.filtre(tentative)
                except ErreurDeContrainte:
                    pass

            return tentative
        else:
            raise InvalidSequence

    def filtre(self, donne):
        ''' Appliacation des filtres à une donne, 
        Renvoie True si la donne satisfait tous les filtres
        de la séquence 
        Les filtres sont liées entre eux par le connecteur logique OU :
            Il suffit que l'ub d'entre eux soit satisfait
        Les filtres sont liées entre eux par le connecteur logique ET :
            Il faut qu'aucun d'entre eux ne soit satisfait
        '''

        for position in Position:
            for fil in self.negatif[position]:
                if fil.filtre(donne[position]):
                    return False

        for position in Position:
            if self.positif[position]:
                position_valide = False
                for fil in self.positif[position]:
                    if fil.filtre(donne[position]):
                        position_valide = True
                if not position_valide:
                    return False
        return True


#Filtres = Sequence

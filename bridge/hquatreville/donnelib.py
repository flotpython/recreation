#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 18:39:51 2018

Cette bibliothèque défini deux classes.

--> Mains_active :
    Classe permettant d'afficher une Mais de bridge dans un frame tk.
    L'initialisation de la classe lie une Main avec le Frame
    Les méthodes associées à cette classe sont :
        -> affiche()         Rend visible la Main dans le Frame   
        -> efface()          Rend invisible la Main dans le Frame  
        -> commute()         Passe de visible à invisible ou vice-versa   
        -> reconfigure(main) associe une nouvelle Main au Frame
        
--> Donne_active :
    Classe permettant d'afficher une Donne de Bridge dans un Frame tk  
    L'initialisation de la classe lie une Main avec le Frame
    activedonne = Donne_active(donne, Frame)  sans option OU
    activedonne = Donne_active(donne, Frame, [bool1,bool2,bool3,bool4])
    où bool1, bool2, bool3 et bool4 sont des booléens indiquant si on 
    souhaite ou non afficher immédiatement les mains respectives de
    Notd, Sud, Est et Ouest
    On dispose sur cette clase des méthodes suivantes :
        -> affiche_info()
        Affiche les informations de donneur au centre du diagramme
        les couleurs de la vulnérabilité sont provisoirement définies 
        par la fonction couleurDePosition de la bibliothèque bridgelib
        -> affiche() 
        Affiche les mains dont l'attibut de visibilité est True
        -> rend_visible(position) 
        Rend visible la main de la position indiquée
        (Ne gère pas son affichage immédiat, utiliser affiche())
        -> rend_invisible(position)
        Rend invisible la main de la position indiquée
        (Ne gère pas son effacement immédiat, utiliser affiche())
        -> commute(position) ou commute(position, False)
        Passe la main indiquée de l'état visible à invisible ou vice-versa,
        gère l'affichage sauf si l'option de mise à jour est indiquée comme 
        False
        -> distribue() ou distribue(False)
        Modifie la donne en la distribuant aléatoirement et l'affiche
        (sauf si l'option de mise à jour False est indiquée)
        -> reconfigure(donne) ou reconfigure(donne, False)
        Modifie la donne en fonction de l'argument et l'affiche
        (sauf si l'option de mise à jour False est indiquée)
        -> etat()
        Récupère un tableau de 4 booléens donnant l'état de visibilité des
        quatre positions
        
@author: hubert
"""

from bridgelib import Donne, Couleur, Position
import tkinter as tk
import tkinter.font as tkf
from tklib import clear, couleurDePosition

DEBUG = False

class Main_active():
    '''  Classe permettant d'afficher une Mais de bridge dans un frame tk.
    L'initialisation de la classe lie une Main avec le Frame
    Les méthodes associées à cette classe sont :
        -> affiche()         Rend visible la Main dans le Frame   
        -> efface()          Rend visible la Main dans le Frame   
        -> commute()         Passe de visible à invisible ou vice-versa   
        -> reconfigure(main) Associe une nouvelle Main au Frame
    '''

    def __init__(self, main, frame):
        self.main = main
        self.visible = False
        self.frame = frame

    def affiche(self):
        '''
        Rend visible la Main dans le Frame 
        '''
        self.visible = True
        for couleur in Couleur:
            symbole1 = tk.Label(self.frame,
                                text=couleur.nbglyph(),
                                fg=couleur.teinte())
            symbole1.grid(column=0, row=3-couleur)
            texte = tk.Label(self.frame, text=str(self.main[couleur]))
            texte.grid(column=1, row=3-couleur, sticky="w")

    def efface(self):
        '''
        Rend visible la Main dans le Frame 
        '''
        self.visible = False
        clear(self.frame)

    def commute(self):
        '''
        Passe de visible à invisible ou vice-versa
        '''
        if self.visible:
            self.efface()
        else:
            self.affiche()

    def reconfigure(self, main):
        '''
        Associe une nouvelle Main au Frame
        '''
        self.main = main
        if self.visible:
            self.efface()
            self.affiche()


class Donne_active:
    ''' Classe permettant d'afficher une Donne de Bridge dans un Frame tk  
    L'initialisation de la classe lie une Main avec le Frame
    activedonne = Donne_active(donne, Frame)  sans option OU
    activedonne = Donne_active(donne, Frame, [bool1,bool2,bool3,bool4])
    où bool1, bool2, bool3 et bool4 sont des booléens indiquant si on 
    souhaite ou non afficher immédiatement les mains respectives de
    Notd, Sud, Est et Ouest
    On dispose sur cette clase des méthodes suivantes :
        -> affiche_info()
        Affiche les informations de donneur au centre du diagramme
        les couleurs de la vulnérabilité sont provisoirement définies 
        par la fonction couleurDePosition de la bibliothèque bridgelib
        -> affiche() 
        Affiche les mains dont l'attibut de visibilité est True
        -> rend_visible(position) 
        Rend visible la main de la position indiquée
        (Ne gère pas son affichage immédiat, utiliser affiche())
        -> rend_invisible(position)
        Rend invisible la main de la position indiquée
        (Ne gère pas son effacement immédiat, utiliser affiche())
        -> commute(position) ou commute(position, False)
        Passe la main indiquée de l'état visible à invisible ou vice-versa,
        gère l'affichage sauf si l'option de mise à jour est indiquée comme 
        False
        -> distribue() ou distribue(False)
        Modifie la donne en la distribuant aléatoirement et l'affiche
        (sauf si l'option de mise à jour False est indiquée)
        -> reconfigure(donne) ou reconfigure(donne, False)
        Modifie la donne en fonction de l'argument et l'affiche
        (sauf si l'option de mise à jour False est indiquée)
        -> etat()
        Récupère un tableau de 4 booléens donnant l'état de visibilité des
        quatre positions 
        '''
        
    geometrie = {Position.NORD: [0, 1],
                 Position.SUD: [2, 1],
                 Position.EST: [1, 2],
                 Position.OUEST: [1, 0]}

    def __init__(self, donne, frame, visible=[True for pos in Position]) :
        ''' donne = la donne à afficher
            frame = le cadre dans lequel on affiche la donne
            visible = un tableau de 4 booléens indiquant les mains à afficher
            TRUE  = on affiche la main
            FALSE = la main est invisible 
        '''

        self.frame = frame
        self.visible = visible
        self.vul = donne.vul
        self.donneur = donne.donneur
        self.mains = []
        for position in Position:
            cadre = tk.Frame(frame)
            cadre.grid(row=Donne_active.geometrie[position][0],
                       column=Donne_active.geometrie[position][1])
            self.mains.append(Main_active(donne[position], cadre))
        frame.columnconfigure(0, minsize=130)
        frame.columnconfigure(1, minsize=130)
        frame.columnconfigure(2, minsize=130)
        frame.rowconfigure(0, minsize=100)
        frame.rowconfigure(1, minsize=100)
        frame.rowconfigure(2, minsize=100)

    def affiche_info(self):
        '''
        Affiche les informations de donneur au centre du diagramme
        les couleurs de la vulnérabilité sont provisoirement définies 
        par la fonction couleurDePosition de la bibliothèque bridgelib
        '''
        fenetre_info = tk.Frame(self.frame,
                                relief="groove",
                                borderwidth=3)
        fenetre_info.grid(row=1, column=1)
        for position in Position:
            label = tk.Label(fenetre_info,
                             text=position.name()[0],
                             bg=couleurDePosition(self.vul, position),
                             relief="raised", borderwidth=2)
            label.grid(row=Donne_active.geometrie[position][0],
                       column=Donne_active.geometrie[position][1])
            if position == self.donneur:
                f = tkf.Font(label, label.cget("font"))
                f. configure(weight="bold")
                f.configure(underline=True)
                f. configure(size=14)
                label.configure(font=f)
            else:
                f = tkf.Font(label, label.cget("font"))
                f. configure(size=14)
                label.configure(font=f)

    def affiche(self):
        '''
         Affiche les mains dont l'attibut de visibilité est True
         '''
        if DEBUG :
            print("Affiche Donne_active ")
        for position in Position:
            self.mains[position].efface()
            if self.visible[position]:
                self.mains[position].affiche()
        self.affiche_info()

    def rend_visible(self, position) :
        '''
        Rend visible la main de la position indiquée
        (Ne gère pas son affichage immédiat, utiliser affiche())
        '''
        print('rv')
        self.visible[position] = True

    def rend_invisible(self, position) :
        '''
        Rend invisible la main de la position indiquée
        (Ne gère pas son effacement immédiat, utiliser affiche())
        '''
        print('ri')
        self.visible[position] = False

    def commute(self, position, mise_a_jour=True):
        '''
        commute(position),  commute(position, True) ou commute(position, False)
        Passe la main indiquée de l'état visible à invisible ou vice-versa,
        gère l'affichage sauf si l'option de mise à jour est indiquée comme 
        False
        '''
        self.visible[position] = not(self.visible[position])
        if mise_a_jour:
            self.mains[position].efface()
            if self.visible[position]:
                self.mains[position].affiche()

    def distribue(self, mise_a_jour=True) :
        '''
        distribue(), distribue(True) ou distribue(False)
        Modifie la donne en la distribuant aléatoirement et l'affiche
        (sauf si l'option de mise à jour False est indiquée)
        '''
        donne = Donne()
        self.vul, self.donneur = donne.vul, donne.donneur
        for position in Position:
            self.mains[position].main = donne[position]
        if mise_a_jour:
            self.affiche()
    
    def reconfigure(self, donne, mise_a_jour=True) :
        '''
        reconfigure(donne), reconfigure(donne,True) ou 
        reconfigure(donne, False)
        Modifie la donne en fonction de l'argument et l'affiche
        (sauf si l'option de mise à jour False est indiquée)
        '''
        self.vul, self.donneur = donne.vul, donne.donneur
        for position in Position:
            self.mains[position].main = donne[position]
        if mise_a_jour:
            self.affiche()        

    def etat(self):
        '''
        Récupère un tableau de 4 booléens donnant l'état de visibilité des
        quatre positions 
        '''
        return self.visible




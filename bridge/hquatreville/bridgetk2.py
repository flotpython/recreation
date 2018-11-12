#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 18:39:51 2018

@author: hubert
"""
from bridgelib import Main, Donne, Couleur, Position
import tkinter as tk

####        I/O          ####
####        TODO         ####


####   AFFICHAGE D'UNE DONNE   

def clear(frame):
    for i in frame.grid_slaves():
        i.destroy()


class Main_active():
    ''' Classe pour afficher les mains  dans un cadre tkinter'''
    def __init__(self,main,frame):
        self.main     = main
        self.visible  = False
        self.frame    = frame


        
    def affiche(self) :
        self.visible = True
        for couleur in Couleur :
            symbole1 = tk.Label(self.frame, 
                               text=couleur.nbglyph(), 
                               fg=couleur.teinte())
            symbole1.grid(column=0, row=3-couleur)
            texte = tk.Label(self.frame, text=str(self.main[couleur]))
            texte.grid(column=1, row=3-couleur, sticky="w")
        
    def efface(self)  :
        self.visible = False
        clear(self.frame)
        
    def commute(self) :
        if self.visible :
            self.efface()
        else :
            self.affiche()
            
    def reconfigure(self,main) :
        self.main = main
        if self.visible :
            self.efface()
            self.affiche()

class Donne_active:
    ''' Classe pour afficher un diagramme dans un cadre tkinter '''
    geometrie = {Position.NORD  : [0,1],
                 Position.SUD   : [2,1],
                 Position.EST   : [1,2],
                 Position.OUEST : [1,0]}
    
    def __init__(self, donne, frame, visible = [True for pos in Position]):
        ''' donne = la donne à afficher
            frame = le cadre dans lequel on affiche la donne
            visible = un tableau de 4 booléens indiquant les mains à afficher
            TRUE  = on affiche la main
            FALSE = la main est invisible '''
            
        self.frame   = frame
        self.visible = visible
        print(self.visible)
        self.vul     = donne.vul
        self.donneur = donne.donneur
        self.mains = []
        for position in Position :
            cadre = tk.Frame(frame)
            cadre.grid (row    = Donne_active.geometrie[position][0],
                        column = Donne_active.geometrie[position][1],
                        sticky =" w")
            self.mains.append (Main_active(donne[position],cadre))
        frame.columnconfigure(0,minsize=130)
        frame.columnconfigure(1,minsize=130)
        frame.columnconfigure(2,minsize=130)    
                        
        
    def affiche(self):
        for position in Position :
            self.mains [position].efface()
            if self.visible[position] :
                self.mains [position].affiche()
                                       
    def rend_visible(self,position):
        print('rv')
        self.visible[position] = True
        
    def rend_invisible(self,position):
        print('ri')
        self.visible[position] = False  
        
    def commute(self,position,mise_a_jour = True):
        print('com',position)
        self.visible[position] = not(self.visible[position])
        if mise_a_jour:
            self.mains [position].efface()
            if self.visible[position] :
                self.mains [position].affiche()
            
        
    def distribue(self, mise_a_jour = True):
        print('ditrib')
        donne = Donne()
        for position in Position :
            self.mains[position].main = donne[position]
        if mise_a_jour :
            self.affiche()        
            
    def etat(self):
        print(self.visible)
        return self.visible
        
        
           
def barre_de_menu(liste, menu): 
    ''' associe une liste de boutons à une liste de commandes
    les items de la liste sont des couples de la forme
    [nom du bouton, commande à exécuter]'''
    clear(menu)
    for commande in liste :
        bouton = tk.Button(menu, 
                           text = commande[0], 
                           command = commande[1], 
                           width=8 )
        bouton.grid(sticky="w")
        
def barre_de_message(message, messager):
    clear(messager)
    mess = tk.Label(messager, text = message)
    mess.grid()
         
       
        
#########################################################################   
####        DEBUT DU PROGRAMME     
####        Interface    ####

root=tk.Tk()
root.title('Utilitaire pour bridgeur')

menu   = tk.Frame(root)
menu.grid(row=0, column=0,sticky='n')
root.columnconfigure(0,weight=1)        

fenetre = tk.Frame(root)
fenetre.grid(row=0, column=1)
root.columnconfigure(1,weight=3)

messager = tk.Frame(root)
messager.grid(row=1, columnspan=2) 
mess = tk.Label(messager, text = "Démarrage")
mess.grid(sticky='ew')


####       Initialisation   ####       

donne= Donne()
active = Donne_active(donne, fenetre)
active.affiche()
compteur = 1
barre_de_message(f"Donne {compteur}", messager)

#####           MENU      #####
print("menu")
def c_nord():
    active.commute(Position.NORD)
    
def c_sud():
    active.commute(Position.SUD)

def c_est():
    active.commute(Position.EST)

def c_ouest():    
    active.commute(Position.OUEST)
    
def c_distribue():
    global compteur
    active.distribue()
    barre_de_message(f"Donne {compteur}", messager)
    compteur += 1

liste_menu = [['Nord', c_nord],
              ['Sud', c_sud],
              ['Est', c_est],
              ['Ouest', c_ouest],
              ['Donne', c_distribue],
              ['Etat', active.etat],
              ['Quit', root.quit]]


barre_de_menu(liste_menu,menu)


#####      MAINLOOP      ######
print('boucle')
root.mainloop()
root.destroy()
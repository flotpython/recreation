#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 18:39:51 2018

@author: hubert
"""
import bridgelib as bl
import tkinter as tk

####        I/O          ####

####     COMMANDES       ####
NORD = 0
SUD = 1
EST = 2
OUEST = 3

def clear(frame):
    for i in frame.grid_slaves():
        i.destroy()

####  Main active        #### 
class Main_active():
    ''' Classe pour afficher les mains  '''
    def __init__(self,main,frame):
        self.main     = main
        self.visible  = False
        self.frame    = frame
        
    def affiche(self) :
        self.visible = True
        affiche_main(self.main,self.frame)
        
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

def affiche_main(main,frame):
    symbole1 = tk.Label(frame, text=bl.Couleur.PIQUE.nbglyph(),
                        fg=bl.Couleur.PIQUE.teinte())   
    symbole1.grid(column=0, row=0)
    texte1 = tk.Label(frame, text=str(main.pique))
    texte1.grid(column=1, row=0, sticky="w")
    symbole2 = tk.Label(frame, text=bl.Couleur.COEUR.nbglyph(),
                        fg=bl.Couleur.COEUR.teinte())   
    symbole2.grid(column=0, row=1)
    texte2 = tk.Label(frame, text=str(main.coeur))
    texte2.grid(column=1, row=1, sticky="w")
    symbole3 = tk.Label(frame, text=bl.Couleur.CARREAU.nbglyph(),
                        fg=bl.Couleur.CARREAU.teinte())   
    symbole3.grid(column=0, row=2)
    texte3 = tk.Label(frame, text=str(main.carreau))
    texte3.grid(column=1, row=2, sticky="w")
    symbole4 = tk.Label(frame, text=bl.Couleur.TREFLE.nbglyph(),
                        fg=bl.Couleur.TREFLE.teinte())   
    symbole4.grid(column=0, row=3)
    texte4 = tk.Label(frame,text=str(main.trefle))
    texte4.grid(column=1, row=3, sticky="w")
    
def commute_nord():
    mains_actives[NORD].commute()   
    
def commute_sud():
    mains_actives[SUD].commute()   

def commute_est():
    mains_actives[EST].commute()   

def commute_ouest():
    mains_actives[OUEST].commute()   

####   Donne active     ####
def initialise():
    global donne_active,mains_actives   
    donne_active=bl.Donne()
    mains_actives = [Main_active(donne_active.nord,main_de_nord),
                     Main_active(donne_active.sud,main_de_sud),
                     Main_active(donne_active.est,main_de_est),
                     Main_active(donne_active.ouest,main_de_ouest)]        



def distribue() :       
    global donne_active,mains_actives   
    donne_active=bl.Donne()
    mains_actives[NORD].reconfigure(donne_active.nord)
    mains_actives[SUD].reconfigure(donne_active.sud) 
    mains_actives[EST].reconfigure(donne_active.est)
    mains_actives[OUEST].reconfigure(donne_active.ouest) 

####        Interface    ####

root=tk.Tk()
root.title('Utilitaire pour bridgeur')

menu   = tk.Frame(root)
menu.grid(row=0, column=0,sticky='n')
root.columnconfigure(0,weight=1)

fenetre = tk.Frame(root)
fenetre.grid(row=0, column=1)
root.columnconfigure(1,weight=3)

#####           MENU      #####
#message = tk.Label(menu, text='Menu', width=6)
#message.grid(sticky="w")

bouton_nord = tk.Button(menu, text='Nord', command=commute_nord, width=6)
bouton_nord.grid(sticky="w")

bouton_sud = tk.Button(menu, text='Sud', command=commute_sud, width=6)
bouton_sud.grid(sticky="w")

bouton_est = tk.Button(menu, text='Est', command=commute_est, width=6)
bouton_est.grid(sticky="w")

bouton_ouest = tk.Button(menu, text='Ouest', command=commute_ouest, width=6)
bouton_ouest.grid(sticky="w")

bouton_distribue = tk.Button(menu, text='Donne', 
                             command=distribue, width=6)
bouton_distribue.grid(sticky="w")

#####      AFFICHAGE       ######
fenetre.columnconfigure(0,minsize=150)
fenetre.columnconfigure(1,minsize=150)
fenetre.columnconfigure(2,minsize=150)
fenetre.rowconfigure(0,minsize=60)
fenetre.rowconfigure(1,minsize=60)
fenetre.rowconfigure(2,minsize=60)

message1 = tk.Label(fenetre, text='Bienvenu')
message1.grid(row=3, column=1)
main_de_nord = tk.Frame(fenetre)
main_de_nord.grid(row=0, column=1,sticky="w")
main_de_sud = tk.Frame(fenetre)
main_de_sud.grid(row=2, column=1,sticky="w")
main_de_ouest = tk.Frame(fenetre)
main_de_ouest.grid(row=1,column=0,sticky="w")
main_de_est = tk.Frame(fenetre)
main_de_est.grid(row=1,column=2,sticky="w")

mains = [main_de_nord, main_de_sud, main_de_est, main_de_ouest]

initialise()
root.mainloop()
root.destroy()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:36:24 2018

@author: hubert
"""

from bridgelib import Donne
import pickle
import tkinter as tk
from tkinter.filedialog import askopenfilename


def clear(frame):
    for i in frame.grid_slaves():
        i.destroy()
        
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
         

def readfiltres():
    filename='data/filtres.fil'
    with open(filename,"rb") as fichier :
        return pickle.load(fichier) 
    
def writefiltre(filtres) :
    filename='data/filtres.fil'
    with open(filename,"wb") as fichier :
        pickle.dump(filtres,fichier)
    
    
   
###################################################        


root=tk.Tk()
root.title('IOtest')


menu   = tk.Frame(root)
menu.grid(row=0, column=0, sticky='n')
root.columnconfigure(0, weight=1)        

fenetre = tk.Frame(root, width = 200, height = 50)
fenetre.grid(row=0, column=1)
root.columnconfigure(1, weight=3)

messager = tk.Frame(root)
messager.grid(row=1, columnspan=2) 
mess = tk.Label(messager, text = "Démarrage")
mess.grid(sticky='ew')


###################################################
DONNETYPE = ("Pack de donne",".pak") 
donnename = tk.StringVar(root)
pack = []

def set_donnename():
    donnename.set(askopenfilename(filetypes = [DONNETYPE],
                                  initialdir = 'data/'))
 
       
def c_donner():
    print("donner")
    global pack
    pack = [Donne().identifiant() for i in range(10)]
    print(pack)
    
def c_charge_donnes():
    print("charger")
    global pack
    donnename.set(askopenfilename(filetypes = [DONNETYPE],
                                  initialdir = 'data/'))
    filename = donnename.get()
    print(filename)
    with open(filename,"rb") as fichier :
        pack = pickle.load(fichier)
        print(pack)
        
    
    
def c_sauve_donnes(): 
    print("sauver")
    var = tk.StringVar(fenetre)
    def validate(event):
        text = var.get()
        try :
            filename = "data/" + text + ".pak"
            with open(filename,"wb") as fichier:
                pickle.dump(pack, fichier)
            wlabel.destroy()
            wentree.destroy()  
            barre_de_message(f"Fichier {filename[5:]} savegardé", messager)
        except IOError:
            barre_de_message("Problème d'entrée/sortie", messager)
    wlabel  = tk.Label(fenetre, text = "Nom du fichier")
    wlabel.grid()    
    wentree = tk.Entry(fenetre, textvariable = var)
    wentree.grid()
    wentree.bind('<Return>', validate)
    

liste_menu = [['Donner', c_donner],
              ['Charger', c_charge_donnes],
              ['Sauver', c_sauve_donnes]]    


barre_de_menu(liste_menu, menu)      
barre_de_message("Test IO", messager)  
########################################################


root.mainloop()


    

       
    
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 17:57:57 2018

@author: hubert
"""

import tkinter as tk
from bridgelib import Filtre, Filtres, Position
import pickle
from tkinter.messagebox import askyesno

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
                           width=16 )
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
    
         
       
        
#########################################################################   
####        DEBUT DU PROGRAMME     
####        Interface    ####

root=tk.Tk()
root.title('Utilitaire pour bridgeur')

menu   = tk.Frame(root)
menu.grid(row=0, column=0, sticky='n')
root.columnconfigure(0,weight=1)        

fenetre = tk.Frame(root)
fenetre.grid(row=0, column=1, sticky='n')
root.columnconfigure(1,weight=3)

messager = tk.Frame(root)
messager.grid(row=1, columnspan=2) 
mess = tk.Label(messager, text = "Démarrage")
mess.grid(sticky='ew')

filtres = Filtres()
donnes  = []

''' filtres = les filtres à utiliser lors de la distribution des donnes 
    donnes  = les donnes à enchérir
Par défaut, ces variables globales sont vides 
'''    

####       Commandes   ####  
def c_selection():
    ''' 
    Sélectionne les filtres qui serviront à filtrer les donnes distribuées.
    '''
    global filtres
    
    def confirmer():
        clear(fenetre)
   
    def select_pos(position):
        print(position)
        nonlocal boutons
        c_selection.position = position
        affiche_filtre(position)
        b_positif.configure(state="normal")
        b_negatif.configure(state="normal")
        for pos in Position:
            if pos == position :
                boutons[pos].configure(relief = 'sunken') 
            else :    
                boutons[pos].configure(relief = 'raised')
        
    def callback(position):
        return lambda : select_pos(position)
    
    def sel_filtre():
        print('sel_filtre')
        def validate(event=None):
            print("validation")
            index_filtre = menu_deroulant.curselection()
            filtres.positif[c_selection.position] = [liste_des_filtres[i] \
                                                     for i in index_filtre]
            affiche_filtre(c_selection.position)
                
        clear(f_positif)
        defilement = tk.Scrollbar(f_positif, orient='vertical')                           
        defilement.grid(row=1, column=1, sticky='ns')
        noms_de_filtres = [f.name for f in liste_des_filtres]
        menu_deroulant = tk.Listbox(f_positif, yscrollcommand=defilement.set,
                                    height=9, selectmode='multiple')
        defilement.configure(command=menu_deroulant.yview)
        menu_deroulant.bind("<Return>", validate)
        menu_deroulant.grid(row=1, column=0)
        for nom in noms_de_filtres :
            menu_deroulant.insert(tk.END, nom)
        tk.Button(f_positif, text='Ok', command=validate).grid()   
        tk.Frame(f_positif,width=largeur).grid(columnspan=2)
            
    def sel_antifiltre():
        print('sel_antifiltre')
        def validate(event=None):
            print("validation")
            index_filtre = menu_deroulant.curselection()
            filtres.negatif[c_selection.position] = [liste_des_filtres[i] \
                                                     for i in index_filtre]
            affiche_filtre(c_selection.position)
                
        clear(f_negatif)
        defilement = tk.Scrollbar(f_negatif, orient='vertical')                           
        defilement.grid(row=1, column=1, sticky='ns')
        noms_de_filtres = [f.name for f in liste_des_filtres]
        menu_deroulant = tk.Listbox(f_negatif, yscrollcommand=defilement.set,
                                    height=9, selectmode='multiple')
        defilement.configure(command=menu_deroulant.yview)
        menu_deroulant.bind("<Return>", validate)
        menu_deroulant.grid(row=1, column=0)
        for nom in noms_de_filtres :
            menu_deroulant.insert(tk.END, nom)
        tk.Button(f_negatif, text='Ok', command=validate).grid()   
        tk.Frame(f_negatif,width=largeur).grid(columnspan=2)
        
    def affiche_filtre(pos):
        messages = ['Filtre de Nord', 'Filtre de Sud',
                    "Filtre d'Est", "Filtre d'Ouest"]
        negsages = ['Interdit de Nord', 'Interdit de Sud',
                    "Interdit d'Est", "Interdit d'Ouest"]
        b_positif.configure(text=messages[c_selection.position])
        b_negatif.configure(text=negsages[c_selection.position])
        clear(f_positif)
        clear(f_negatif)
        for filtre in filtres.positif[c_selection.position] :
            tk.Label(f_positif, text=filtre.name).grid()
        tk.Frame(f_positif,width=largeur).grid()
        for filtre in filtres.negatif[c_selection.position] :
            tk.Label(f_negatif, text=filtre.name).grid() 
        tk.Frame(f_negatif,width=largeur).grid()    
        print('affiche sortie')    
            
    barre_de_message('Séquence de filtres', messager)        
    clear(fenetre)
    largeur=250
    tk.Label(fenetre, text='Main à filtrer').grid(row=0,columnspan=4)
    boutons = []
    for pos in Position:
        boutons.append(tk.Button(fenetre, command=callback(pos), 
                  text=pos.name()))
        boutons[pos].grid(row=1, column=int(pos), sticky='ew')
    b_positif = tk.Button(fenetre, text=f"Filtre à sélectionner",
              command=sel_filtre, state='disabled')
    b_positif.grid(row=2, columnspan=2, sticky='ew')
    b_negatif = tk.Button(fenetre, text=f"Filtres interdit",
              command=sel_antifiltre, state='disabled')
    b_negatif.grid(row=2, column=2, columnspan=2, sticky='ew')
    f_positif = tk.Frame(fenetre, height=250, width=largeur)
    f_positif.grid(row=3, columnspan=2)
    f_positif.grid_propagate(0)
    f_negatif = tk.Frame(fenetre, height=250, width=largeur)
    f_negatif.grid(row=3, column=2, columnspan=2)
    f_negatif.grid_propagate(0)
    confirmation = tk.Button(fenetre, text = 'Valider les filtres',
                             command=confirmer)
    confirmation.grid(row=4, columnspan=4)
    print('f_positif')
         

def c_distribuer():
    return None

def c_encherir():
    return None

def c_sauvegarder():
    return None

def c_charger():
    return None


filtre_menu = [[' Sélectionner séquence', c_selection],
               ['Distribuer',c_distribuer],
               ['Enchérir',c_encherir],
               ['Sauvegarder les donnes', c_sauvegarder],
               ['Charger des donnes', c_charger]]

barre_de_menu(filtre_menu, menu)


#####      MAINLOOP      ######
liste_des_filtres = readfiltres()

print('boucle')
root.mainloop()
root.destroy()     
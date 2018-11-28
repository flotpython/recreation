#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 17:57:57 2018

@author: hubert
"""

import tkinter as tk
from bridgelib import Position
#from tkinter.messagebox import askyesno
from tklib import clear, barre_de_message
from IOlib import readfiltres
import tkcolors as tc

DEBUG = False

####       Commandes   ####  
def regler_sequence(sequence, fenetre, messager):
    ''' 
    filtres  : séquence de filtres dans la classe Filtres
    fenetre  : fentre dans laquelle l'interface aparait
    messager : fennetre dans laquelle on envoie des messages d'état
    
    Le rôle de cette interface est d'effectuer les réglages de la séquence
    de filtres. Celle-ci est donc modifiée au cours de ces réglages.
    Le mot séquence fait référence à une éventuelle séquence d'enchères
    correspondant aux différents filtres utilisés.
    '''

    def select_pos(position):
        ''' Sélection de la Main à filtrer 
        La main active est sauvegarder dans la variable globale
        sequence.position
        '''
        sequence.position = position
        affiche_filtre(position)
        b_positif.configure(state="normal")
        b_negatif.configure(state="normal")
        for pos in Position:
            if pos == position :
                boutons[pos].configure(relief='sunken', bg=tc.THEME5) 
            else :    
                boutons[pos].configure(relief='raised', bg=tc.THEME4)
        
    def callback(position):
        ''' Artefact pour que la position soit choisie au moment
        de la création du bouton et pas au moment où il est activé.
        '''
        return lambda : select_pos(position)
    
    def sel_filtre():
        ''' Sélectionne un ou plusieurs filtres associée à
        la Main de la position active'''
        if DEBUG :
            print('sel_filtre')
        def validate(event=None):
            if DEBUG :
                print("validation")
            index_filtre = menu_deroulant.curselection()
            sequence.positif[sequence.position] = \
                                   [liste_des_filtres[i] for i in index_filtre]
            affiche_filtre(sequence.position)
                
        clear(f_positif)
        defilement = tk.Scrollbar(f_positif, orient='vertical')                           
        defilement.grid(row=1, column=1, sticky='ns')
        noms_de_filtres = [f.name for f in liste_des_filtres]
        menu_deroulant = tk.Listbox(f_positif, 
                                    yscrollcommand=defilement.set,
                                    height=9, 
                                    selectmode='multiple')
        defilement.configure(command=menu_deroulant.yview)
        menu_deroulant.bind("<Return>", validate)
        menu_deroulant.grid(row=1, column=0)
        for nom in noms_de_filtres :
            menu_deroulant.insert(tk.END, nom)
        tk.Button(f_positif, text='Ok', command=validate).grid()   
        tk.Frame(f_positif,width=LARGEUR).grid(columnspan=2)
            
    def sel_antifiltre():
        ''' Sélectionne les anti-filtres, c'est à dire les types de mains que
        l'on ne veut pas.
        Fonctionnement analogue à sel_filtre
        '''
        if DEBUG :
            print('sel_antifiltre')
        def validate(event=None):
            if DEBUG :
                print("validation")
            index_filtre = menu_deroulant.curselection()
            sequence.negatif[sequence.position] = \
                                   [liste_des_filtres[i] for i in index_filtre]
            affiche_filtre(sequence.position)
                
        clear(f_negatif)
        defilement = tk.Scrollbar(f_negatif, orient='vertical')                           
        defilement.grid(row=1, column=1, sticky='ns')
        noms_de_filtres = [f.name for f in liste_des_filtres]
        menu_deroulant = tk.Listbox(f_negatif, 
                                    yscrollcommand=defilement.set,
                                    height=9, 
                                    selectmode='multiple')
        defilement.configure(command=menu_deroulant.yview)
        menu_deroulant.bind("<Return>", validate)
        menu_deroulant.grid(row=1, column=0)
        for nom in noms_de_filtres :
            menu_deroulant.insert(tk.END, nom)
        tk.Button(f_negatif, text='Ok', command=validate).grid()   
        tk.Frame(f_negatif,width=LARGEUR).grid(columnspan=2)
        
    def affiche_filtre(pos):
        ''' Boutons pour sélectionner les filtres
        '''
        messages = ['Filtre de Nord', 'Filtre de Sud',
                    "Filtre d'Est", "Filtre d'Ouest"]
        negsages = ['Interdit de Nord', 'Interdit de Sud',
                    "Interdit d'Est", "Interdit d'Ouest"]
        b_positif.configure(text=messages[sequence.position])
        b_negatif.configure(text=negsages[sequence.position])
        clear(f_positif)
        clear(f_negatif)
        for filtre in sequence.positif[sequence.position] :
            tk.Label(f_positif, text=filtre.name).grid()
        tk.Frame(f_positif,width=LARGEUR).grid()
        for filtre in sequence.negatif[sequence.position] :
            tk.Label(f_negatif, text=filtre.name).grid() 
        tk.Frame(f_negatif,width=LARGEUR).grid()    
        if DEBUG :
            print('affiche sortie')    

#########################################################
#####               DEBUT                 
#########################################################
#   Initialisations     
    liste_des_filtres = readfiltres()       
    barre_de_message('Séquence de filtres', messager)        
    clear(fenetre)
    LARGEUR = 250
    HAUTEUR = 200
    
#   Titre    
    tk.Label(fenetre, text='Main à filtrer').grid(row=0,columnspan=4)
    
#   Boutons de position    
    boutons = []
    for pos in Position:
        boutons.append(tk.Button(fenetre, command=callback(pos), 
                  text=pos.name()))
        boutons[pos].grid(row=1, column=int(pos), sticky='ew')
        
#   Fenêtre de sélection de filtres à gauche        
    b_positif = tk.Button(fenetre, text=f"Filtre à sélectionner",
              command=sel_filtre, state='disabled')
    b_positif.grid(row=2, columnspan=2, sticky='ew')
    f_positif = tk.Frame(fenetre, height=HAUTEUR, width=LARGEUR)
    f_positif.grid(row=3, columnspan=2)
    f_positif.grid_propagate(0)
    
#   fenêtre de sélection d'anti-filtres à droite    
    b_negatif = tk.Button(fenetre, text=f"Filtres interdit",
              command=sel_antifiltre, state='disabled')
    b_negatif.grid(row=2, column=2, columnspan=2, sticky='ew')    
    f_negatif = tk.Frame(fenetre, height=HAUTEUR, width=LARGEUR)
    f_negatif.grid(row=3, column=2, columnspan=2)
    f_negatif.grid_propagate(0)
    
#   Nommer la séquence
    saisie = tk.StringVar(fenetre, value=sequence.name)
    if DEBUG :
        print("entrée:", saisie.get())
    tk.Label(fenetre, text='Nom : ').grid(row=4, column=0)
    e = tk.Entry(fenetre, textvariable=saisie)
    e.grid(row=4, column=1, columnspan=3, sticky='ew')    
    
#   Bouton pour sortir  
    '''
    confirmation = tk.Button(fenetre, 
                             text='Valider les filtres',
                             command=confirmer)
    confirmation.grid(row=5, columnspan=2)
    annulation = tk.Button(fenetre,
                           text='Annuler',
                           command=annuler)
    annulation.grid(row=5, column=2, columnspan=2)
    '''
    
    
    if DEBUG :    
       def verify():
           barre_de_message(saisie.get(), messager)
       verification = tk.Button(fenetre, text = " Vérifier le nom",
                                command=verify)
       verification.grid(row=6)
       
    return saisie
    # récupération du nom de la séquence de filtres   



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 09:38:57 2018

@author: hubert
"""
import tkinter as tk


def clear(frame) :
    ''' Efface la fenêtre '''
    for i in frame.grid_slaves():
        i.destroy()
        
 
def barre_de_menu(liste, menu) :
    ''' Associe une liste de boutons à une liste de commandes
    dans le frame : menu
    les items de la liste sont des couples de la forme
    [nom du bouton, commande à exécuter]'''
    clear(menu)
    for commande in liste:
        bouton = tk.Button(menu,
                           text=commande[0],
                           command=commande[1],
                           width=20)
        bouton.grid(sticky="ew")


def barre_de_message(message, messager) :
    ''' Affiche un message dans la barre d'état : messager '''
    clear(messager)
    mess = tk.Label(messager, text=message)
    mess.grid()
   
    
def barre_de_validation(menu, validate, cancel=None) :
    ''' Crée deux bouton dans le menu
    validation : commande à éxécuter en cas de validation
    cancel     : commande à éxécuter ebn cas d'annulation '''
    def nope() :
        pass
    if not cancel :
        cancel = nope
    clear(menu)
    tk.Button(menu, text='Valider', command=validate, width=20).grid()
    tk.Button(menu, text='Annuler', command=cancel, width=20).grid()     
    
def scale_couple(fenetre, name, ligne, maxi=13):
    ''' 
    Couplage de deux ScaleButtons pour 
    régler une intervalle d'entier
    fenetre = Frame d'affichage
    name    = nom du Bouton à afficher
    ligne   = position dans la grille
    maxi    = valeur maxuimale       
    '''
    def min_command(event):
        value_min = var_min.get()
        value_max = var_max.get()
        if value_min > value_max :
            var_max.set(value_min)
    def max_command(event):
        value_min = var_min.get()
        value_max = var_max.get()
        if value_min > value_max :
            var_min.set(value_max)       
    w_lab = tk.Label(fenetre, text = name)
    w_lab.grid(row=ligne, column=0, sticky="w")
    var_min = tk.IntVar(fenetre)
    var_max = tk.IntVar(fenetre)
    min_button = tk.Scale(fenetre, variable=var_min, from_=0, to=maxi,
                          orient=tk.HORIZONTAL, command=min_command)
    min_button.grid(row=ligne, column=1)
    max_button = tk.Scale(fenetre, variable=var_max, from_=0, to=maxi,
                          orient=tk.HORIZONTAL, command=max_command)
    max_button.grid(row=ligne, column=2)  
    return var_min,var_max      

def desactiver(menu) :
    for w in menu.winfo_children() :
        w.configure(state='disabled')
    
def activer(menu) :    
    for w in menu.winfo_children() :
        w.configure(state='normal')       
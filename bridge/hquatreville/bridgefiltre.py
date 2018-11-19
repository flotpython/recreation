#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 17:57:57 2018

@author: hubert
"""

import tkinter as tk
from bridgelib import Filtre
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
menu.grid(row=0, column=0,sticky='n')
root.columnconfigure(0,weight=1)        

fenetre = tk.Frame(root)
fenetre.grid(row=0, column=1)
root.columnconfigure(1,weight=3)

messager = tk.Frame(root)
messager.grid(row=1, columnspan=2) 
mess = tk.Label(messager, text = "Démarrage")
mess.grid(sticky='ew')


####       Commandes   ####  
def scale_couple(frame, name, ligne, maxi=40):
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
    var_min = tk.IntVar()
    var_max = tk.IntVar()
    min_button = tk.Scale(fenetre, variable=var_min, from_=0, to=maxi,
                          orient=tk.HORIZONTAL, command=min_command)
    min_button.grid(row=ligne, column=1)
    max_button = tk.Scale(fenetre, variable=var_max, from_=0, to=maxi,
                          orient=tk.HORIZONTAL, command=max_command)
    max_button.grid(row=ligne, column=2)  
    return var_min,var_max     



def c_regler_filtre(index_filtre = None):
    clear(menu)
    barre_de_message('Réglage du filtre', messager)
    def conclure():
        if name.get():
            print(var_pointH_min.get(),var_HLD_min.get())
            print(name.get())
            filtre = Filtre (name = name.get(),
                             pointH_min = var_pointH_min.get(),
                             pointH_max = var_pointH_max.get(),
                             trefle_min = trefle_min.get(),
                             trefle_max = trefle_max.get(),
                             carreau_min = carreau_min.get(),
                             carreau_max = carreau_max.get(),
                             coeur_min = coeur_min.get(),
                             coeur_max = coeur_max.get(),
                             pique_min = pique_min.get(),
                             pique_max = pique_max.get(),
                             points_totaux_min = var_HLD_min.get(),
                             points_totaux_max = var_HLD_max.get())
            liste_des_filtres.append(filtre)
            if isinstance(index_filtre, int) :
                del liste_des_filtres[index_filtre]
            liste_des_filtres.sort(key= lambda filtre:filtre.name)   
            writefiltre(liste_des_filtres)
            clear(fenetre)
            barre_de_menu(filtre_menu,menu)
                
            
    def annuler():
        clear(fenetre)
        barre_de_menu(filtre_menu,menu)
    def supprimer():
        print('supprimer')
        if askyesno(title='Etes-vous sûr ?',
                    message='Vous allez supprimez un filtre'):
            print('oui')
            del liste_des_filtres[index_filtre]
            liste_des_filtres.sort(key= lambda filtre:filtre.name)
            clear(fenetre)
            barre_de_menu(filtre_menu,menu)
        
    
    var_pointH_min, var_pointH_max = scale_couple(fenetre, 'Points H', 0)
    var_HLD_min, var_HLD_max = scale_couple(fenetre, 'Points HLD', 1, 60)
    pique_min, pique_max = scale_couple(fenetre, 'Nombre de piques', 2, 13)
    coeur_min, coeur_max = scale_couple(fenetre, 'Nombre de coeurs', 3, 13)
    carreau_min, carreau_max = scale_couple(fenetre, 
                                            'Nombre de carreaux', 4, 13)
    trefle_min, trefle_max = scale_couple(fenetre, 'Nombre de trèfles', 5, 13)
    name = tk.StringVar()
    tk.Label(fenetre, text='Nom du filtre').grid(row=10, column=0)
    tk.Entry(fenetre, textvariable=name).grid(row=10, column = 1)
    tk.Button(fenetre, text='Sauvegarder', command = conclure, 
              width = 8).grid(row=11, column=0)
    tk.Button(fenetre, text='Annuler', command = annuler, 
              width = 8).grid(row=11, column=2)
    if isinstance(index_filtre, int) :
        selection = liste_des_filtres[index_filtre]
        name.set(selection.name)
        var_pointH_min.set(selection.pointH_min)
        var_pointH_max.set(selection.pointH_max)
        var_HLD_min.set(selection.points_totaux_min)
        var_HLD_max.set(selection.points_totaux_max)
        pique_min.set(selection.pique_min)
        pique_max.set(selection.pique_max)
        coeur_min.set(selection.coeur_min)
        coeur_max.set(selection.coeur_max)
        carreau_min.set(selection.carreau_min)
        carreau_max.set(selection.carreau_max)
        trefle_min.set(selection.trefle_min)
        trefle_max.set(selection.trefle_max)
        tk.Button(fenetre, text='Supprimer', command = supprimer, 
              width = 8).grid(row=11, column=1)
    else :
        var_pointH_max.set(40)
        var_HLD_max.set(60)
        pique_max.set(13)
        coeur_max.set(13)
        carreau_max.set(13)
        trefle_max.set(13)
  

def c_modifier_filtre():
    def validate(event):
        print("validation")
        index_filtre, = menu_deroulant.curselection()               
        clear(fenetre)
        c_regler_filtre(index_filtre)
        #c_regler_filre()
    
    print('modifier filtre')
    clear(menu)
    defilement = tk.Scrollbar(fenetre, orient='vertical')                           
    defilement.grid(row=1, column=1, sticky='ns')
    tk.Label(fenetre, text = 'Choisir le filtre à modifier').grid(row=0, 
                                                                  column=0)
    noms_de_filtres = [f.name for f in liste_des_filtres]
    menu_deroulant = tk.Listbox(fenetre, yscrollcommand=defilement.set,
                                height=9)
    defilement.configure(command=menu_deroulant.yview)
    menu_deroulant.bind("<Double-Button-1>", validate)
    menu_deroulant.grid(row=1, column=0)
    for nom in noms_de_filtres :
        menu_deroulant.insert(tk.END, nom)
    


def c_afficher_filtres():
    for f in liste_des_filtres:
        print(f.name)


filtre_menu = [[' Nouveau filtre', c_regler_filtre],
               ['Modifier filtre',c_modifier_filtre],
               ['Afficher filtres',c_afficher_filtres]]
barre_de_menu(filtre_menu,menu)


#####      MAINLOOP      ######
liste_des_filtres = readfiltres()

print('boucle')
root.mainloop()
root.destroy()     
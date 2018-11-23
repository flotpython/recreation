#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 09:27:49 2018

@author: hubert
"""

import tkinter as tk
from tkinter.messagebox import askyesno
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import pickle

from tklib import clear, barre_de_message, barre_de_menu, barre_de_validation
from tklib import scale_couple
from bridgelib import Sequence, Donne, Position, Filtre
from sequencelib import regler_sequence
from IOlib import readfiltres, readsequences, writesequences, writefiltres
from donnelib import Donne_active

DONNETYPE = ("Pack de donne", ".pak")

DEBUG = False
# True permet la réinitialisations des données sur les filtres
# en cas de problème

################################################################
#       INITIALISATION DES VARIABLES GLOBALES
################################################################
sequence_active = None
# La séquence en cours d'utilisation (vide a priori)

donne_actuelle = Donne()
# La donne en cours d'affichage

pack_actif = []
# Le pack de donne en cours d'utilisation
index_pack = 0
# Index référençant la donne du pack en cours d'utilisation

liste_des_filtres = readfiltres()
# Les filtres sauvegardés dans le fichier filtres.fil

liste_des_sequences = readsequences()
# Les séquences sauvegardées dans le fichier sequences.fil

position_active = Position(1)
# La position natuelle est en Sud

widgets_actifs ={}
# Sauvegarde de quelques boutons afin de maintenir la communication entre
# ceux-ci.



################################################################

def c_retour():
    ''' Retour au menu principal '''
    clear(fenetre)
    menu_principal()
    
################################################################
#                  MENU    PRINCIPAL  
################################################################
def c_gestion_donne():
    clear(menu)
    barre_de_message("Menu des donnes", messager)
    barre_de_menu(lm_donne, menu)

def c_sequence():
    clear(menu)
    barre_de_message("Menu des séquences", messager)
    barre_de_menu(lm_sequence, menu)
    
def c_gestion_filtre():
    clear(menu)
    clear(fenetre)
    barre_de_message("Menu des filtres", messager)
    barre_de_menu(lm_filtre, menu)

def c_enchérir():
    clear(menu)
    barre_de_message("Menu des enchères", messager)
    barre_de_menu(lm_enchere, menu)
    initialise_encheres()

def c_quit():
    root.quit()
    root.destroy()


lm_principale = [["Gérer les donnes", c_gestion_donne],
                 ["Gérer les filtres", c_gestion_filtre],
                 ["Gérer les séquences", c_sequence],
                 ["Enchérir", c_enchérir],
                 ["Quitter", c_quit]
                ]

def menu_principal() :
    load = Image.open("data/gambling.jpg")
    resolution = (250,200)
    img = ImageTk.PhotoImage(load.resize(resolution), master=fenetre)
    panel = tk.Label(fenetre, image=img)
    panel.grid()
    panel.image = img
    barre_de_menu(lm_principale, menu)
    barre_de_message("Menu principal", messager)    


################################################################
#                  MENU DONNES
################################################################
def c_distribuer_donnes() :
    def validate() :
        global pack_actif, index_pack
        try :
            saisie = int(saisir.get())
        except ValueError :
            mess = 'Entrez un entier stictement positif'
            barre_de_message(mess,messager)
            return None
        if saisie in range(1,1000):
            compteur = 0
            overflow = 0
            pack_actif =[]
            index_pack = 0
            while compteur < saisie and overflow < 10_000 :
                donne = Donne()
                overflow += 1
                if (not sequence_active) or sequence_active.filtre(donne) :
                    compteur += 1
                    pack_actif.append(donne.identifiant())
            if compteur == 0 :
                mess = 'Filtres incompatibles'              
            elif compteur < 0 :
                mess = 'Donnes rares.' + str(compteur) + 'donnes distribuées'
            else :
                mess = 'Donnes distribuées'     
            barre_de_message(mess, messager)   
            barre_de_menu(lm_donne, menu)
            clear(fenetre) 
        else :
            mess = 'Entrez un entier compris entre 1 et 1000'
            barre_de_message(mess,messager)
        
    def cancel() :
        clear(menu)
        barre_de_menu(lm_donne, menu)
        clear(fenetre)
        
    clear(fenetre)
    w1 = tk.Label(fenetre, text="Combien voulez-vous de donnes : ")
    w1.grid(row=0, column=0)
    saisir = tk.Entry(fenetre)
    saisir.grid(row=0, column=1)
    if sequence_active :
        mess = "Séquence de filtres activés : " + sequence_active.name
    else :
        mess = 'Pas de filtre actif, donnes aléatoires '        
    w3 = tk.Label(fenetre, text=mess)
    w3.grid(row=1, columnspan=2)
    barre_de_validation(menu, validate, cancel)

def c_sauvegarder_donnes() :
    if DEBUG :
        print("sauver")
    var = tk.StringVar(fenetre)

    def validate(event):
        text = var.get()
        try:
            filename = "data/" + text + ".pak"
            with open(filename, "wb") as fichier:
                pickle.dump(pack_actif, fichier)
            wlabel.destroy()
            wentree.destroy()
            barre_de_message(f"Fichier {filename[5:]} savegardé", messager)
        except IOError:
            barre_de_message("Problème d'entrée/sortie", messager)
    wlabel = tk.Label(fenetre, text="Nom du fichier")
    wlabel.grid()
    wentree = tk.Entry(fenetre, textvariable=var)
    wentree.grid()
    wentree.bind('<Return>', validate)

def c_charger_donnes() :
    if DEBUG :
        print("charger")
    global pack_actif, index_pack
    donnename = tk.StringVar(fenetre)
    donnename.set(askopenfilename(filetypes=[DONNETYPE], initialdir='data/'))
    filename = donnename.get()
    if DEBUG :
        print(filename)
    with open(filename, "rb") as fichier:
        pack_actif = pickle.load(fichier)
        index_pack = 0
        if DEBUG :
            print(pack_actif)  
        mess = f'Donne du fichier {filename} chargées'
        barre_de_message(mess,messager)

def c_charger_archives() :
    mess = 'Option indisponible dans cette version'
    barre_de_message(mess, messager)

lm_donne = [['Distribuer', c_distribuer_donnes],
            ['Sauvegarder', c_sauvegarder_donnes],
            ['Charger', c_charger_donnes],
            ['Archives', c_charger_archives],
            ["Gérer les séquences", c_sequence],
            ["Enchérir", c_enchérir],
            ['Menu principal', c_retour],
            ["Quitter", c_quit]
           ]
################################################################
#                  MENU FILTRE
################################################################
def c_regler_filtre(index_filtre = None):
    clear(menu)
    barre_de_message('Réglage du filtre', messager)
    def conclure():
        if name.get():
            if DEBUG :
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
            writefiltres(liste_des_filtres)
            clear(fenetre)
            barre_de_menu(lm_filtre,menu)
                
            
    def annuler():
        clear(fenetre)
        barre_de_menu(lm_filtre,menu)
        
    def supprimer():
        if DEBUG :
            print('supprimer')
        if askyesno(title='Etes-vous sûr ?',
                    message='Vous allez supprimez un filtre'):
            if DEBUG :
                print('oui')
            del liste_des_filtres[index_filtre]
            liste_des_filtres.sort(key= lambda filtre:filtre.name)
            clear(fenetre)
            barre_de_menu(lm_filtre,menu)
        
    
    var_pointH_min, var_pointH_max = scale_couple(fenetre, 'Points H', 0, 40)
    var_HLD_min, var_HLD_max = scale_couple(fenetre, 'Points HLD', 1, 60)
    pique_min, pique_max = scale_couple(fenetre, 'Nombre de piques', 2)
    coeur_min, coeur_max = scale_couple(fenetre, 'Nombre de coeurs', 3)
    carreau_min, carreau_max = scale_couple(fenetre, 'Nombre de carreaux', 4)
    trefle_min, trefle_max = scale_couple(fenetre, 'Nombre de trèfles', 5)
    name = tk.StringVar(fenetre)
    tk.Label(fenetre, text='Nom du filtre').grid(row=10, column=0)
    tk.Entry(fenetre, textvariable=name).grid(row=10, column = 1)
    #tk.Button(fenetre, text='Sauvegarder', command = conclure, 
    #          width = 8).grid(row=11, column=0)
    #tk.Button(fenetre, text='Annuler', command = annuler, 
    #          width = 8).grid(row=11, column=2)
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
        lm_regler_filtre = [['Sauvegarder', conclure],
                            ['Supprimer', supprimer],
                            ['Annuler', annuler] 
                            ]
        #tk.Button(fenetre, text='Supprimer', command = supprimer, 
        #      width = 8).grid(row=11, column=1)
    else :
        var_pointH_max.set(40)
        var_HLD_max.set(60)
        pique_max.set(13)
        coeur_max.set(13)
        carreau_max.set(13)
        trefle_max.set(13)
        lm_regler_filtre = [['Sauvegarder', conclure],
                            ['Annuler', annuler] 
                            ]
    barre_de_menu(lm_regler_filtre, menu)  

def c_modifier_filtre():
    def validate(event=None):
        if DEBUG :
            print("validation")
        try :    
            index_filtre, = menu_deroulant.curselection()               
            clear(fenetre)
            c_regler_filtre(index_filtre)
        except ValueError :
            mess = 'Choisir le filtre à modifier'
            barre_de_message(mess, messager)
        #c_regler_filre()
    
    def annuler():
        clear(fenetre)
        barre_de_menu(lm_filtre,menu)
    
    if DEBUG :    
        print('modifier filtre')
    clear(menu)
    defilement = tk.Scrollbar(fenetre, orient='vertical')                           
    defilement.grid(row=1, column=1, sticky='ns')
    lab = tk.Label(fenetre, text = 'Choisir le filtre à modifier')
    lab.grid(row=0, column=0)
    noms_de_filtres = [f.name for f in liste_des_filtres]
    menu_deroulant = tk.Listbox(fenetre, 
                                yscrollcommand=defilement.set,
                                height=9)
    defilement.configure(command=menu_deroulant.yview)
    menu_deroulant.bind("<Double-Button-1>", validate)
    menu_deroulant.grid(row=1, column=0)
    for nom in noms_de_filtres :
        menu_deroulant.insert(tk.END, nom)
    lm_modifier_filtre = [['Choisir', validate],
                          ['Annuler', annuler]
                         ]     
    barre_de_menu(lm_modifier_filtre, menu)    
    


def c_afficher_filtres():
    for f in liste_des_filtres:
        print(f.name) 

lm_filtre = [[' Nouveau filtre', c_regler_filtre],
             ['Modifier filtre',c_modifier_filtre],
             ["Gérer les séquences", c_sequence],
             ['Menu principal', c_retour],
             ["Quitter", c_quit]
             ]
################################################################
#                  MENU ENCHERES 
################################################################


def initialise_encheres() :
    clear(fenetre)  
    fenetre_donne = tk.Frame(fenetre, height = 100)
    fenetre_donne.grid(row=1, columnspan=4)   
    visible = position_active.visibilite()
    if DEBUG :
        print(visible)
    donne_active = Donne_active(donne_actuelle, fenetre_donne, visible)
    donne_active.affiche()
    widgets_actifs["donne_active"] = donne_active
    def select_position() :
        global position_active
        position_active = Position(varRad.get())
        if DEBUG :
            print(position_active)
        donne_active.visible = position_active.visibilite()    
        donne_active.affiche()    
      
    varRad = tk.IntVar(fenetre)
    varRad.set(position_active+0)
    boutons_de_position_des_encheres = []
    for pos in Position :
        b = tk.Radiobutton(fenetre, 
                           variable=varRad, 
                           text=pos.name(),
                           indicatoron=0,
                           value=int(pos),
                           command=select_position,
                           width=10,
                           anchor='n')
        b.grid(row=0, column=pos+0, sticky='ew')
        boutons_de_position_des_encheres.append(b)
    widgets_actifs['BDPDE'] = boutons_de_position_des_encheres 
    if DEBUG :
        print(widgets_actifs)
    mess = 'Donne aléatoire lors de la configuration'    
    barre_de_message(mess, messager)    

def c_choisir_position() :
    if widgets_actifs['BDPDE'][0].cget('state') == 'disabled' :
        for pos in Position :
            widgets_actifs['BDPDE'][pos].configure(state='normal')
    else :  
        for pos in Position :
            widgets_actifs['BDPDE'][pos].configure(state='disabled')

def c_afficher_ligne() :
    donne_active = widgets_actifs["donne_active"]
    donne_active.visible = position_active.visibilite_ligne()
    donne_active.affiche()

def c_afficher_donne() :
    donne_active = widgets_actifs["donne_active"]
    donne_active.visible = [True for pos in Position]
    donne_active.affiche()

def c_donne_suivante() :
    global index_pack
    if index_pack == len(pack_actif) :
        mess = 'Dernière donne atteinte'
        barre_de_message(mess, messager)       
    else :    
        donne_active = widgets_actifs["donne_active"]
        donne = Donne (identifiant=pack_actif[index_pack])
        index_pack += 1
        donne_active.visible = position_active.visibilite()
        donne_active.reconfigure(donne)
        barre_de_message(f'Enchérir la donne n°{index_pack}', messager)

def c_archiver_donne() :
    mess = 'Fonctionnalité non disponible dans cette version'
    barre_de_message(mess, messager)
    
lm_enchere = [['Choisir Position', c_choisir_position],
              ['Afficher Ligne', c_afficher_ligne],
              ['Afficher donne', c_afficher_donne],
              ['Donne suivante', c_donne_suivante],
              ['Archiver', c_archiver_donne],
              ["Gérer les donnes", c_gestion_donne],
              ['Menu principal', c_retour],
               ["Quitter", c_quit]
              ]
################################################################
#                  MENU SEQUENCES
################################################################
def c_choisir_sequence() :
    ''' Choix de la séquence active '''
    def postaction() :        
        barre_de_menu(lm_sequence, menu)
        barre_de_message(f'Séquence active : {sequence_active.name}', messager)
        clear(fenetre)
        
    if liste_des_sequences :
        clear(fenetre)
        _selectionne_sequence(postaction)
        
    else :
        clear(fenetre)
        tk.Label(fenetre, text = "Attention !").grid()
        tk.Label(fenetre, text = "Aucune séquence sauvegardées !").grid()
        tk.Label(fenetre, text = "Veuillez en créer une nouvelle !").grid()
        
def _selectionne_sequence(postaction) :
    def validate(event=None) :
        global sequence_active
        if DEBUG :
            print("Validation sequence")
        try :    
            index_sequence, = menu_deroulant.curselection()   
        except ValueError :
            barre_de_message('Sélectionnez une séquence', messager)  
            return None
        sequence_active = liste_des_sequences[index_sequence]  
        postaction()
    
    def escape(event=None) :
        barre_de_menu(lm_sequence, menu)
        clear(fenetre)
           
    if DEBUG :    
        print('chosir sequence')
    defilement = tk.Scrollbar(fenetre, orient='vertical')                           
    defilement.grid(row=1, column=2, sticky='ns')
    lab = tk.Label(fenetre, text = 'Choisir la séquence active')
    lab.grid(row=0, column=0, columnspan=2)
    noms_de_sequences = [seq.name for seq in liste_des_sequences]
    menu_deroulant = tk.Listbox(fenetre, 
                                yscrollcommand=defilement.set,
                                height=9)
    defilement.configure(command=menu_deroulant.yview)
    menu_deroulant.bind("<Double-Button-1>", validate)
    menu_deroulant.grid(row=1, column=0, columnspan=2)
    for nom in noms_de_sequences :
        menu_deroulant.insert(tk.END, nom)  
    #mini = tk.Frame(fenetre).grid(row=2, column=0)   
    barre_de_validation(menu, validate, escape)
    '''
    but1 = tk.Button(fenetre, text='Valider', command=validate)
    but1.grid(row=2, column=0)
    but2 = tk.Button(fenetre, text='Annuler', command=escape, anchor='w')
    but2.grid(row=2, column=1)  
    '''

def c_modifier_sequence() :
    ''' Modification de la séquence active '''
    if DEBUG :
            print('modifier séquence')
    clear(fenetre)    
    _selectionne_sequence(_modification)        

    
def _modification() :
    def postaction() :
        ''' Actions à effectuer en sortie '''
        name = saisie.get() 
        if DEBUG :
            print("sortie:", saisie.get())
        name_actif = sequence_active.name
        names = [seq.name for seq in liste_des_sequences]
        names = [n for n in names if n != name_actif]    
        if name :
            if name in names :
                barre_de_message('Ce nom existe déjà', messager)
            else :
                barre_de_message('Séquence validée', messager)                              
        else :
            barre_de_message('Entrez un nom de séquence', messager)
        sequence_active.name = name    
        barre_de_menu(lm_sequence, menu)
        liste_des_sequences.sort(key= lambda seq:seq.name)
        writesequences(liste_des_sequences)
        clear (fenetre)
         
    def annul():
        barre_de_menu(lm_sequence, menu)
        clear(fenetre)
           
    
    barre_de_validation(menu, postaction, annul)
    saisie = regler_sequence(sequence_active, fenetre, messager)     
    # La suite est envoyée dans séquence par le biais de postaction
    # ou annul
    
def _supprimer_sequence(sequence) :
    global liste_des_sequences
    name = sequence.name
    for i in range(len(liste_des_sequences)) :
        if liste_des_sequences[i].name == name :
            index = i
    del liste_des_sequences[index]
        

def c_nouvelle_sequence() :
    ''' Crée une nouvelle séquence de filtres'''
    def postaction() :
        ''' Actions à effectuer en sortie '''
        names = [seq.name for seq in liste_des_sequences]
        name = saisie.get()
        if name in names :
            mess = "Ce nom existe déjà !"
            barre_de_message(mess, messager)
        else :
            sequence.name = name
            barre_de_menu(lm_sequence, menu)
            liste_des_sequences.append(sequence)
            liste_des_sequences.sort(key= lambda seq:seq.name)
            writesequences(liste_des_sequences)
            clear(fenetre)
            
    def annul():
        barre_de_menu(lm_sequence, menu)   
        
    clear(fenetre)    
    sequence = Sequence()
    barre_de_validation(menu, postaction, annul)    
    saisie = regler_sequence(sequence, fenetre, messager)     
    # La suite eszt envoyée dans séquence par le biais de postaction
    

def c_reinitialiser_sequences() :
    global liste_des_sequences
    clear(fenetre)
    tk.Label(fenetre, text = "Attention !").grid()
    tk.Label(fenetre, text = "Vous allez effacer les séquences !").grid()
    tk.Label(fenetre, text = "En cas de Bug uniquement !").grid()
    if askyesno(title='EFFACEMENT DES SEQUENCES', 
                message='Continuer ?',
                parent=menu) :
        liste_des_sequences = []
        writesequences(liste_des_sequences)
    clear(fenetre)    
        

        
def c_supprimer_sequence() :
    ''' Choix de la séquence active puis supression'''
    def postaction() : 
        global sequence_active
        barre_de_menu(lm_sequence, menu)
        _supprimer_sequence(sequence_active)
        writesequences(liste_des_sequences)
        barre_de_message(f'{sequence_active.name} effacée', messager)
        sequence_active = None
        clear(fenetre)
        
    if liste_des_sequences :
        clear(fenetre)
        _selectionne_sequence(postaction)
        
    else :
        clear(fenetre)
        tk.Label(fenetre, text = "Attention !").grid()
        tk.Label(fenetre, text = "Aucune séquence sauvegardées !").grid()
        tk.Label(fenetre, text = "Veuillez en créer une nouvelle !").grid()
    
    

lm_sequence = [['Choisir séquence', c_choisir_sequence],
               ['Modifier séquence', c_modifier_sequence],
               ['Nouvelle séquence', c_nouvelle_sequence],
               ['Supprimer séquence', c_supprimer_sequence],
               ["Gérer les filtres", c_gestion_filtre],
               ["Gérer les donnes", c_gestion_donne],
               ['Menu principal', c_retour],
               ["Quitter", c_quit]
               ] 
              
if DEBUG :
    lm_sequence.append(['Réinitialiser', c_reinitialiser_sequences])    





################################################################
#       LANCEMENT DE L'INTERFACE
################################################################

root=tk.Tk()
root.title('Utilitaire pour bridgeur')

menu   = tk.Frame(root)
menu.grid(row=0, column=0,sticky='n')
#menu.configure(width=180, height = 200)
#menu.grid_propagate(0)
root.columnconfigure(0,weight=1)        

fenetre = tk.Frame(root)
fenetre.grid(row=0, column=1)
root.columnconfigure(1,weight=3)

messager = tk.Frame(root)
messager.grid(row=1, columnspan=2) 
mess = tk.Label(messager, text = "Démarrage")
mess.grid(sticky='ew')

if DEBUG :
    print('boucle')
menu_principal()
root.protocol("WM_DELETE_WINDOW", c_quit)
root.mainloop()
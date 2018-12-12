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
from random import randint

import tkcolors
from tklib import clear, barre_de_message, barre_de_menu, barre_de_validation
from tklib import scale_couple
from bridgelib import Sequence, Donne, Position, Filtre
from bridgelib import InvalidSequence, Vulnerabilite
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

pack_actif = [donne_actuelle.identifiant()]
# Le pack de donne en cours d'utilisation
index_pack = 0
# Index référençant la donne du pack en cours d'utilisation

liste_des_filtres = readfiltres()
# Les filtres sauvegardés dans le fichier filtres.fil

liste_des_sequences = readsequences()
# Les séquences sauvegardées dans le fichier sequences.fil

position_active = Position(1)
# La position natuelle est en Sud

widgets_actifs = {}
# Sauvegarde de quelques boutons afin de maintenir la communication entre
# ceux-ci.

expert = True

################################################################

def c_retour():
    ''' Retour au menu principal '''
    clear(fenetre)
    if expert:
        menu_principal()
    else:
        proto_menu()

def c_quit():
    root.quit()
    root.destroy()

################################################################
#                       PROTO MENU
################################################################

def c_menu_rapide():
    global expert
    expert = False
    c_charger_donnes()
    clear(menu)
    barre_de_message("Menu des enchères", messager)
    barre_de_menu(lm_enchere_rapide, menu)
    initialise_encheres()

def c_menu_normal():
    global expert
    expert = False

    def postaction():
        mess = f'Séquence active : {sequence_active.name}'
        barre_de_message(mess, messager)
        c_distribuer_donnes()

    if liste_des_sequences:
        clear(fenetre)
        _selectionne_sequence(postaction)
    else:
        clear(fenetre)
        expert = True
        tk.Label(fenetre, text="Attention !").grid()
        tk.Label(fenetre, text="Aucune séquence sauvegardées !").grid()
        tk.Label(fenetre, text="Veuillez en créer une nouvelle !").grid()

def c_menu_expert():
    global expert
    expert = True
    clear(fenetre)
    menu_principal()


lm_proto_menu = [["Menu rapide", c_menu_rapide],
                 ["Menu normal", c_menu_normal],
                 ["Menu expert", c_menu_expert],
                 [],
                 ["Quitter", c_quit]
                 ]


def image():
    clear(fenetre)
    load = Image.open("data/gambling.jpg")
    resolution = (375, 300)
    img = ImageTk.PhotoImage(load.resize(resolution), master=fenetre)
    panel = tk.Label(fenetre, image=img)
    panel.grid()
    panel.image = img


def proto_menu():
    image()
    barre_de_menu(lm_proto_menu, menu)
    barre_de_message("Menu principal", messager)

################################################################
#                  MENU    PRINCIPAL
################################################################


def c_gestion_donne():
    clear(menu)
    image()
    barre_de_message("Menu des donnes", messager)
    barre_de_menu(lm_donne, menu)


def c_sequence():
    clear(menu)
    image()
    barre_de_message("Menu des séquences", messager)
    barre_de_menu(lm_sequence, menu)


def c_gestion_filtre():
    clear(menu)
    image()
    barre_de_message("Menu des filtres", messager)
    barre_de_menu(lm_filtre, menu)


def c_enchérir():
    clear(menu)
    barre_de_message("Menu des enchères", messager)
    barre_de_menu(lm_enchere, menu)
    initialise_encheres()


lm_principale = [["Gérer les donnes", c_gestion_donne],
                 ["Gérer les filtres", c_gestion_filtre],
                 ["Gérer les séquences", c_sequence],
                 ["Enchérir", c_enchérir],
                 [],
                 ["Quitter", c_quit]
                 ]


def menu_principal():
    image()
    barre_de_menu(lm_principale, menu)
    barre_de_message("Menu principal", messager)

################################################################
#                  MENU DONNES
################################################################


def c_distribuer_donnes():
    def validate(event=None):
        global pack_actif, index_pack
        try:
            saisie = int(saisir.get())
        except ValueError:
            mess = 'Entrez un entier stictement positif'
            barre_de_message(mess, messager)
            return None
        if saisie in range(1, 1000):
            mess = 'Cela prend parfois quelques instants'
            barre_de_message(mess, messager)
            messager.update()
            index_pack = 0
            if not sequence_active:
                pack_actif = [Donne() for i in range(saisie)]
            else:
                try :
                    pack_actif = []
                    for i in range(saisie):
                        donne = sequence_active.distribue()
                        donneur = vardonneur.get()
                        if donneur == 4 :
                            donne.donneur = randint(0,3)
                        else :    
                            donne.donneur = Position(donneur)
                        vul = varvul.get()
                        if vul == 4 :
                            donne.vul = randint(0,3)
                        else:    
                            donne.vul = Vulnerabilite(vul)
                        pack_actif.append(donne.identifiant())                              
                except InvalidSequence :
                    mess = "Séquence invalide "
                    barre_de_message(mess, messager)
                    clear(menu)
                    barre_de_menu(lm_sequence, menu)
                    clear(fenetre)
                    return None
            mess = 'Donnes distribuées'
            barre_de_message(mess, messager)
            if expert :
                barre_de_menu(lm_donne, menu)
                clear(fenetre)
            else :
                c_sauvegarder_donnes()
        else:
            mess = 'Entrez un entier compris entre 1 et 1000'
            barre_de_message(mess, messager)

    def cancel():
        clear(menu)
        barre_de_menu(lm_donne, menu)
        clear(fenetre)

    clear(fenetre)
    w1 = tk.Label(fenetre, text="Combien voulez-vous de donnes ? : ")
    w1.grid(row=0, column=0)
    saisir = tk.Entry(fenetre)
    saisir.grid(row=0, column=1, columnspan=4)
    saisir.bind("<Return>", validate)
    if sequence_active:
        mess = "Séquence de filtres activés : " + sequence_active.name
    else:
        mess = 'Pas de filtre actif, donnes aléatoires '
    w3 = tk.Label(fenetre, text=mess)
    w3.grid(row=1, column=0)    
    vardonneur = tk.IntVar(fenetre)    
    varvul     = tk.IntVar(fenetre)    
    tk.Label(fenetre, text="Donneur").grid(row=2, column=0)
    for pos in Position:        
        b = tk.Radiobutton(fenetre, 
                           variable=vardonneur, 
                           text = pos.name(),
                           value = int(pos),
                           width=8,
                           anchor="w"
                           )
        b.grid(row=2, column = pos+1)        
        if pos ==0 :
            b.select()
    b = tk.Radiobutton(fenetre, 
                       variable=vardonneur, 
                       text = "aléatoire",
                       value = 4,
                       width=8,
                       anchor="w"
                       )
    b.grid(row=2, column = 5)        
    tk.Label(fenetre, text="Vulnérabilité").grid(row=3, column=0)
    for vul in Vulnerabilite:        
        b = tk.Radiobutton(fenetre, 
                           variable=varvul, 
                           text = vul.name(),
                           value = int(vul),
                           width=8,
                           anchor="w"
                           )
        b.grid(row=3, column = vul+1) 
        if vul ==0 :
            b.select()
    b = tk.Radiobutton(fenetre, 
                       variable=varvul, 
                       text = "aléatoire",
                       value = 4,
                       width=8,
                       anchor="w"
                       )
    b.grid(row=3, column = 5)         
    barre_de_validation(menu, validate, cancel)
    mess = " Distribution des donnes "
    barre_de_message(mess, messager)


def c_sauvegarder_donnes():
    if DEBUG:
        print("sauver")
    var = tk.StringVar(fenetre)

    def validate(event=None):
        text = var.get()
        if text:
            try:
                filename = "data/" + text + ".pak"
                with open(filename, "wb") as fichier:
                    pickle.dump(pack_actif, fichier)
                wlabel.destroy()
                wentree.destroy()
                mess = f"Fichier {filename[5:]} sauvegardé"
                barre_de_message(mess, messager)
                if expert :
                    barre_de_menu(lm_donne, menu)
                else :
                    c_enchérir()
            except IOError:
                barre_de_message("Problème d'entrée/sortie", messager)

    def escape(event=None):
        if expert:
            clear(fenetre)
            barre_de_menu(lm_donne, menu)
        else:
            clear(fenetre)
            barre_de_menu(lm_proto_menu, menu)
            

    clear(fenetre)
    if len(pack_actif) < 5:
        mess = 'Attention, votre pack de donne est presque vide !'
        texte = f'nombre de sonnes à sauvegarder : {len(pack_actif)}'
        alerte1 = tk.Label(fenetre, text=texte)
        alerte1.grid()
        alerte2 = tk.Label(fenetre, text='Avez-vous bien distribué ?')
        alerte2.grid()
        tk.Label(fenetre, text='').grid()
    else:
        mess = 'Sauvegarde des donnes'
    barre_de_message(mess, messager)
    wlabel = tk.Label(fenetre, text="Nom du fichier")
    wlabel.grid()
    wentree = tk.Entry(fenetre, textvariable=var)
    wentree.grid()
    wentree.bind('<Return>', validate)
    barre_de_validation(menu, validate, escape)


def c_charger_donnes():
    if DEBUG:
        print("charger")
    global pack_actif, index_pack
    donnename = tk.StringVar(fenetre)
    donnename.set(askopenfilename(filetypes=[DONNETYPE], 
                                  initialdir='data/'))
    filename = donnename.get()
    if DEBUG:
        print("file : ", filename)
    if filename:
        with open(filename, "rb") as fichier:
            pack_actif = pickle.load(fichier)
            index_pack = 0
            if DEBUG:
                print(pack_actif)
            mess = f'Donne du fichier {filename} chargées'
            barre_de_message(mess, messager)
    else:
        mess = "Pas de fichier sélectionné"
        barre_de_message(mess, messager)


def c_charger_archives():
    mess = 'Option indisponible dans cette version'
    barre_de_message(mess, messager)


lm_donne = [['Distribuer', c_distribuer_donnes],
            ['Sauvegarder', c_sauvegarder_donnes],
            ['Charger', c_charger_donnes],
            ['Archives', c_charger_archives],
            [],
            ["Gérer les séquences", c_sequence],
            ["Enchérir", c_enchérir],
            [],
            ['Menu principal', c_retour],
            ["Quitter", c_quit]
            ]
################################################################
#                  MENU FILTRE
################################################################


def c_regler_filtre(index_filtre=None):
    clear(menu)
    barre_de_message('Réglage du filtre', messager)
    def init_vars(selection):
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

    def conclure():
        if name.get():
            if DEBUG:
                print(var_pointH_min.get(), var_HLD_min.get())
                print(name.get())
            filtre = Filtre(name=name.get(),
                            pointH_min=var_pointH_min.get(),
                            pointH_max=var_pointH_max.get(),
                            trefle_min=trefle_min.get(),
                            trefle_max=trefle_max.get(),
                            carreau_min=carreau_min.get(),
                            carreau_max=carreau_max.get(),
                            coeur_min=coeur_min.get(),
                            coeur_max=coeur_max.get(),
                            pique_min=pique_min.get(),
                            pique_max=pique_max.get(),
                            points_totaux_min=var_HLD_min.get(),
                            points_totaux_max=var_HLD_max.get())
            mess = filtre.controle_couleurs()
            if mess :
                barre_de_message(mess, messager)
                init_vars(filtre)
                return None
            mess = filtre.controle_HLD()
            if mess :
                barre_de_message(mess, messager)
                init_vars(filtre)
                return None
            liste_des_filtres.append(filtre)
            if isinstance(index_filtre, int):
                del liste_des_filtres[index_filtre]
            liste_des_filtres.sort(key=lambda filtre: filtre.name)
            writefiltres(liste_des_filtres)
            barre_de_menu(lm_filtre, menu)
            mess = "Filtre enregistré"
            barre_de_message(mess, messager)
            clear(fenetre)

    def annuler():
        clear(fenetre)
        barre_de_menu(lm_filtre, menu)

    def supprimer():
        if DEBUG:
            print('supprimer')
        if askyesno(title='Etes-vous sûr ?',
                    message='Vous allez supprimez un filtre'):
            if DEBUG:
                print('oui')
            del liste_des_filtres[index_filtre]
            liste_des_filtres.sort(key=lambda filtre: filtre.name)
            writefiltres(liste_des_filtres)
            clear(fenetre)
            barre_de_menu(lm_filtre, menu)
            mess = 'Le filtre a été supprimé'
            barre_de_message(mess, messager)

    clear(fenetre)
    var_pointH_min, var_pointH_max = scale_couple(fenetre, 'Points H', 0, 40)
    var_HLD_min, var_HLD_max = scale_couple(fenetre, 'Points HLD', 1, 58)
    pique_min, pique_max = scale_couple(fenetre, 'Nombre de piques', 2)
    coeur_min, coeur_max = scale_couple(fenetre, 'Nombre de coeurs', 3)
    carreau_min, carreau_max = scale_couple(fenetre, 'Nombre de carreaux', 4)
    trefle_min, trefle_max = scale_couple(fenetre, 'Nombre de trèfles', 5)
    name = tk.StringVar(fenetre)
    tk.Label(fenetre, text='Nom du filtre').grid(row=10, column=0)
    tk.Entry(fenetre, textvariable=name).grid(row=10, column=1)
    if isinstance(index_filtre, int):
        selection = liste_des_filtres[index_filtre]
        name.set(selection.name)
        init_vars(selection)
        lm_regler_filtre = [['Sauvegarder', conclure],
                            ['Supprimer', supprimer],
                            ['Annuler', annuler]
                            ]   
    else:
        var_pointH_max.set(40)
        var_HLD_max.set(58)
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
        if DEBUG:
            print("validation")
        try:
            index_filtre, = menu_deroulant.curselection()
            clear(fenetre)
            c_regler_filtre(index_filtre)
        except ValueError:
            mess = 'Choisir le filtre à modifier'
            barre_de_message(mess, messager)
        # c_regler_filre()

    def annuler():
        clear(fenetre)
        barre_de_menu(lm_filtre, menu)

    if DEBUG:
        print('modifier filtre')
    clear(fenetre)
    defilement = tk.Scrollbar(fenetre, orient='vertical')
    defilement.grid(row=1, column=1, sticky='ns')
    lab = tk.Label(fenetre, text='Choisir le filtre à modifier')
    lab.grid(row=0, column=0)
    noms_de_filtres = [f.name for f in liste_des_filtres]
    menu_deroulant = tk.Listbox(fenetre,
                                yscrollcommand=defilement.set,
                                height=15,
                                width=35
                                )
    defilement.configure(command=menu_deroulant.yview)
    menu_deroulant.bind("<Double-Button-1>", validate)
    menu_deroulant.grid(row=1, column=0)
    for nom in noms_de_filtres:
        menu_deroulant.insert(tk.END, nom)
    barre_de_validation(menu, validate, annuler)


lm_filtre = [[' Nouveau filtre', c_regler_filtre],
             ['Modifier filtre', c_modifier_filtre],
             [],
             ["Gérer les séquences", c_sequence],
             [],
             ['Menu principal', c_retour],
             ["Quitter", c_quit]
             ]
################################################################
#                  MENU ENCHERES
################################################################


def initialise_encheres():
    global donne_actuelle
    clear(fenetre)
    fenetre_donne = tk.Frame(fenetre, height=100)
    fenetre_donne.grid(row=1, columnspan=4)
    visible = position_active.visibilite()
    if DEBUG:
        print(visible)
    if pack_actif:
        donne_actuelle = Donne(identifiant=pack_actif[0])
    else:
        mess = "Aucune donne n'a été chargée"
        barre_de_message(mess, messager)
    donne_active = Donne_active(donne_actuelle, fenetre_donne, visible)
    donne_active.affiche()
    widgets_actifs["donne_active"] = donne_active

    def select_position():
        global position_active
        position_active = Position(varRad.get())
        if DEBUG:
            print(position_active)
        donne_active.visible = position_active.visibilite()
        donne_active.affiche()

    varRad = tk.IntVar(fenetre)
    varRad.set(position_active+0)
    boutons_de_position_des_encheres = []
    for pos in Position:
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
    if DEBUG:
        print(widgets_actifs)
    mess = 'Choisir son orientation'
    barre_de_message(mess, messager)


def c_choisir_position():
    if widgets_actifs['BDPDE'][0].cget('state') == 'disabled':
        for pos in Position:
            widgets_actifs['BDPDE'][pos].configure(state='normal')
    else:
        for pos in Position:
            widgets_actifs['BDPDE'][pos].configure(state='disabled')


def c_afficher_ligne():
    donne_active = widgets_actifs["donne_active"]
    donne_active.visible = position_active.visibilite_ligne()
    donne_active.affiche()


def c_afficher_donne():
    donne_active = widgets_actifs["donne_active"]
    donne_active.visible = [True for pos in Position]
    donne_active.affiche()


def c_donne_suivante():
    global index_pack
    if index_pack == len(pack_actif)-1:
        mess = 'Dernière donne atteinte'
        barre_de_message(mess, messager)
    else:
        donne_active = widgets_actifs["donne_active"]
        index_pack += 1
        donne = Donne(identifiant=pack_actif[index_pack])
        donne_active.visible = position_active.visibilite()
        donne_active.reconfigure(donne)
        barre_de_message(f'Enchérir la donne n°{index_pack}', messager)


def c_donne_precedente():
    global index_pack
    if index_pack < 2:
        mess = 'Début de paquet'
        barre_de_message(mess, messager)
    else:
        donne_active = widgets_actifs["donne_active"]
        index_pack -= 1
        donne = Donne(identifiant=pack_actif[index_pack])
        donne_active.visible = position_active.visibilite()
        donne_active.reconfigure(donne)
        barre_de_message(f'Enchérir la donne n°{index_pack}', messager)


def c_archiver_donne():
    mess = 'Fonctionnalité non disponible dans cette version'
    barre_de_message(mess, messager)


lm_enchere = [['Choisir Position', c_choisir_position],
              ['Afficher Ligne', c_afficher_ligne],
              ['Afficher donne', c_afficher_donne],
              ['Donne suivante', c_donne_suivante],
              ['Donne précédente', c_donne_precedente],
              ['Archiver', c_archiver_donne],
              [],
              ["Gérer les donnes", c_gestion_donne],
              [],
              ['Menu principal', c_retour],
              ["Quitter", c_quit]
              ]
lm_enchere_rapide = [['Choisir Position', c_choisir_position],
                     ['Afficher Ligne', c_afficher_ligne],
                     ['Afficher donne', c_afficher_donne],
                     ['Donne suivante', c_donne_suivante],
                     ['Donne précédente', c_donne_precedente],
                     [],
                     ['Menu principal', c_retour]
                     ]

################################################################
#                  MENU SEQUENCES
################################################################


def c_choisir_sequence():
    ''' Choix de la séquence active '''
    def postaction():
        barre_de_menu(lm_sequence, menu)
        barre_de_message(f'Séquence active : {sequence_active.name}', messager)
        clear(fenetre)

    if liste_des_sequences:
        clear(fenetre)
        _selectionne_sequence(postaction)

    else:
        clear(fenetre)
        tk.Label(fenetre, text="Attention !").grid()
        tk.Label(fenetre, text="Aucune séquence sauvegardées !").grid()
        tk.Label(fenetre, text="Veuillez en créer une nouvelle !").grid()


def _selectionne_sequence(postaction):
    def validate(event=None):
        global sequence_active
        if DEBUG:
            print("Validation sequence")
        try:
            index_sequence, = menu_deroulant.curselection()
        except ValueError:
            barre_de_message('Sélectionnez une séquence', messager)
            return None
        sequence_active = liste_des_sequences[index_sequence]
        postaction()

    def escape(event=None):
        if expert :
            barre_de_menu(lm_sequence, menu)
            clear(fenetre)
        else :
            barre_de_menu(lm_proto_menu, menu)
            clear(fenetre)

    if DEBUG:
        print('chosir sequence')
    defilement = tk.Scrollbar(fenetre, orient='vertical')
    defilement.grid(row=1, column=2, sticky='ns')
    lab = tk.Label(fenetre, text='Choisir la séquence active')
    lab.grid(row=0, column=0, columnspan=2)
    noms_de_sequences = [seq.name for seq in liste_des_sequences]
    menu_deroulant = tk.Listbox(fenetre,
                                yscrollcommand=defilement.set,
                                height=15,
                                width=35
                                )
    defilement.configure(command=menu_deroulant.yview)
    menu_deroulant.bind("<Double-Button-1>", validate)
    menu_deroulant.grid(row=1, column=0, columnspan=2)
    for nom in noms_de_sequences:
        menu_deroulant.insert(tk.END, nom)
    #mini = tk.Frame(fenetre).grid(row=2, column=0)
    barre_de_validation(menu, validate, escape)


def c_modifier_sequence():
    ''' Modification de la séquence active '''
    if DEBUG:
        print('modifier séquence')
    clear(fenetre)
    _selectionne_sequence(_modification)


def _modification():
    def postaction():
        ''' Actions à effectuer en sortie '''
        name = saisie.get()
        if DEBUG:
            print("sortie:", saisie.get())
        name_actif = sequence_active.name
        names = [seq.name for seq in liste_des_sequences]
        names = [n for n in names if n != name_actif]
        if name:
            if name in names:
                barre_de_message('Ce nom existe déjà', messager)
            else:
                barre_de_message('Séquence validée', messager)
        else:
            barre_de_message('Entrez un nom de séquence', messager)
            return None
        if sequence_active.is_invalide():
            mess = 'Filtres incompatibles'
            barre_de_message(mess, messager)
        else :    
            sequence_active.name = name
            barre_de_menu(lm_sequence, menu)
            liste_des_sequences.sort(key=lambda seq: seq.name)
            writesequences(liste_des_sequences)
            clear(fenetre)

    def annul():
        barre_de_menu(lm_sequence, menu)
        clear(fenetre)

    barre_de_validation(menu, postaction, annul)
    saisie = regler_sequence(sequence_active, fenetre, messager)
    # La suite est envoyée dans séquence par le biais de postaction
    # ou annul


def _supprimer_sequence(sequence):
    global liste_des_sequences
    name = sequence.name
    for i in range(len(liste_des_sequences)):
        if liste_des_sequences[i].name == name:
            index = i
    del liste_des_sequences[index]


def c_nouvelle_sequence():
    ''' Crée une nouvelle séquence de filtres'''
    def postaction():
        global sequence_active
        ''' Actions à effectuer en sortie '''
        names = [seq.name for seq in liste_des_sequences]
        name = saisie.get()
        if name in names:
            mess = "Ce nom existe déjà !"
            barre_de_message(mess, messager)
        elif name == "":
            mess = 'Entrez un nom de séquence'
            barre_de_message(mess, messager)
        elif sequence.is_invalide():
            mess = 'Filtres incompatibles'
            barre_de_message(mess, messager)
        else:
            sequence.name = name
            sequence_active = sequence
            barre_de_menu(lm_sequence, menu)
            liste_des_sequences.append(sequence)
            liste_des_sequences.sort(key=lambda seq: seq.name)
            writesequences(liste_des_sequences)
            clear(fenetre)

    def annul():
        barre_de_menu(lm_sequence, menu)
        clear(fenetre)

    clear(fenetre)
    sequence = Sequence()
    barre_de_validation(menu, postaction, annul)
    saisie = regler_sequence(sequence, fenetre, messager)
    # La suite eszt envoyée dans séquence par le biais de postaction


def c_reinitialiser_sequences():
    global liste_des_sequences
    clear(fenetre)
    tk.Label(fenetre, text="Attention !").grid()
    tk.Label(fenetre, text="Vous allez effacer les séquences !").grid()
    tk.Label(fenetre, text="En cas de Bug uniquement !").grid()
    if askyesno(title='EFFACEMENT DES SEQUENCES',
                message='Continuer ?',
                parent=menu):
        liste_des_sequences = []
        writesequences(liste_des_sequences)
    clear(fenetre)


def c_supprimer_sequence():
    ''' Choix de la séquence active puis supression'''
    def postaction():
        global sequence_active
        barre_de_menu(lm_sequence, menu)
        _supprimer_sequence(sequence_active)
        writesequences(liste_des_sequences)
        barre_de_message(f'{sequence_active.name} effacée', messager)
        sequence_active = None
        clear(fenetre)

    if liste_des_sequences:
        clear(fenetre)
        _selectionne_sequence(postaction)

    else:
        clear(fenetre)
        tk.Label(fenetre, text="Attention !").grid()
        tk.Label(fenetre, text="Aucune séquence sauvegardées !").grid()
        tk.Label(fenetre, text="Veuillez en créer une nouvelle !").grid()


lm_sequence = [['Choisir séquence', c_choisir_sequence],
               ['Modifier séquence', c_modifier_sequence],
               ['Nouvelle séquence', c_nouvelle_sequence],
               ['Supprimer séquence', c_supprimer_sequence],
               [],
               ["Gérer les filtres", c_gestion_filtre],
               ["Gérer les donnes", c_gestion_donne],
               [],
               ['Menu principal', c_retour],
               ["Quitter", c_quit]
               ]

if DEBUG:
    lm_sequence.append(['Réinitialiser', c_reinitialiser_sequences])


################################################################
#       LANCEMENT DE L'INTERFACE
################################################################

root = tk.Tk()
root.title('Utilitaire pour bridgeur')
tkcolors.palette(root)

menu = tk.Frame(root)
menu.grid(row=0, column=0, sticky='n')
root.columnconfigure(0, weight=1)

fenetre = tk.Frame(root)
fenetre.grid(row=0, column=1)
root.columnconfigure(1, weight=3)

messager = tk.Frame(root)
messager.grid(row=1, columnspan=2)
mess = tk.Label(messager, text="Démarrage")
mess.grid(sticky='ew')

if DEBUG:
    print('boucle')
# menu_principal()
proto_menu()
root.protocol("WM_DELETE_WINDOW", c_quit)
root.mainloop()

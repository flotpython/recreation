#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 20 12:16:13 2018

@author: hubert
"""
import pickle

DEBUG = False

def readfiltres():
    ''' Lire la liste des filtres sauvegardée '''
    filename='data/filtres.fil'
    if DEBUG :
        print("readfiltes", filename)
    with open(filename,"rb") as fichier :
        return pickle.load(fichier) 
            
def writefiltres(filtres) :
    ''' Sauvegarder la liste des séquences de filtres '''
    filename='data/filtres.fil'
    if DEBUG :
        print("writefiltes", filename)
    with open(filename,"wb") as fichier :
        pickle.dump(filtres,fichier) 
        
def readsequences():
    ''' Lire la liste des séquences de filtres sauvegardée '''
    filename='data/sequences.fil'
    if DEBUG :
        print("readsequences", filename)
    with open(filename,"rb") as fichier :
        return pickle.load(fichier) 
            
def writesequences(sequences) :
    ''' Sauvegarder la liste des séquences de filtres'''
    filename='data/sequences.fil'
    if DEBUG :
        print("writesequences", filename)
    with open(filename,"wb") as fichier :
        pickle.dump(sequences,fichier)         
        
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 14:43:39 2018

@author: hubert
"""

from bridgelib import Donne, Filtre, Position

class Filtres:
    ''' Groupe de filtres pour une Donne '''
    def __init__(self):
        self.positif = [[] for positionn in Position]
        self.negatif = [[] for positionn in Position]
        self.name    = 'My name is nobody'
        
    def set_filtre(self, position, filtre, normal = True):
        if normal :
            self.positif[position].append(filtre)
        else :
            self.negatif[position].append(filtre)
            
    def set_name(self, name):
        self.name = name
        
            
    def filtre(self, donne) :
        ''' AAppliacation des filtres à une donne, 
        Renvoie True si la donne satisfait le groupe de filtres '''
        
        for position in Position:
            for filtre in self.positif[position]:
                if not filtre.filtre(donne[position]):
                    return False
        for position in Position:
            for filtre in self.positif[position]:
                if filtre.filtre(donne[position]):
                    return False 
        return True        
                
                
        
            
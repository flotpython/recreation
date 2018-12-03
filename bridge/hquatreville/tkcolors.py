#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:30:49 2018

@author: hubert
"""

############################################################################
# COLOR CHART
############################################################################

#  Couleurs de Vulnérabilité dans les diagrammes
VERT = "spring green"  # provision pour retour en arrière
ROUGE = "tomato"
VERT = "#82C47E"      # compatibilité

#   Thème généré avec coolors
THEME5 = "#F1E3F3"   # gris marron pastel
THEME2 = "#82C47E"   # Vert clair
THEME3 = "#8FB8ED"
THEME4 = "#EFE9E7"   # Gris
THEME1 = "#C2BBF0"   # violet clair


def palette(root):
    root.tk_setPalette(background=THEME4,
                       activeBackground=THEME2,
                       selectBackground=THEME3,
                       selectColor=THEME5,
                       disabledForegroud=THEME3
                       )

###########################################################################
# Couleurs en réserve pour remplacer THEME3 au cas où, inutilisées en l'éta


ALTERNATE2 = "#CAD2C5"
ALTERNATE3 = "#8DA7BE"
ALTERNATE1 = "#8FB8ED"
ALTERNATE4 = "#B4B8AB"

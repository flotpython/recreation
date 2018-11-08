#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 09:12:59 2018

@author: hubert
"""

import bridgelib as bl


filtres = {}   #liste des filtres

''' Juste quelques filtres simples pour le moment à étendre'''


def _init_filtres():    
    filtres["1P"] = bl.Filtre("1P", pointH_min = 10, pique_min =5,
           points_totaux_min = 13)
    filtres["1C"] = bl.Filtre("1C", pointH_min = 10, coeur_min =5,
           points_totaux_min = 13)
    filtres["1TK"] = bl.Filtre("1TK", pointH_min = 10, coeur_max =4,
           pique_max = 4, points_totaux_min = 13)
    filtres["1SA"] = bl.Filtre("1SA", pointH_min = 14, pointH_max=18,
           trefle_min=2,carreau_min =2, coeur_min =2, pique_min=2)
    filtres["1SAfaible"] = bl.Filtre("1SAfaible", pointH_min = 11, pointH_max=14,
           trefle_min=2,carreau_min =2, coeur_min =2, pique_min=2)  
    
_init_filtres()    


#########################################################################
###        TEST DIVERS                                                ###
#########################################################################

    
    
 
                      
#test={0,5,12,15,16,21,51,18,32,45,17,50}
#main = decode_main(test) 
#main.affiche()   
#vérification de la réversibilkité de code et decode  
donne=bl.Donne()        
donne.affiche()    
donne._code()
donne._decode()
donne.affiche()  

#vérification de l'identifiant
donne=bl.Donne()
donne.affiche()
print(donne.identifiant())
mon_id=donne.identifiant()
donne1=bl.Donne(identifiant=mon_id)
donne1.affiche()
donne1=bl.Donne(identifiant='0xb29f79e11ca17a9c0dd60f3069a')
donne1.affiche()

print(donne1.sud.vertues())
print(donne1.est.vertues())
print(donne1.ouest.vertues())
print(donne1.nord.vertues())

piques = bl.Longueur((1,4,6,10,11))
print(len(piques))

 # Test des filtres
donne = bl.Donne()
compteur = 0
print("1P en sud")
while not (filtres["1P"].filtre(donne.sud) or compteur > 200):
    donne = bl.Donne()
    compteur += 1
    print("essai", compteur)
donne.affiche()   
 
donne = bl.Donne()
compteur = 0
print("1C en sud")
while not (filtres["1C"].filtre(donne.sud) or compteur > 200):
    donne = bl.Donne()
    compteur += 1
    print("essai", compteur)
donne.affiche()    

donne = bl.Donne()
compteur = 0
print("1mineur en sud")
while not (filtres["1TK"].filtre(donne.sud) or compteur > 200):
    donne = bl.Donne()
    compteur += 1
    print("essai", compteur)
donne.affiche()                
                
                
donne = bl.Donne()
compteur = 0
print("1SA fort en sud")
while not (filtres["1SA"].filtre(donne.sud) or compteur > 200):
    donne = bl.Donne()
    compteur += 1
    print("essai", compteur)
donne.affiche()       
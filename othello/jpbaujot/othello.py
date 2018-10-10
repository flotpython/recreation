# -*- coding: utf-8 -*-

# pour dire à pylint de ne pas vérifier la présence des docstring
# pylint: disable=c0111
# vérifier avec
# $ pip3 install pylint
# $ pylint othello.py
# il reste quelques identificateurs qui ne sont pas casher, je vous laisse
# choisir de les rectifier ou pas

#@parmentelat : dans une version déjà modifiee (simplifiée en code) , j'ai pris en compte vos suggestions sur les adjacents et le test d'appartenance
#mais je ne sais pas ce que vous entendez par identificateurs pas casher : pouver vous préciser les lignes concernées

# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 21:07:27 2018
Evolutions avec prise en compte compteur et fin de jeu , mais reste à debugguer ...
@author: JP
"""
import numpy as np
class Grille :
    # classe pour gerer la grille
    def __init__(self) :
        self.tableau = np.zeros((8,8))
        self.tableau[3][3], self.tableau[4][4]=1,1
        self.tableau[3][4], self.tableau[4][3]=2,2
        self.pions = [". ","O ","X "]
        
    
    def __str__(self):
        nom_col = "  A B C D E F G H\n"
        msg = "\n"+ nom_col       
        for i in range(8):            
            msg+=f"{i+1} "
            for j in range(8):
                msg+=self.pions[int(self.tableau[i][j])]                       
            msg+=f" {i+1}\n"
        msg += nom_col
        return msg
    
    @staticmethod
    def adjacents():
        #liste des cases ajdacentes en relatif
        return [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy] 
    
    def pose_test(self,forme,ligne,colonne) :        
        #verifie si pose d'un pion forme permet ou pas de retouner 
        #des pions del'autre forme et renvoie booleen sur la pose possible
        # et un  tableau des nombre de pions retournes 
        listeRetournables =[0,0,0,0,0,0,0,0]
        #teste case jouee non vide        
        if int(self.tableau[ligne][colonne]) :
            print("erreur : case non vide")
            return False,listeRetournables        
         
          
        for idx,(dx,dy) in enumerate(self.adjacents()) :
            if not self.test_case(ligne+dx, colonne+dy):# case adj hors grille
                continue
            formeAdjacent = self.tableau[ligne+dx][colonne+dy]
            if not formeAdjacent==3-forme: #case adj vide ou meme couleur
                continue
            
            # case adj de couleur differente, on teste les cases audelà ds cette direction
            i=2 
            while self.test_case (ligne+i*dx,colonne+i*dy):
                formeAdjacent = self.tableau[ligne+i*dx][colonne+i*dy]
                if formeAdjacent ==0 :# on tombe sur case vide = mauvaise direction
                    break # on regarde les autres cases adjacentes
                if formeAdjacent == forme :
                    listeRetournables[idx]=i-1 
                    break # on regarde les autres cases adjacentes
                i+=1 # on continue dans la direction
           
        ## Retourne True si on peut  retourner des pions False sinon, + liste contenant les pions retournables       
        return (sum(listeRetournables)>0),listeRetournables 
    
    def pose(self,forme,ligne,colonne) :        
        #verifie si pose d'un pion forme permet ou pas de retouner 
        #des pions del'autre forme , retourne les pions si possibles et retourne 
        #un booleen pour dire si le tableau a été modifié ou pas
       
        result,listeRetournables = self.pose_test(forme,ligne,colonne)
        if result : ## remplit les cases du tableau  
            for idx,(dx,dy) in enumerate(self.adjacents()) : 
                for j in range(listeRetournables[idx]+1):
                    self.tableau[ligne+j*dx][colonne+j*dy] = forme                
         
        return result
    
    
    def test_case(self,x,y):
        # teste si une case est bien dans la grille
        return not (x<0 or x>7 or y<0 or y>7)   

    
    
    def partie_terminee (self):
        # teste si toutes cases occupées : aucune case à 0 ou jeu bloqué pour les 2
        return  self.tableau_rempli() or self.jeu_bloque()

    
    def jeu_bloque(self):
        # teste si les 2 joueurs sont bloqués
        return not (self.teste_pose_possible(1) or self.teste_pose_possible(2)) 
        
    def teste_pose_possible(self,forme):
        # renvoie le nombre de pions retournables sur l'ensemble de la grille pour une couleur(forme) donnée
        return (sum([self.pose_test(forme,i,j)[0]\
                for i in range(8) for j in range(8)\
                if not self.tableau[i][j]]))
    
    def tableau_rempli(self) :
        # verifie si le tableau est bien rempli
        return (np.count_nonzero(self.tableau == 0)==0)
    
    def compte_formes(self):
        # renvoie un tuple des nombres de croix et de ronds
        return np.count_nonzero(self.tableau == 1), np.count_nonzero(self.tableau == 2)
        
class Jeu :
    def __init__(self) :
         self.grille = Grille()
         print(self.grille)
         self.colonnes = ['A','B','C','D','E','F','G','H']
         self.lignes = [str(i+1) for i in range(8)]
         self.joueur = ["Rond","Croix"]
         
    def partie(self):
        #partie principale
        forme = 2 # les X commencent
        condstop = False
        while not self.grille.partie_terminee() and not condstop:
            totalRond,totalCroix = self.grille.compte_formes()
            
            print (f"Compteur : Rond = {totalRond} Croix = {totalCroix} ")
            
            while True :
                #teste si le joueur a une case possible pour poser sa forme
                #presque le meme code que pose en testant toutes les cases à 0 
                # mais sans modifier
                
                if not self.joue_test(forme):
                    forme = 3-forme
                    break
                
                # saisie case valide
                case = self.entree_valide(forme)
                # condition arret
                if case =='00':
                    condstop = True
                    break
                
                #transcrit la saisie en ligne colonne du tableau
                idxlign, idxcol = case[1],case[0].upper()
                ligne = self.lignes.index(idxlign)                
                colonne = self.colonnes.index(idxcol)
                
                # test si case permet de retourner des pions 
                if self.joue (forme,ligne,colonne):
                    forme = 3-forme # changement de joueur                    
                    break 
                    
        totalRond,totalCroix = self.grille.compte_formes() 
        print (f"Compteur final : Rond = {totalRond} Croix = {totalCroix} ")
        
    def entree_valide(self,forme) : 
        # teste la validite de la saisie des cases par les joueurs
        while True :
            case = input(f"Joueur {self.joueur[forme-1]} quelle case(ex: A4 ? (00 pour arreter) ")
            if not len(case)==2  :
                print ("ce n'est pas une case valide")
                continue
            if case =='00': # condition sortie 
                print("OK on arrete")
                return case
                
            if case[0].upper() not in self.colonnes or case[1] not in self.lignes :
                print ("ce n'est pas une case valide")
                continue
            return case
                 
            
         
    def joue (self,forme,ligne,colonne) : 
        # verifie si la case choisie permet de poser un pion et si oui retourne les pions autre forme
        if self.grille.pose(forme,ligne,colonne) : # verifie pose possible et retourne les pions
            print (self.grille)
            return True
        else :
            print ("rejouez case non autorisée pour vous")
            return False
        
    def joue_test(self,forme) :         
        # verifie la possibilité de poser du joueur sinon passera son tour
        if self.grille.teste_pose_possible(forme): #verifie qu'au moins une case peut etre jouee
            return True
                   
        print (f"Joueur {self.joueur[forme-1]} ne peut jouer")    
        return False      
   
        
jeu = Jeu() 
jeu.partie()


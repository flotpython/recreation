# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 21:07:27 2018

@author: JP
"""
import numpy as np
class Grille :
    
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


    
    def pose(self,forme,ligne,colonne) :        
        #verifie si pose d'un pion forme permet ou pas de retouner 
        #des pions del'autre forme
        
        #teste case jouee non vide        
        if int(self.tableau[ligne][colonne]) :
            print("erreur : case non vide")
            return False
        
        # init retour à False si pas de pions retournables      
        retour = False
        
        ## tuples des cellules adjacentes possibles en relatifs
        adj = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        for dx,dy in adj :
            if not self.testcase(ligne+dx, colonne+dy):# case adj hors grille
                continue
            formeadj = self.tableau[ligne+dx][colonne+dy]
            if not formeadj==3-forme: #case adj vide ou meme couleur
                continue
            i=2 # case couleur differente
            while self.testcase (ligne+i*dx,colonne+i*dy):
                formeadj = self.tableau[ligne+i*dx][colonne+i*dy]
                if formeadj ==0 :# on tombe sur case vide = mauvaise direction
                    break # on regarde les autres cases adjacentes
                if formeadj == forme :
                    self.remplitcases(ligne,colonne,i,dx,dy,forme)
                    retour = True # on a retourne des pieces
                    break # on regarde les autres cases adjacentes
                i+=1 # on continue dans la direction
        return retour # True si on a retourné des pions False sinon
    
    def testcase(self,x,y):
        # teste si une case est bien dans la grille
        if x<0 or x>7 or y<0 or y>7 :
            return False
        return True
    
    def remplitcases(self,ligne,colonne,i,dx,dy,forme):
        # remplit les cases qu'on peut retourner dans la direction validee
        for j in range(i):
            self.tableau[ligne+j*dx][colonne+j*dy] = forme
    
    
    def partie_terminee (self):
        # teste si toutes cases occupées : aucune case à 0
        if self.tableaurempli() :
            return True        
        # si possibilité existe sur les cases occupées : teste chaque case à 0 
        # pour voir si une forme peut etre posée avec succés , attention à
        # ne pas modifier les cases ..... va necessiter de la reprise de code
        # 
        return False
    
    def tableaurempli(self) :
        # verifie si le tableau est bien rempli
        for i in range(8) :
            for j in range (8):
                if int(self.tableau[i][j]) ==0 :            
                    return False
        return True
    
    def compteformes(self):
        # renvoie un tuple des nombres de croix et de ronds
        pass
    
        
class Jeu :
    def __init__(self) :
         self.grille = Grille()
         print(self.grille)
         self.colonnes = ['A','B','C','D','E','F','G','H']
         self.lignes = [str(i+1) for i in range(8)]
         self.joueur = ["Rond","Croix"]
         
    def partie(self):
        forme = 1 # les O commencent
        condstop = False
        while not self.grille.partie_terminee() and not condstop:
            while True :
                # saisie case valide
                case = self.entreevalide(forme)
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
                    # ici il faudrait un compteur des formes X et O
                    forme = 3-forme # changement de joueur
                    print(forme)
                    break 
            
    def entreevalide(self,forme) : 
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
        
        if self.grille.pose(forme,ligne,colonne) : # verifie pose possible
            print (self.grille)
            return True
        else :
            print ("rejouez case non autorisée pour vous")
            return False
          
        
        
jeu = Jeu() 
jeu.partie() 

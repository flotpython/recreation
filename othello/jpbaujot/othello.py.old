# -*- coding: utf-8 -*-

# pour dire à pylint de ne pas vérifier la présence des docstring
# pylint: disable=c0111
# vérifier avec
# $ pip3 install pylint
# $ pylint othello.py
# il reste quelques identificateurs qui ne sont pas casher, je vous laisse
# choisir de les rectifier ou pas

#@parmentelat : dans une version déjà modifiee (simplifiée en code) , 
#j'ai pris en compte vos suggestions sur les adjacents et le test d'appartenance
#mais je ne sais pas ce que vous entendez par identificateurs pas casher : 
#pouver vous préciser les lignes concernées

# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 21:07:27 2018

@author: JP
"""
import numpy as np

CROIX = 'Croix'
ROND = 'Rond'
formes = [CROIX,ROND]

class Grille :
    # classe pour gerer la grille
    colonnes = ['A','B','C','D','E','F','G','H']
    lignes = [str(i+1) for i in range(8)] 
    
    def __init__(self) :
        self.tableau = np.zeros((8,8))
        self.tableau[3][3], self.tableau[4][4]=2,2
        self.tableau[3][4], self.tableau[4][3]=1,1
        self.pions = [". ","X ","O "]        
    
    def __str__(self): 
        nom_col = "  "+" ".join(self.colonnes)+"\n"
        msg = "\n"+ nom_col       
        for i in range(8):            
            msg+=f"{i+1} "
            for j in range(8):
                msg+=self.pions[int(self.tableau[i][j])]                       
            msg+=f"{i+1}\n"
        msg += nom_col
        return msg
    
    @staticmethod
    def adjacents():
        #liste des case_tab ajdacentes en relatif
        return [(delta_x, delta_y) for delta_x in (-1, 0, 1)\
                for delta_y in (-1, 0, 1) if delta_x or delta_y] 
 
    def pose_test(self,forme,case_tab) :        
        #intreface pour transformer les coordonnées de l'interface utilisateur 
        # en coordonnées utilisables dans les fonctions internes de la classe
        ligne = self.lignes.index(case_tab[1])                
        colonne = self.colonnes.index(case_tab[0])
        return self.pose_test_int(forme,ligne,colonne)        
        
    def pose_test_int(self,forme,ligne,colonne) :
        #verifie si pose d'un pion forme permet ou pas de retouner 
        #des pions del'autre forme et renvoie booleen sur la pose possible
        # et un  tableau des nombre de pions retournables 
        
        tab_retournables =np.zeros((8))
        #teste case_tab jouee non vide        
        if int(self.tableau[ligne][colonne]) :            
            return False,tab_retournables 
          
        for idx,(delta_x,delta_y) in enumerate(self.adjacents()) :
            # case_tab adj hors grille ?
            if not self.test_case_tableau(ligne+delta_x, colonne+delta_y):
                continue
            form_adj = self.tableau[ligne+delta_x][colonne+delta_y]
            if not form_adj==3-forme: #case_tab adj vide ou meme forme
                continue
            
            # case_tab adj de forme differente, 
            # on teste les case_tab audelà ds cette direction
            i=2 
            while self.test_case_tableau (ligne+i*delta_x,colonne+i*delta_y):
                form_adj = self.tableau[ligne+i*delta_x][colonne+i*delta_y]
                # on tombe sur case_tab vide = mauvaise direction
                if form_adj ==0 :
                    break # on regarde les autres case_tab adjacentes
                if form_adj == forme :
                    tab_retournables[idx]=i-1 
                    break # on regarde les autres case_tab adjacentes
                i+=1 # on continue dans la direction
           
        # Retourne True si on peut  retourner des pions False sinon, 
        # + liste contenant les pions retournables       
        return (sum(tab_retournables)>0),tab_retournables     
    
    def pose(self,forme,case_tab) :        
        #verifie si pose d'un pion forme permet ou pas de retouner 
        #des pions del'autre forme , retourne les pions si possibles et retourne 
        #un booleen pour dire si le tableau a été modifié ou pas
        ligne = self.lignes.index(case_tab[1])                
        colonne = self.colonnes.index(case_tab[0])         
        
        result,tab_retournables = self.pose_test_int(forme,ligne,colonne)
        if result : ## remplit les case_tab du tableau  
            for idx,(delta_x,delta_y) in enumerate(self.adjacents()) : 
                for j in range(int(tab_retournables[idx])+1):
                    self.tableau[ligne+j*delta_x][colonne+j*delta_y] = forme 
        return result
    
    def test_case_tableau(self,ligne,colonne):
        # teste si une case_tab est bien dans la grille
        return 0<=ligne<=7 and  0<=colonne<=7
    
    def partie_terminee (self):
        # teste si toutes case_tab occupées : 
        #aucune case_tab à 0 ou jeu bloqué pour les 2
        return  self.tableau_rempli() or self.jeu_bloque()
    
    def jeu_bloque(self):
        # teste si les 2 JoueurHumains sont bloqués
        return not (self.teste_pose_possible(1) or self.teste_pose_possible(2)) 
    
    def teste_pose_possible(self,forme):
        # renvoie le nombre de pions retournables sur l'ensemble de la grille 
        #pour une forme(forme) donnée
        return (sum([self.pose_test_int(forme,i,j)[0]\
                for i in range(8) for j in range(8)\
                if not self.tableau[i][j]]))
                    
    def tableau_rempli(self) :
        # verifie si le tableau est bien rempli
        return np.count_nonzero(self.tableau == 0)==0
    
    def compte_formes(self):
        # renvoie un tuple des nombres de croix et de ronds
        totalCroix = np.count_nonzero(self.tableau == 1)
        totalRond = np.count_nonzero(self.tableau == 2)
        return f"Croix = {totalCroix} Rond = {totalRond} "

    def case_retournable(self,forme, ligne, colonne):
        #teste si case peut etre retournee  au tour  suivant
        #necessite une deeepcopie de la grille pour poser pion 
        #puis chercher une solution de retournement
        pass
    
    def simulation(self,forme):
        # teste pour chaque case jouable , l'impact des meilleurs coups adv 
        #dans les x tours suivants, et par ex de pouvoir jouer au coup suivant
        #necessite -t il de mémoriser des objets grilles et de regarder toute la
        #combinatoire des jeux possibles ?
        pass
        
        
class Jeu :
    def __init__(self) :
         self.grille = Grille()
         print(self.grille)
         # version avec choix AI ou Humain pour les 2 joeurs 
         self.Joueurs=[] # tableau des instances de Joueur

         for forme in [CROIX,ROND] :
             saisie = self.saisieJoueurValide(forme)
             JoueurChoisi = JoueurHumain(forme) if saisie == '0' else JoueurAI(forme)
             self.Joueurs.append(JoueurChoisi)
    
    def saisieJoueurValide(self,forme) :
        "verifie que le joueur choisi est bien dans les choix proposés "
        msg = forme +('s'if forme==ROND else '')
      
        while True :
             saisie = input(f"Qui joue les {msg} ? Humain =0 ou AI = 1  ")
             if  len(saisie)==1 and saisie  in '01':
                 break
             print("saisie invalide")
        
        return saisie
         
    def partie(self):
        #partie principale
        indexJoueur = 0 # les X commencent
        condstop = False
        while not self.grille.partie_terminee() and not condstop:
            print (f"Compteur :"+self.grille.compte_formes())
            
            joueur = self.Joueurs[indexJoueur]
            #verifie si pose pion possible pour le joueur
            if not joueur.joue_test(self):
                indexJoueur = 1-indexJoueur
                continue 
            
            if joueur.joue() :
                print (self.grille)
                indexJoueur = 1-indexJoueur                
                continue
            condstop = True
            
        print (f"Compteur final :"+self.grille.compte_formes())
 

class Joueur :    
    colonnes = ['A','B','C','D','E','F','G','H']
    lignes = [str(i+1) for i in range(8)]   

    def __init__(self,formeWord) :
         self.formeWord = formeWord
         self.forme = formes.index(formeWord)+1  
         
    def joue_test(self,jeu) :         
        # verifie la possibilité de poser du Joueur sinon passe son tour 
        # méthode commune aux 2 types de joueurs
        if jeu.grille.teste_pose_possible(self.forme):       
            return True
                   
        print (f"Joueur {self.formeWord} ne peut jouer")    
        return False    

class JoueurHumain(Joueur) :

    def __init__(self, formeWord):        
        Joueur.__init__(self, formeWord)

    def entree_valide(self,forme) : 
        # renvoie une saisie autorisée de la case ex A4 ou de l'arret 00
        
        while True :
            case_tab = input(f"Joueur {self.formeWord} quelle case \
                                (ex: A4 ? (00 pour arreter) ").upper()
 
            case1, case2 = case_tab[0],case_tab[1]
            case_out = case1 not in self.colonnes or case2 not in self.lignes
            if len(case_tab)!=2 or (case_tab !='00' and case_out):           
                print ("ce n'est pas une case valide")
                continue
            return case_tab
         
    def joue (self) : 
        # renvoie  un booleen pion posé = True arretjeu = False         
        #  verifie une saisie correcte et retourne les pions 
            
        while True :  #saisie entree case JoueurHumain 
            case_tab = self.entree_valide(self.forme)
            
            # condition arret
            if case_tab =='00':
                print("OK on arrete")
                return False
            
            # verifie pose possible et retourne les pions
            if jeu.grille.pose(self.forme,case_tab) : 
                return True
            print ("rejouez case non autorisée pour vous")

        
class JoueurAI(Joueur) :

    def __init__(self, formeWord):        
        Joueur.__init__(self, formeWord)  
   
    def joue(self):
        # analyse les priorités essentiellement        
        return self.priorites()
    
    def priorites(self) :
        import random 
        # joue max points en priorisant coins puis  
        # autres cases sauf case adjacentes des coins et avant derniere rangee
        # puis avant derniere rangee
        # pire cas case adjacente d'un coin si retournable 
        lignes = self.lignes
        colonnes = self.colonnes
        
        tout = {y+x for x in lignes for y in colonnes }
        coins = {y+x  for x in ('18') for y in ('AH')}         
        adj_coins = {y+x  for x in ('1278') for y in ('ABGH')} -coins        
        tour =tout - {y+x for x in lignes[1:-1] for y in colonnes[1:-1] }        
        av_dern_rang = tout - tour - adj_coins \
                      - {y+x for x in lignes[2:-2] for y in colonnes[2:-2]}
                                    
        normal = tout - coins - av_dern_rang - adj_coins - tour
        dern_ligne = tour - coins - adj_coins 
        
        ensembles1 = [coins, dern_ligne,normal, av_dern_rang, adj_coins]
        ensembles = []
        
        for ensemble in ensembles1 :
            ens = list(ensemble)
            random.shuffle(ens)
            ensembles.append(list(ens)) 
            
        
        # coins prioritaires
        for ensemble in ensembles:         
            maxPions = 0
            case_max = None
            for case_tab in ensemble :
                # verifie pose possible et retourne les pions
                pose,retourne = jeu.grille.pose_test(self.forme,case_tab)  
                # il faudrait en fait regarder quelle case est meilleure 
                #vis à vis du meilleur jeu de l'adv aux x tours suivants 
                
                if sum(retourne)>maxPions :
                    maxPions = sum(retourne)
                    case_max = case_tab
            if maxPions>0:
                print(f"\nAI {self.formeWord} joue en {case_max}")
                return jeu.grille.pose(self.forme,case_max) 

    
jeu = Jeu() 
jeu.partie()


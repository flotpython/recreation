#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 14:34:46 2018

@author: hubert
"""
from random import randint,shuffle

# Impression des cartes à l'écran avec des caractères spéciaux
code_pique,code_coeur,code_carreau,code_trefle=3,2,1,0
couleur={code_trefle:'\u2663',code_carreau:'\x1b[31;1m\u2666\x1b[39;1m',\
         code_coeur:'\x1b[31;1m\u2665\x1b[39;1m',code_pique:'\u2660'}
couleurs=[code_pique,code_coeur,code_carreau,code_trefle]
valeur=['2','3','4','5','6','7','8','9','10','V','D','R','A']
# Evaluation des cartes selon les perdantes et selon les points H
honneur = [0,0,0,0,0,0,0,1,2,5,10,10,10]
pointH  = [0,0,0,0,0,0,0,0,0,1,2,3,4]
pointD  = [3,2,1,0,0,1,2,3,4,5,6,7,8,9]

class Longueur:
    ''' Une longueur dans une couleur particulière'''
    def __init__(self,cartes):
        self.cartes=set(cartes)
    def __repr__(self):
        l=list(self.cartes)
        l.sort(reverse=True)
        chaine=''
        for x in l:
            chaine += ' '+valeur[x]
        return chaine   
    def __len__(self):
        return len(self.cartes)
    def qualite(self):
        res=0
        for x in self.cartes:
            res += honneur[x]
        return res    
    def pointH (self):
        res=0
        for x in self.cartes:
            res += pointH[x]
        return res    
        
        
        

class Main:
    ''' Une Main de bridge avec les quatre couleur'''
    def __init__(self,trefle,carreau,coeur,pique):
        self.trefle=Longueur(trefle)
        self.carreau=Longueur(carreau)
        self.coeur=Longueur(coeur)
        self.pique=Longueur(pique)
        self.total=[self.trefle,self.carreau,self.coeur,self.pique]
        
    def affiche(self,decalage=0, autre_main=None):
        if autre_main:
            for c in couleurs:
                print(couleur[c],self.total[c],\
                      ' '*(26-len(str(self.total[c]))),\
                      couleur[c],autre_main.total[c])
        else:    
            for c in couleurs:
                print(' '*decalage,couleur[c],self.total[c])
    def codes(self):
        ''' Renvoie la liste des cartes de la main codées entre 0 et 51''' 
        res=[]
        for i in range(4):
            for j in self.total[i].cartes:
                res.append(i*13+j)
        #print(res)        
        return res  
    def vertues(self):
        ''' évalue la main selon les critères habituels des bridgeurs :
            0 : valeur de la main en points H
            1,2,3,4 : longueurs des 4 couleurs
            5,6,7,8 : qualité de ces couleurs
            9 : évaluation conventionnelle de la distibution D '''
        res=[]
        points = self.trefle.pointH()
        points += self.carreau.pointH()
        points += self.coeur.pointH()
        points += self.pique.pointH()
        res.append(points)
        res.append(len(self.trefle))
        res.append(len(self.carreau))
        res.append(len(self.coeur))
        res.append(len(self.pique))
        res.append(self.trefle.qualite())
        res.append(self.carreau.qualite())
        res.append(self.coeur.qualite())
        res.append(self.pique.qualite())
        distribution =  pointD[len(self.trefle)]
        distribution += pointD[len(self.carreau)]
        distribution += pointD[len(self.coeur)]
        distribution += pointD[len(self.pique)]
        res.append(distribution)
        return res
        
    
        
        
            
def decode_main(liste):
    ''' Creation d'une main à partir d'une liste de cartes codées de 0 à 51'''
    listes =[[] for i in range(4)]
    for carte in liste:
        listes[carte//13].append(carte%13)
    return Main(*listes)    
    
    
            
    
class Donne:
    donneurs = ['Nord','Sud','Est','Ouest']
    vulnerabilite = ['Personne','NS','EO','Tous']
    def __init__(self, sud = None, nord = None, est = None, ouest = None, \
                       donneur = 'Nord', vul = 'Personne', identifiant= None):
        ''' On peut créer une donne de trois façons. En entrant les quatre mains
        et optionnellement la vulnérabilité et le donneur, ou bien
        en la générant aléatoirement, ou encore en entrant un identifiant unique
        associée à chaque donne possible. Les syntaxes possibles sont
        Donne(nord=((2,5,6,10),(2,11),(0,12),(3,5,6,8,10)), sud = cartes de sud,
        est = ..., ouest = ... ) facultativement
        Donne(nord=..., sud = ..., est = ..., ouest = ..., donneur = , vul = )
        si on veut indiquer le donneur et la vulnérabilité
        Donne() pour distribuer une main aléatoirement ou
        Donne(identifiant = un nombre) pour retrouver une donne dont on a c
        onservé l'identifiant'''
        if sud :
            self.sud     = Main(*sud)
            self.nord    = Main(*nord)
            self.est     = Main(*est)
            self.ouest   = Main(*ouest)
            self.donneur = donneur
            self.vul     = vul
            self._code()
        elif identifiant: # Reconstitue la main à partir d'un identifiant unique
            self._reconstitution(identifiant)    
        else  :  
            # On distribue les cartes
            #print("distribution")
            melange = list(range(52))
            shuffle(melange)
            self.attributions=list(range(52))
            for i in range(52):
                self.attributions[melange[i]]=i//13
            self._decode()   
            i = randint(0,3)
            self.donneur=Donne.donneurs[i]
            i = randint(0,3)
            self.vul=Donne.vulnerabilite[i]
            

            
    def _decode(self):
        ''' Reconstitue les quatre mains en fonction des attributions des cartes '''
        #print("decodage")
        liste_des_mains=[[] for i in range(4)]
        for n in range(52):
            liste_des_mains[self.attributions[n]].append(n)
        self.nord=decode_main(liste_des_mains[0])
        self.sud=decode_main(liste_des_mains[2])
        self.est=decode_main(liste_des_mains[1])
        self.ouest =decode_main(liste_des_mains[3])

            
        
    def _code(self):
        ''' Attribue à chaque carte la main dans laquelle elle a été distribuée'''
        self.attributions=list(range(52))
        for x in self.nord.codes():
            #print(x,0)
            self.attributions[x]=0
        for x in self.sud.codes():
            #print(x,2)
            self.attributions[x]=2
        for x in self.est.codes():
            #print(x,1)
            self.attributions[x]=1    
        for x in self.ouest.codes():
            #print(x,3)
            self.attributions[x]=3    
        
    def identifiant(self):
        ''' Calcul de l'identifiant unique de la donne. Le résultat est 
        transformé en chaîne de caractères 
        pour transmission par des fichiers textes'''
        def code_vul(vul):
            for i in range(4):
                if Donne.vulnerabilite[i].lower()==self.vul.lower():
                    return i
            raise    NameError('problème codage vulnérabilité')
        def code_donneur(don):
            for i in range(4):
                if Donne.donneurs[i].lower()==self.donneur.lower():
                    return i
            raise    NameError('Problème codage donneur')    
            
        mon_id = 0
        att=list(self.attributions)
        att.append(code_donneur(self.donneur))
        att.append(code_vul(self.vul))
        for i in range(54):
            mon_id *=4
            mon_id += att[i]  
        return hex(mon_id)    
    
    def _reconstitution(self,identifiant):
        ''' Decodage de l'identifiant unique'''
        mon_id = int(identifiant,0)
        self.identifiant=identifiant
        self.vul = Donne.vulnerabilite[mon_id%4]
        mon_id //= 4
        self.donneur = Donne.donneurs[mon_id%4]
        mon_id //= 4
        self.attributions=[0]*52
        for i in range(52):
            self.attributions[i]=(mon_id%4)
            mon_id //= 4
        #self.attributions[0]=(mon_id%4)    
        self.attributions.reverse()
        self._verification()
        self._decode()
        
    def _verification(self):
        ''' vérification de l'intégrité d'une donne '''
        compteur=[0,0,0,0]
        for i in range(52):
            compteur[self.attributions[i]] +=1
        for i in range(4):
            if compteur[i] != 13 :
                raise NameError('Une des mains ne compporte pas 13 cartes')
        
    
        
        
        
    def affiche(self):
        print(' Donneur : '+self.donneur+'   Vulnérabilité : '+self.vul)
        print('                Nord')
        self.nord.affiche(15)
        print('Ouest                         Est')
        self.ouest.affiche(10,self.est)
        print('                Sud')
        self.sud.affiche(15)

        
class Filtre:
    ''' Filtres correspondant à des enchères classiques. Les filtres sont 
    volontairement plus vastes que les critères habituels des bridgeurs
    de façon à correspondre à des styles différents'''
    def __init__(self,name,
                 pointH_min = 0,
                 pointH_max = 40,
                 trefle_min = 0,
                 trefle_max = 13,
                 carreau_min = 0,
                 carreau_max = 13,
                 coeur_min = 0,
                 coeur_max= 13,
                 pique_min = 0,
                 pique_max = 13,
                 trefle_qualite = 0,
                 carreau_qualite = 0,
                 coeur_qualite = 0,
                 pique_qualite = 0,
                 points_totaux_min = 0,
                 points_totaux_max = 99):
        self.name = name
        self.pointH_min = pointH_min
        self.pointH_max = pointH_max
        self.trefle_min = trefle_min
        self.trefle_max = trefle_max
        self.carreau_min = carreau_min
        self.carreau_max = carreau_max
        self.coeur_min = coeur_min
        self.coeur_max = coeur_max
        self.pique_min = pique_min
        self.pique_max = pique_max
        self.trefle_qualite = trefle_qualite
        self.carreau_qualite = carreau_qualite
        self.coeur_qualite = coeur_qualite
        self.pique_qualite = pique_qualite
        self.points_totaux_min = points_totaux_min
        self.points_totaux_max = points_totaux_max 
        
    def filtre(self,main):    
        ''' Renvoie True si la main considérée correspond au filtre désirée, 
        c'est à dire est proche d'une enchère cklassique'''
        valeurs = main.vertues()
        if self.pointH_min > valeurs[0] :
            #print(1)
            return False
        if self.pointH_max < valeurs[0] :
            #print(2)
            return False
        if self.trefle_min > valeurs[1] :
            #print(3)
            return False
        if self.trefle_max < valeurs[1] :
            #print(4)
            return False
        if self.carreau_min > valeurs[2] :
            #print(5)
            return False
        if self.carreau_max < valeurs[2] :
            #print(6)
            return False
        if self.coeur_min > valeurs[3] :
            #print(7)
            return False
        if self.coeur_max < valeurs[3] :
            #print(8)
            return False
        if self.pique_min > valeurs[4] :
            #print(9)
            return False
        if self.pique_max < valeurs[4] :
            #print(10)
            return False
        if self.trefle_qualite > valeurs[5] :
            #print(11)
            return False
        if self.carreau_qualite > valeurs[6] :
            #print(12)
            return False
        if self.coeur_qualite > valeurs[7] :
            #print(13)
            return False
        if self.pique_qualite > valeurs[8] :
            #print(14)
            return False
        if self.points_totaux_min > valeurs[0]+valeurs[9] :
            #print(15)
            return False
        if self.points_totaux_max < valeurs[0]+valeurs[9] :
            #print(16)
            return False
        return True
        
            
 
filtres = {}   #liste des filtres

''' Juste quelques filtres simples pour le moment à étendre'''


def _init_filtres():    
    filtres["1P"] = Filtre("1P", pointH_min = 10, pique_min =5,
           points_totaux_min = 13)
    filtres["1C"] = Filtre("1C", pointH_min = 10, coeur_min =5,
           points_totaux_min = 13)
    filtres["1TK"] = Filtre("1TK", pointH_min = 10, coeur_max =4,
           pique_max = 4, points_totaux_min = 13)
    filtres["1SA"] = Filtre("1SA", pointH_min = 14, pointH_max=18,
           trefle_min=2,carreau_min =2, coeur_min =2, pique_min=2)
    filtres["1SAfaible"] = Filtre("1SAfaible", pointH_min = 11, pointH_max=14,
           trefle_min=2,carreau_min =2, coeur_min =2, pique_min=2)  

    
    
_init_filtres()
    
    
                        
#test={0,5,12,15,16,21,51,18,32,45,17,50}
#main = decode_main(test) 
#main.affiche()   
#vérification de la réversibilkité de code et decode  
donne=Donne()        
donne.affiche()    
donne._code()
donne._decode()
donne.affiche()  

#vérification de l'identifiant
donne=Donne()
donne.affiche()
print(donne.identifiant())
mon_id=donne.identifiant()
donne1=Donne(identifiant=mon_id)
donne1.affiche()
donne1=Donne(identifiant='0xb29f79e11ca17a9c0dd60f3069a')
donne1.affiche()

print(donne1.sud.vertues())
print(donne1.est.vertues())
print(donne1.ouest.vertues())
print(donne1.nord.vertues())

piques = Longueur((1,4,6,10,11))
print(len(piques))

 # Test des filtres
donne = Donne()
compteur = 0
print("1P en sud")
while not (filtres["1P"].filtre(donne.sud) or compteur > 200):
    donne = Donne()
    compteur += 1
    print("essai", compteur)
donne.affiche()   
 
donne = Donne()
compteur = 0
print("1C en sud")
while not (filtres["1C"].filtre(donne.sud) or compteur > 200):
    donne = Donne()
    compteur += 1
    print("essai", compteur)
donne.affiche()    

donne = Donne()
compteur = 0
print("1mineur en sud")
while not (filtres["1TK"].filtre(donne.sud) or compteur > 200):
    donne = Donne()
    compteur += 1
    print("essai", compteur)
donne.affiche()                
                
                
donne = Donne()
compteur = 0
print("1SA fort en sud")
while not (filtres["1SA"].filtre(donne.sud) or compteur > 200):
    donne = Donne()
    compteur += 1
    print("essai", compteur)
donne.affiche()       
    

    
    
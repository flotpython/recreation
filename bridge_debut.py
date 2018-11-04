#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 14:34:46 2018

@author: hubert
"""
from random import randint,shuffle

code_pique,code_coeur,code_carreau,code_trefle=3,2,1,0
couleur={code_trefle:'\u2663',code_carreau:'\x1b[31;1m\u2666\x1b[39;1m',code_coeur:'\x1b[31;1m\u2665\x1b[39;1m',code_pique:'\u2660'}
couleurs=[code_pique,code_coeur,code_carreau,code_trefle]
valeur=['2','3','4','5','6','7','8','9','10','V','D','R','A']

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
                print(couleur[c],self.total[c],' '*(26-len(str(self.total[c]))),couleur[c],autre_main.total[c])
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
           
            
def decode_main(liste):
    ''' Creation d'une main à partir d'une liste de cartes codées de 0 à 51'''
    listes =[[] for i in range(4)]
    for carte in liste:
        listes[carte//13].append(carte%13)
    return Main(*listes)    
    
    
            
    
class Donne:
    donneurs = ['Nord','Sud','Est','Ouest']
    vulnerabilite = ['Personne','NS','EO','Tous']
    def __init__(self, sud = None, nord = None, est = None, ouest = None, donneur = 'Nord', vul = 'Personne', identifiant= None):
        ''' On peut créer une donne de trois façons. En entrant les quatre mains et optionnellement la vulnérabilité et le donneur, ou bien
        en la générant aléatoirement, ou encore en entrant un identifiant unique associée à chaque donne possible. Les syntaxes possibles sont
        Donne(nord=((2,5,6,10),(2,11),(0,12),(3,5,6,8,10)), sud = cartes de sud, est = ..., ouest = ... ) facultativement
        Donne(nord=..., sud = ..., est = ..., ouest = ..., donneur = , vul = ) si on veut indiquer le donneur et la vulnérabilité
        Donne() pour distribuer une main aléatoirement ou
        Donne(identifiant = un nombre) pour retrouver une donne dont on a conservé l'identifuiant'''
        if sud :
            self.sud     = Main(*sud)
            self.nord    = Main(*nord)
            self.est     = Main(*est)
            self.ouest   = Main(*ouest)
            self.donneur = donneur
            self.vul     = vul
            self._code()
        elif identifiant:
            self._reconstitution(identifiant)    # Reconstitue la main à partir d'un identifiant unique
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
        ''' Calcul de l'identifiant unique de la donne. Le résultat est transformé en chaîne de caractères 
        #pour transmission par des fichiers textes'''
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
              
                
                
      
    

    
    
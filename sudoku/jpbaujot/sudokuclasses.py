# -*- coding: utf-8 -*-
"""
Created on Fri Jan  5 14:45:20 2018
000000000
@author: JP
"""

string ='\
000001200\n\
009800000\n\
800006070\n\
705030060\n\
000209000\n\
020010803\n\
030700004\n\
000004500\n\
006500000'

string ='\
000000010\n\
400000000\n\
020000000\n\
000050407\n\
008000300\n\
001090000\n\
300400200\n\
050100000\n\
000806000'

class Case :
    
    def __init__(self,i,j,val = 0):
        self.l = i
        self.c = j
        self.val = val
        self.val_poss = []
        if not val :
            self.val_poss = [n for n in range(1,10)]  
        
    def case_choices(self,grida):        
        val_used = [grida[self.l][p].val_case() for p in range(9)] +[grida[p][self.c].val_case() for p in range(9)]

        for p in range(int((self.l)/3)*3,int((self.l)/3)*3+3):
            for q in range(int((self.c)/3)*3,int((self.c)/3)*3+3):
                val_used.append(grida[p][q].val_case())  
        
        return [n for n in range(1,10) if n not in set(val_used) ]

    def val_case(self):
        return self.val
    
    def set_value(self,val):
        self.val = val
    

class Grid :
    def __init__(self,grid) :        
        self.grida = []
        self.listchoix = []
        self.count=0
        c= 0        
        for row in grid :
            self.grida.append([])
            for d,val in enumerate(row):                               
                self.grida[c].append(Case(c,d,int(val)))
            c+=1
                
    def __str__ (self):
        msg = ''
        for i in range(9) :
            for j in range(9) :
                msg += str(self.grida[i][j].val_case())+" "
            msg +="\n"
        return msg
        
        
    def count_zeros (self):
    
    #compte les 0 de la grille 
        for i in range(9) :
            for j in range(9) :
                if not self.grida[i][j].val_case() :
                    return True
        return False
    
    def retro (self):    
    #en cas de blocage , revient sur les choix précédents 
    #passe au choix suivant dans la derniere case ou remonte à la case 
    #qui a fait l'objet du choix précédent 
    
        while True : 
            i,j,choix = self.listchoix.pop() # on recupére le dernier choix fait
            case = self.grida[i][j]
            case.set_value (0)
            liste_choix = case.case_choices(self.grida) 
            idx = liste_choix.index(choix)
            if idx<len(liste_choix)-1 : # on va prendre l'élement suivant s'il existe
                self.listchoix.append((i,j,liste_choix[idx+1]))# on rememorise le choix
                self.count+=1
                case.set_value(liste_choix[idx+1])
                break

                
    def search_min(self) :
        i,j,min  = 0,0,9 
        listmin =[]
        
        countones = True
        
        while countones :                
            countones = False
            cond = True
            for m in range(9): 
                if not cond:
                    break
                for n in range(9):
                    case = self.grida[m][n]
                    if not case.val_case() :
                        testlist = case.case_choices(self.grida)
                        if len(testlist)==1 :
                            countones = True
                            self.count+=1
                            self.listchoix.append((m,n,testlist[0]))            
                            self.grida[m][n].set_value(testlist[0]) 
                        
                        if len(testlist)<min :
                            min = len(testlist)
                            i,j=m,n
                            listmin = testlist
                            if not min :
                                cond = False
                                countones = False
                                self.retro()
                                break
        
        if min >1 :
            self.count+=1
            self.listchoix.append((i,j,listmin[0]))            
            self.grida[i][j].set_value(listmin[0])

        

                          
import time        
temps = time.time()
grid = string.split('\n')
sudoku= Grid(grid)


print (sudoku)


while sudoku.count_zeros():
    sudoku.search_min()


print (sudoku) 
print(sudoku.count)
temps = time.time() - temps  
print(temps)





# sudoku en recursivité :
#pour chaque case 
    # on regarde si la grille est compléte
    # si la case est une case origine , on transmet le message amont ou aval

    #si on trouve une valeur compatible,  
       # on met à jour la case
       # on interroge la case suivante
       # si retour False d'une case aval : 
           # on relance la fonction pour la case qui se trouve incrementée       
   #si  blocage on renvoie False à la case précédente 
# on peut faire des sudoku de 4,9,16,25.....  
import numpy as np  
import math
import time
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

S = 9
SQ = int(math.sqrt(S))
def case_min(): 
    '''
    return a case with minimum possibilities
    '''
    i,j = 0,0
    liste_cases = sorted ([(len(case_choices(m,n)),m,n) \
                   for m in range(S) for n in range(S) if not grida[m][n]])
    if liste_cases : _,i,j= liste_cases[0]
    return i,j

def square_zone(l,c):
    '''
    return a list of the cells in the same square of cells (SQ *SQ)
    '''
    return [(p,q) for p in range(int(l/SQ)*SQ,int(l/SQ)*SQ+SQ)\
                 for q in range(int(c/SQ)*SQ,int(c/SQ)*SQ+SQ)]

def case_choices(l,c): 
    '''
    return a list of possible values for a case
    '''       
    val_used = [grida[l][p] for p in range(S)] +[grida[p][c]for p in range(S)]    
    val_used += [grida[p][q] for p,q in square_zone(l,c) ]    
    return [n for n in range(1,S+1) if (n not in set(val_used) and  n>grida[l][c])]

def filled_grid() :
    '''
    return a boolean , which is used to end the game
    '''    
    return not np.count_nonzero(grida == 0)

def sudoku (i1,j1):
    '''
    function called by the main, using recursivity to calculate the grid
    at each turn,
    test if the grid is filled and stop the game
    if not, test if the case can be filled with a value ,
        fill the case with minimum value available candidate
        the case with minimum number of choices is selected and tested in recursivity
            if bad result with the filled value (another case with no choice)
               it tries to propose another value , 
    else put 0 in the cell and return false value to the previous call of functions
    '''    
    if filled_grid():return                  
    liste_choices = case_choices(i1,j1)
    if  liste_choices  :
        grida[i1,j1] = liste_choices[0]
        return sudoku (i1,j1) if not sudoku(*case_min()) else True
    grida[i1,j1] = 0
    return False
#--------------main code---------------------            
#initial grid 
grida = np.zeros((S,S))
grid = string.split('\n')
c = 0        
for row in grid :
    for d,val in enumerate(row):
        grida[c][d] = int(val)
    c+=1
print(grida) 
print() 
# recursivity 
m,n = 0,0 
temps = time.time()
while grida[m,n] : # search for a empty case to begin
    n += 1
    n %= S
    m += int(n/S)
sudoku (m,n)
temps = time.time() - temps  
print(temps)
print(grida)   
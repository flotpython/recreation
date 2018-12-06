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
import numpy as np

count = 0
f = open('sudoku17.txt', 'r')
file = f.read()

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
    if filled_grid():
        return                  
    liste_choices = case_choices(i1,j1)
   
    if liste_choices  :
        grida[i1,j1] = liste_choices[0]
        if not sudoku(*case_min()) : return sudoku (i1,j1)

    
    grida[i1,j1] = 0
    return False
#--------------main code---------------------            
#initial grid 
temps = time.time()
for row in file.split('\n')[0:10]:
    grida = np.zeros((S,S))
    grid = [row[i*9:i*9+9]for i in range(9)]
    
    c = 0        
    for line in grid :
        d  =0
        for val in line:
            grida[c][d] = int(val)
            d+=1
        c+=1
           
    m,n = 0,0 
    while grida[m][n] : # search for a empty case to begin
        n += 1
        n %= S
        m += int(n/S)
    sudoku (m,n)
    print(grida)
    count+=1            
    
    temps = time.time() - temps
    print(count,temps)
    temps = time.time()

  
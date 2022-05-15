# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 18:20:57 2021

@author: 1000249643
"""

# code of an actual reduction that produces a CNF formula then calls a minisat solver 
# and then reads the solution for a sudoku puzzle from a satisfying assignment to this formula 


import itertools
import os

puzzle=[
        "5***1***4",
        "***2*6***",
        "**8*9*6**",
        "*4*****1*",
        "7*1*8*4*6",
        "*5*****3*",
        "**6*4*1**",
        "***5*2***",
        "2***6***8"  
        ]

#puzzle=[
#        "83**4**16",
#        "***9*1*4*",
#        "*********",
#        "15*******",
#        "**8**9***",
#        "2**1*5*8*",
#        "*41***3**",
#        "7*34***2*",
#        "*2******5"  
#        ]

#puzzle=[
#        "",
#        "",
#        "",
#        "",
#        "",
#        "",
#        "",
#        "",
#        ""  
#        ]

#puzzle=[
#        "*5**62*4*",
#        "***95****",
#        "**9*4*1**",
#        "8******7*",
#        "537***962",
#        "*9******8",
#        "**1*1*7**",
#        "****96***",
#        "*6*78***5*"  
#        ]

#puzzle=[
#        "*5***83**",
#        "3****5***",
#        "64**92**5",
#        "**6****5*",
#        "***2*4***",
#        "*2****1**",
#        "7**58**92",
#        "***4****6",
#        "**51***8*"  
#        ]

clauses = []
digits = range(1,10)

# generates unique 3 digit number for every variable, we need this to give a formula to minisat solver
def varnum(i,j,k):
#    assert (i in digits and j in digits and k in digits)  #maybe this is to convert string into integers
    return 100*i + 10*j + k

# This is a method which given a list of literals writes down clauses that express the fact
# that exactly one of these literals is equal to true

def exactly_one_of(literals):
    clauses.append([l for l in literals]) #  we first add a clause that contains all the literals in the list literals
    
#    for pair in itertools.product(literals, repeat=2): # then for all pair of literals we add a clause containing two negated literals from this list
    for pair in itertools.combinations(literals, 2):
        clauses.append([-l for l in pair]) # as discussed in the lecture this expresses that only one of them is TRUE
        
# Now we start writing down clauses expressing that each cell contains exactly one digit
# Namely, for all pairs of digits we write down a clause stating that the cell[i,j] contains exactly one digit
# cell [i,j] contains exactly one digit
for (i,j) in itertools.product(digits, repeat=2):
    exactly_one_of([varnum(i,j,k) for k in digits])
    
## k appears exactly one in row i  
for (i,k) in itertools.product(digits, repeat=2):   
    exactly_one_of([varnum(i,j,k) for j in digits])
    
# k appears exactly one in row j       
for (j,k) in itertools.product(digits, repeat=2):   
    exactly_one_of([varnum(i,j,k) for i in digits])    

      
## k appears exactly once in a 3x3 block     
for (i,j) in itertools.product([1,4,7], repeat=2):
    for k in digits:
        exactly_one_of([varnum(i + deltai, j+deltaj, k) for (deltai, deltaj) in itertools.product(range(3), repeat=2)])
             
##        
### Adding varaibles for input puzzle    
for (i,j) in itertools.product(digits, repeat=2):
    if puzzle[i-1][j-1] != "*": # if corresponding cell is specified then we just add unit clause containing exactly one corresponding variable
        k = int(puzzle[i-1][j-1])
        assert(k in digits)
        clauses.append([varnum(i,j,k)])
        
# here we write down all the clauses.         
with open('tmp.cnf', 'w') as f: # Namely, we open a file, tmp.cnf  
    f.write("p cnf {} {}\n".format(999, len(clauses))) # in the first line we write p cnf followed by the number of variables in our case it is roughly 1000 and then the number of clauses
    for c in clauses: 
        c.append(0) # Then for each clause which is currently in our list of clauses we first append 0 to satisfy the format which is accepted by mini-SAT
        f.write(" ".join(map(str, c))+"\n") # and then we just write down this clause

# then we call minisat SAT solver give it the formula tmp.cnf anf also indicate the file tmp.sat where it will write down the staisfying assignment

filename = "tmp.sat"  # This is because the minisat command requires that tmp.sat file where the output has to be written must be present in the directory
if not os.path.exists(filename):
    open(filename, 'w').close()
      
os.system("minisat tmp.cnf tmp.sat")

# then we open the satisying assignment file and read the first line 

with open ("tmp.sat", "r") as satfile:
    for line in satfile:
        if line.split()[0] == "UNSAT": # if it is "UNSAT", we just report that the formula is unsatisfiable
            print("There is no solution")
        elif line.split()[0] == "SAT": # If the first line is "SAT", we know that the formula is satisfiable and we know that the second line will be followed by a satisfying assignment
            pass
        else:
            assignment = [int(x) for x in line.split()] # At this line we read the corresponding satisfying assignment 
            # Notice that besides satisfying assignment all other assignments will be negative
#            print(assignment)
            
            # and then we parse it
            
            for i in digits:
                for j in digits:
                    for k in digits:
                        if varnum(i,j,k) in assignment: # We just see if the corresponding variable in this assignment then we print it
                            print(k, end="")
                            break
            
                print(" ")

'''
To understand this problem only understand the fact that 

Clauses expressing the fact that exactly one of the literals ℓ1, ℓ2, ℓ3 is equal to 1 is :

    (ℓ1 ∨ ℓ2 ∨ ℓ3) (-ℓ1 ∨ -ℓ2) (-ℓ1 ∨ -ℓ3) (-ℓ2 ∨ -ℓ3)
    
First clause shows that only one is true and rest shows that none of the two can be true simultaneously.

'''
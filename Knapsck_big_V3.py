# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 11:09:09 2018

@author: a.teffal
"""

import numpy as np
import pandas as pd

#read the file
f = open('knapsack_big.txt', 'r')
fichier = f.readlines()
f.close()

# max capcity
W=int(fichier[0].split(sep=' ')[0])

# number of items
N=int(fichier[0].split(sep=' ')[1])

#storing values and weights
#values
values=[]
#weights
weights=[]

n=len(fichier)

for i in range(1,n):
    values.append(int(fichier[i].split(sep=' ')[0]))
    weights.append(int(fichier[i].split(sep=' ')[1]))
    




# array of subproblems's solutions of first i items
A_i=np.zeros((N),dtype=int) 

# array of subproblems's solutions of first (i-1) items
A_i_1=np.zeros((N),dtype=int) 


#selected_items
selected=set()

wi=np.argsort(weights)

jj=0

for i in range(N):
    jj=0
    for j in range(0,N):
        jj=jj+weights[wi[j]]
        if jj> W:
            A_i[j]=A_i[j-1]
        if jj<=W:
            if j-1 >=0:
                max_temp=max(A_i_1[j],A_i_1[j-1]+values[wi[i]])
                A_i[j]=max_temp
        #        if max_temp==A[i-1,j-weights[i]]+values[i]:
        #            selected.add((values[i],weights[i]))
            else:
                A_i[j]=A_i_1[j]

    A_i_1=A_i.copy()
print("optimal solution is ",A_i[N-1])



































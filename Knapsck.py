# -*- coding: utf-8 -*-
"""
Created on Thu Apr  5 11:09:09 2018

@author: a.teffal
"""

import numpy as np
import pandas as pd

#read the file
f = open('knapsack1.txt', 'r')
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
    




# array of subproblems
A=np.zeros((N,W),dtype=int)

#selected_items
selected=set()

for i in range(1,N):
    for j in range(W):
        if j-weights[i] >=0:
            max_temp=max(A[i-1,j],A[i-1,j-weights[i]]+values[i])
            A[i,j]=max_temp
            if max_temp==A[i-1,j-weights[i]]+values[i]:
                selected.add((values[i],weights[i]))
        else:
            A[i,j]=A[i-1,j]


print("optimal solution is ",A[N-1,W-1])




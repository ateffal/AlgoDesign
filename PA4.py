# -*- coding: utf-8 -*-
"""
Created on Mon May 21 12:53:58 2018

@author: a.teffal
"""

import numpy as np
import pandas as pd
import copy

from graph import *


#read the file
f = open('test2.txt', 'r')
fichier = f.readlines()
f.close()

#Read number of verticies and edges
#verticies

n=int(fichier[0].split(" ")[0])

#edges
m=int(fichier[0].split(" ")[1])


graph1 = Digraph()

#Adding nodes to graph1
for i in range(1,n+1):
    graph1.addNode(Node(str(i),i-1))

for i in range(1,m+1):
    temp = fichier[i].split(" ")
    source = graph1.getNode(temp[0]) #Node(temp[0])
    destination = graph1.getNode(temp[1]) #Node(temp[1])
    edge = Edge(source, destination, int(temp[2]))
    graph1.addEdge(edge)
    
print(graph1)
    

src = graph1.getNode('1')
dest = graph1.getNode('6')

def DFS_2(graphe, source, destination):
    
#    graphe = copy.deepcopy(graph)
    #a dict storing for each marked node the min distance to that node
    #from the source and the previous node in this shortest path 
    best_node_to = {}
    
    def update_dist(node, dist, prev):
        if ((node in best_node_to)  and (dist < best_node_to[node][0])) or not (node in best_node_to)  :
            best_node_to[node] = [dist, prev]
 
    stack1 = []
    stack1.append(source)
    update_dist(source, 0, None)
    current = None
    
    
    while len(stack1) > 0:
        #pop the node from the stack
        
        current = stack1.pop()
        current.mark()
            
        #get the childrens of the this node
        childrens = graphe.childrenOf(graphe.getNode(current.getName()))
        #put this childrens in the stack
        for w in childrens:
            if not w.isMarked():
                stack1.append(w)
                
            update_dist(w,best_node_to[current][0]+1, current)
                
    print(destination)
    path= destination.getName()
    temp = best_node_to[destination][1]
    while temp.getName() != source.getName():
        path = temp.getName() + '-->' + path
        temp = best_node_to[temp][1]
    path = temp.getName() + '-->' + path
    print(path)


#    for d in best_node_to:
#        print(d, ' : ', best_node_to[d][0], '---', best_node_to[d][1])
#        print(best_node_to[destination])
        
        
def Bellman_Ford(graphe, source):
    
    def calc_min(n_edges, dest):
        temp_min = float("inf")
        node_dest = graphe.getNode(str(dest+1))
        parents = graphe.parentsOf(node_dest)
        for p in parents:
            temp_min = min(A[n_edges -1 , int(p[0].getName())-1] +  p[1], temp_min )
            
        return temp_min
        
        
        
    A = np.zeros((n+1,n), dtype=float)
    
    #Initialisation
    for i in range(n):
            A[0,i] = float("inf")      
    A[0,source] = 0
    
    
            
    for j in range(1, n+1):
        for i in range(n):
            A[j, i] = min(A[j-1, i], calc_min(j, i))
            
    return A      


def Bellman_Ford2(graphe, source):
    
    def calc_min(dest):
        temp_min = float("inf")
        node_dest = graphe.getNode(str(dest+1))
        parents = graphe.parentsOf(node_dest)
        for p in parents:
            temp_min = min(A_j_1[int(p[0].getName())-1] +  p[1], temp_min )
            
        return temp_min
        
        
    A_j_1 = np.zeros((n,), dtype=float)
    A = np.zeros((n,), dtype=float)
    
    #Initialisation
    for i in range(n):
            A_j_1[i] = float("inf")    
            A[i] = float("inf")   
            
    A_j_1[source] = 0
    A[source] = 0
    
    for j in range(1, n+1):
        A_j_1 = A.copy()
        for i in range(n):
            A[i] = min(A_j_1[i], calc_min(i))
        
            
    return np.array([A_j_1,A])      


def Bellman_Ford3(graphe, source):
    
    def calc_min(dest):
        temp_min = float("inf")
        best_vertex = ''
        node_dest = graphe.getNode(str(dest+1))
        parents = graphe.parentsOf(node_dest)
        for p in parents:
            if A_j_1[int(p[0].getName())-1] +  p[1] <= temp_min:
                temp_min = A_j_1[int(p[0].getName())-1] +  p[1]
                best_vertex = p[0].getName()
                
            
        return temp_min, best_vertex
        
        
    A_j_1 = np.zeros((n,), dtype=float)
    A = np.zeros((n,), dtype=float)
    B = np.empty((n,n),dtype='object')
    
    #Initialisation
    for i in range(n):
            A_j_1[i] = float("inf")    
            A[i] = float("inf")   
            
    A_j_1[source] = 0
    A[source] = 0
    
    for j in range(1, n):
        A_j_1 = A.copy()
        for i in range(n):
            temp = calc_min(i)
            if temp[0] < A_j_1[i]:
                A[i] = temp[0]
                #B[i] = temp[1] + ' -> ' + B[i-1] + ' -> ' + str(i+1)
                B[j, i] = temp[1]
            else:
                A[i] = A_j_1[i]
                B[j,i] = B[j-1,i]
                
        
            
    return np.array([A_j_1,A]), B     


def shortestPath(B_, src, dest):
    """B_ is the B array returned by the Bellman Ford algorithm"""
    temp = B_[dest]
    path = str(dest+1)
    while temp!=str(src+1):
        path = temp + '->' + path
        temp = B_[int(temp)-1]
    path = str(src + 1) + '->' + path
    
    print(path)
    


def Floyd_Warshall(file):
    #read the file
    f = open(file, 'r')
    fichier = f.readlines()
    f.close()
    
    #Read number of verticies and edges
    #verticies
    n=int(fichier[0].split(" ")[0])
    #edges
    m=int(fichier[0].split(" ")[1])
    
    graph1 = Digraph()
    
    A = np.zeros((n, n, n+1),dtype=float)
    
    for i in range(n):
        for j in range(n):
            if i==j:
                A[i,j,0] = 0
            else:
                A[i,j,0] = float("inf") 
    
    #Adding nodes to graph1
    for i in range(1,n+1):
        graph1.addNode(Node(str(i),i))

    for i in range(1,m+1):
        temp = fichier[i].split(" ")
        source = graph1.getNode(temp[0]) #Node(temp[0])
        destination = graph1.getNode(temp[1]) #Node(temp[1])
        edge = Edge(source, destination, int(temp[2]))
        graph1.addEdge(edge)
        A[int(source.getName())-1, int(destination.getName())-1,0] = int(temp[2])
        
    
    for k in range(1,n+1):
        for i in range(n):
            for j in range(n):
                A[i,j,k] = min(A[i,j,k-1], A[i,k-1,k-1] + A[k-1,j,k-1] ) #Le nom des vertex est égal leur indice +1
    
    return A[:,:,n]


    
def Floyd_Warshall2(file):
    #read the file
    f = open(file, 'r')
    fichier = f.readlines()
    f.close()
    
    #Read number of verticies and edges
    #verticies
    n=int(fichier[0].split(" ")[0])
    #edges
    m=int(fichier[0].split(" ")[1])
    
    graph1 = Digraph()
    
    A_k = np.zeros((n, n),dtype=float)
    
    A_k_1 = np.zeros((n, n),dtype=float)
    
    for i in range(n):
        for j in range(n):
            if i==j:
                A_k[i,j] = 0
            else:
                A_k[i,j] = float("inf") 
    
    #Adding nodes to graph1
    for i in range(1,n+1):
        graph1.addNode(Node(str(i),i))

    for i in range(1,m+1):
        temp = fichier[i].split(" ")
        source = graph1.getNode(temp[0]) #Node(temp[0])
        destination = graph1.getNode(temp[1]) #Node(temp[1])
        edge = Edge(source, destination, int(temp[2]))
        graph1.addEdge(edge)
        A_k[int(source.getName())-1, int(destination.getName())-1] = int(temp[2])
        
    
    for k in range(1,n+1):
        A_k_1 = A_k.copy()
        for i in range(n):
            for j in range(n):
                A_k[i,j] = min(A_k_1[i,j], A_k_1[i,k-1] + A_k_1[k-1,j] ) #Le nom des vertex est égal leur indice +1
        
    
    return A_k


















        
    
        
        
        
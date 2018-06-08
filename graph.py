# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 15:04:56 2016

@author: guttag
"""

import heapq

from Heap import *

class Node(object):
    def __init__(self, name,indice):
        """Assumes name is a string"""
        self.name = name
        self.marked = False
        self.indice = indice
    def getName(self):
        return self.name
    
    def getIndice(self):
        return self.indice
    
    def isMarked(self):
        return self.marked
    
    def mark(self):
        self.marked = True
        
    def unmark(self):
        self.marked = False
    
    def __str__(self):
        return self.name

class Edge(object):
    def __init__(self, src, dest, weight):
        """Assumes src and dest are nodes"""
        self.src = src
        self.dest = dest
        self.weight = weight
        
    def getSource(self):
        return self.src
    
    def getDestination(self):
        return self.dest
    
    def getWeight(self):
        return self.weight
    
    def __str__(self):
        return self.src.getName() + '->' + self.dest.getName()
               
class Digraph(object):
    """edges is a dict mapping each node to a list of
    its children"""
    def __init__(self):
        self.edges = {}
        self.parents = {}
        self.nodes = []
        
    def addNode(self, node):
        if node in self.nodes:
            raise ValueError('Duplicate node ' + node.getName())
        else:
            self.edges[node] = []
            self.parents[node] = []
            self.nodes.append(node)
            
    def addEdge(self, edge):
        src = edge.getSource()
        dest = edge.getDestination()
        weight = edge.getWeight()
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph ' + src.getName() + '  ' + dest.getName())
        self.edges[src].append((dest, weight))
        self.parents[dest].append((src, weight))
        
    def childrenOf(self, node):
        return [w[0] for w in self.edges[node]]
    
    def weightEdgeOf(self, node):
        return self.edges[node]
    
    def parentsOf(self, node):
#        return [w[0] for w in self.parents[node]]
        return self.parents[node]
    
    def hasNode(self, node):
        return node in self.nodes
    
    def getNode(self, name):
        for n in self.nodes:
            if n.getName() == name:
                return n
        raise NameError(name)
        
    def getNodesNumber(self):
        return len(self.nodes)
    
    def getEdgesNumber(self):
        return len(self.edges)
        
    def __str__(self):
        result = ''
        for src in self.nodes:
            for dest in self.edges[src]:
                result = result + src.getName() + '->'\
                         + dest[0].getName() + '\n'
        return result[:-1] #omit final newline

class Graph(Digraph):
    def addEdge(self, edge):
        Digraph.addEdge(self, edge)
        rev = Edge(edge.getDestination(), edge.getSource(), edge.getWeight())
        Digraph.addEdge(self, rev)
    

def printPath(path):
    """Assumes path is a list of nodes"""
    result = ''
    for i in range(len(path)):
        result = result + str(path[i])
        if i != len(path) - 1:
            result = result + '->'
    return result 

def DFS(graph, start, end, path, shortest, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes;
          path and shortest are lists of nodes
       Returns a shortest path from start to end in graph"""
    path = path + [start]
    if toPrint:
        print('Current DFS path:', printPath(path))
    if start == end:
        return path
    for node in graph.childrenOf(start):
        if node not in path: #avoid cycles
            if shortest == None or len(path) < len(shortest):
                newPath = DFS(graph, node, end, path, shortest,
                              toPrint)
                if newPath != None:
                    shortest = newPath
        elif toPrint:
            print('Already visited', node)
    return shortest
    



def BFS(graph, start, end, toPrint = False):
    """Assumes graph is a Digraph; start and end are nodes
       Returns a shortest path from start to end in graph"""
    initPath = [start]
    pathQueue = [initPath]
    while len(pathQueue) != 0:
        #Get and remove oldest element in pathQueue
        tmpPath = pathQueue.pop(0)
        if toPrint:
            print('Current BFS path:', printPath(tmpPath))
        lastNode = tmpPath[-1]
        if lastNode == end:
            return tmpPath
        for nextNode in graph.childrenOf(lastNode):
            if nextNode not in tmpPath:
                newPath = tmpPath + [nextNode]
                pathQueue.append(newPath)
    return None
    
    

def Dijkstra_old(graph, source):
    import heapq
    # Number of verticies and edges
    n = graph.getNodesNumber()
    m = graph.getEdgesNumber()
    
    # Initialize distances and previous verticies
    dist = np.zeros((n,), dtype=float)
    prev = np.empty((n,),dtype='object')
    
    for i in range(n):
        dist[i] = 1000000   #float("inf")
        prev[i] = None
        
    dist[source.getIndice()] = 0
    
    #creating the heap 
    heap = []
    print(n)
    for i in range(n):
        heap.append((dist[i],str(i+1)))
    heapq.heapify(heap)
    
        
    
    
    while len(heap) != 0:
        # Get the node with min distance (deletting it from the heap)
        u = graph.getNode(heapq.heappop(heap)[1])
        # Get the nodes adjacent to u ((u,v) edges) and the weight of edges
        children = graph.weightEdgeOf(u) #return a list of (v, weight)
        for (v,w) in children:
            if dist[v.getIndice()] > dist[u.getIndice()] + w:
                dist[v.getIndice()] = dist[u.getIndice()] + w
                prev[v.getIndice()] = u.getIndice()
                # decrease the key of v
                for h in heap:
                    if h[1]==v.getName():
                        h = (dist[v.getIndice()],h[1])
        
        #retore the heap property
        heapq.heapify(heap)
    
    return dist, prev
        
    
    

def Dijkstra(graph, source):
    
    # Number of verticies and edges
    n = graph.getNodesNumber()
    m = graph.getEdgesNumber()
    
    # Initialize distances and previous verticies
    dist = np.zeros((n,), dtype=float)
    prev = np.empty((n,),dtype='object')
    
    for i in range(n):
        dist[i] = 1000000   #float("inf")
        prev[i] = None
        
    dist[source.getIndice()] = 0
    
    #creating the heap 
    heap = Heap()
    for i in range(n):
        heap.addItem([dist[i],str(i+1)])
    
    # main loop of the algorithm
    while len(heap) != 0:
        # Get the node with min distance (deletting it from the heap)
        u = graph.getNode(heap.pop()[1])
        # Get the nodes adjacent to u ((u,v) edges) and the weight of edges
        children = graph.weightEdgeOf(u) #return a list of (v, weight)
        for (v,w) in children:
            if dist[v.getIndice()] > dist[u.getIndice()] + w:
                dist[v.getIndice()] = dist[u.getIndice()] + w
                prev[v.getIndice()] = u.getIndice()
                # decrease the key of v
                
                for h in heap:
                    if h[1]==v.getName():
                        h = (dist[v.getIndice()],h[1])
        
        #retore the heap property
        heapq.heapify(heap)
    
    return dist, prev
    
    
    
    

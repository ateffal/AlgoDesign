# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 12:36:30 2018

@author: a.teffal
"""

class Heap(object):
    """Assumes items are lists like [value, key] """
    def __init__(self):
        self.size = 0
        self.table = []
        self.keyIndice = {}
    
    
    def restoreHeapDown(self, i):
        # i = self.size -1 
        j = int((i-1)/2)
        while j >=0:
            if self.table[j][0] > self.table[i][0]:
                self.table[j] , self.table[i] = self.table[i], self.table[j]
                #update key inndice
                self.keyIndice[self.table[j][1]] = j
                self.keyIndice[self.table[i][1]] = i
                i = j
                j = int((j-1)/2)
            else:
                break
        
    
    def restoreHeapTop(self, i):
        #i = 0 
        left = 2*i+1
        right = 2*i+2
        
        while left < self.size or right < self.size:
            temp = -1
            if left < self.size:
                if self.table[left][0] < self.table[i][0]:
                    self.table[left] , self.table[i] = self.table[i], self.table[left]
                    #update key inndice
                    self.keyIndice[self.table[left][1]] = left
                    self.keyIndice[self.table[i][1]] = i
                    temp = left
                
            if right < self.size:
                if self.table[right][0] < self.table[i][0]:
                    self.table[right] , self.table[i] = self.table[i], self.table[right]
                    #update key inndice
                    self.keyIndice[self.table[right][1]] = right
                    self.keyIndice[self.table[i][1]] = i
                    temp = right
                
            if temp == -1:
                break
            
            i = temp
            left = 2*i+1
            right = 2*i+2
            
        
    def addItem(self, item):
        #add the item to the end of the heap
        self.table.append(item)
        self.keyIndice[item[1]] = self.size
        
        # update size
        self.size = self.size + 1
        
        # restore the heap property
        self.restoreHeapDown(self.size -1)
            
    def pop(self):
        """Extracts the min"""
        # remove the first element if the heap is not empty
        if self.size !=0:
            # replace the root with the last element in the heap, but save it before to return it
            temp = self.table[0]
            self.table[0] = self.table[self.size-1]
            self.keyIndice[self.table[self.size-1][1]] = 0
            
            # remove the last element in the heap
            self.table.pop()
            self.keyIndice.pop(temp[1])
            
            # update size
            self.size = self.size - 1
            
            # restore the heap property
            self.restoreHeapTop(0)
            
            return temp
        
        else:
            return None
    
    def updateValue(self, key, newValue):
        
        #if the item doesnt exist return false
        if not key in self.keyIndice:
            return False
        else:
            i = self.keyIndice[key]
        
        oldValue = self.table[i][0]
        self.table[i][0] = newValue
        if newValue < oldValue:
            self.restoreHeapDown(i)
            return True
        if newValue > oldValue:
            self.restoreHeapTop(i)
            return True
        
    
        
    def getTable(self):
            return self.table
        
    def getSize(self):
        return self.size
    
    def getIndices(self):
        return self.keyIndice
        
        
        

#test
h1 = Heap()
h1.addItem([42,'amine'])
h1.addItem([32,'bilal'])
print(h1.getTable())
print(h1.getIndices())


h1.addItem([10,'ali'])
print(h1.getTable())
print(h1.getIndices())

h1.addItem([1,'omar'])
print(h1.getTable())
print(h1.getIndices())

h1.addItem([67,'father'])
print(h1.getTable())
print(h1.getIndices())

h1.pop()
print(h1.getTable())
print(h1.getIndices())

































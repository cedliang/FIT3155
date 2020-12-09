# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 14:42:12 2020

@author: cedri
"""
import sys

class disjointSet:
    
    #initialises array with n being the number of elements
    def __init__(self, n):
        self.keyArray = [-1]*n
        
        
    #arguments are indexes within the keyArray
    #returns the index of the root element
    def find(self, a):
        if self.keyArray[a] < 0:
            return a
        else:
            self.keyArray[a] = self.find(self.keyArray[a])
            return self.keyArray[a]
        
        
        
        
    #arguments are the indexes within keyArray
            
    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a  == root_b:
            raise Exception("The elements at index "+str(a)+" and "+str(b)+" are already in the same set")
        
        #note that these correspond to height+1
        height_a = -1*self.keyArray[root_a]
        height_b = -1*self.keyArray[root_b]
        
        if height_a > height_b: 
            self.keyArray[root_b] = root_a
            
        elif height_b > height_a: 
            self.keyArray[root_a] = root_b
        
        #height_b == height_a
        else:
            self.keyArray[root_a] = root_b
            self.keyArray[root_b] = -1* (height_b+1)
        
        

     
def getWeight(edge):
    return edge[2]




#call from command line
if __name__ == "__main__":
    graph = []
    numVerticesRead = sys.argv[1]
    numVertices = int(numVerticesRead)
    f = open(sys.argv[2],"r")






    
    for line in f:
        stringArray = line.split()
        temp = []
        for elem in stringArray:
            temp.append(int(elem))
        if not temp == []:
            graph.append(temp)
    

    
    #O(n log n) call on sort as per https://wiki.python.org/moin/TimeComplexity
    graph.sort(key=getWeight)
    
    #the disjoint set to keep track of vertices
    vertexSet = disjointSet(numVertices)
    
    #stores the edges to keep
    outputArray = []
    totalWeight = 0
    
    #loop through all the edges
    for edge in graph:
        if not (vertexSet.find(edge[0]) == vertexSet.find(edge[1])):
            outputArray.append(edge)
            vertexSet.union(edge[0], edge[1])
            totalWeight += edge[2]
            
            #early termination when a spanning tree has been found
            if len(outputArray) == numVertices - 1:
                break
    

    f = open("output_kruskals.txt", "w")
    f.write(str(totalWeight)+"\n")
    for elem in outputArray:
        f.write(str(elem[0])+" "+str(elem[1])+" "+str(elem[2])+"\n")
    f.close()







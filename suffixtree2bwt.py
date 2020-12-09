# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 19:37:55 2020

@author: cedri
"""
import sys

class NaiveSuffixTree:
    
    class Node:
        def __init__(self, children = None, parentPointer = None):
            if children is None:
                self.numChild = 0
                self.childrenPointers = []
                
            else:
                self.childrenPointers = children
                self.numChild = len(children)
            
            #counters and pointers to facilitate traversal
            self.parentPointer = parentPointer
            self.edgesProcessed = 0
                
    class Edge:
        def __init__(self, payload, parentNode, childNode = None):
            self.payload = payload
            self.parentNode = parentNode
            self.childNode = childNode
        
    
    def __init__(self, string):
        self.string = string+"%"
        
        self.suffixes = []
        for i in range(len(self.string)):
            self.suffixes.append(self.string[i:len(self.string)])
        
        
        self.rootNode = self.Node()
        
        #Generate Tree
        for suffix in self.suffixes:
            remainingSuffix = suffix
            location = self.rootNode
            mismatch = False
            
            while not mismatch:
                #location is Node
                if isinstance(location, self.Node):
                    firstLetter = remainingSuffix[0]
                    
                    foundEdge = None
                    
                
                    
                    
                    for edge in location.childrenPointers:
                        if edge.payload[0] == firstLetter:
                            foundEdge = edge
                    
                    if foundEdge is None:
                        mismatch = True
                        
                    else:
                        location = foundEdge
                
                #location is edge
                else:
                    
                    edgePayload = location.payload
                    
                    
                    #note the observation here: if remainingSuffix here is shorter than
                    #the edge, it must necessarily be the case that there is a mismatch that arises due to 
                    #the $ at the end of remainingSuffix
                    
                    
                    #edge is longer than remaining, guaranteed mismatch somewhere on this edge
                    if len(edgePayload) >= len(remainingSuffix):
                        i = 0
                        while not mismatch and i < len(remainingSuffix):
                            if edgePayload[i] != remainingSuffix[i]:
                                mismatch = True
                                mismatchIndex = i
                                remainingSuffix = remainingSuffix[i:]
                            i += 1
                        
                    
                    #edge is shorter than remaining, possibility of mismatch, or possibility of successful traversal
                    else:
                        i = 0
                        while not mismatch and i < len(edgePayload):
                            if edgePayload[i] != remainingSuffix[i]:
                                mismatch = True
                                mismatchIndex = i
                                remainingSuffix = remainingSuffix[i:]
                            i += 1
                        
                        #successful traversal
                        if not mismatch:
                            location = location.childNode
                            remainingSuffix = remainingSuffix[i:]              
                        
                        
            #deal with mismatch
            #is Node, meaning that an edge must be created
            if isinstance(location, self.Node):
                
                if len(remainingSuffix) > 0:
                    #create edge
                    location.childrenPointers.append(self.Edge(remainingSuffix, location, self.Node(None,None)))
                    location.childrenPointers[-1].childNode.parentPointer = location.childrenPointers[-1]
                    
                    
            #mismatch at an edge, must branch
            else:
                childOfOriginalEdge = location.childNode
                
                sharedPayload = location.payload[:mismatchIndex]
                unsharedPayload = location.payload[mismatchIndex:]
                
                location.payload = sharedPayload
                location.childNode = self.Node(None, location)
                
                #add new branch
                location.childNode.childrenPointers.append(self.Edge(remainingSuffix,location.childNode,self.Node() ))
                location.childNode.childrenPointers[-1].childNode.parentPointer = location.childNode.childrenPointers[-1]
                
                #add old branch
                location.childNode.childrenPointers.append(self.Edge(unsharedPayload, location.childNode, childOfOriginalEdge))
                childOfOriginalEdge.parentPointer = location.childNode.childrenPointers[-1]
                
    def getSuffixArray(self):
        #perform depth first traversal based on lexographical order
        
        suffixesInOrder = []
        location = self.rootNode
        finishedTraversal = False
        partialString = ""
        downTraversal = True
        
        while not finishedTraversal:
            #location is Node
            if isinstance(location, self.Node):
                
                
                
                #exhausted all child edges, done here, traverse up
                if location.edgesProcessed == len(location.childrenPointers):
                 
                    
                    #is leaf
                    if len(location.childrenPointers) == 0:
                        suffixesInOrder.append(partialString)
                        
                    #all edges of rootNode have been exhausted, end traversal
                    if location == self.rootNode:
                        finishedTraversal = True
                        
                    #reset edgesProcessed
                    location.edgesProccessed = 0
                    location = location.parentPointer
                    downTraversal = False

                
                #have not exhausted all children, continue traversing down
                else:
                    
                    #THIS LINE ENSURES OUTPUT IS IN SORTED ALPHABETICAL ORDER
                    if location.edgesProcessed == 0:
                        location.childrenPointers.sort(key = lambda edge: edge.payload)
                        
                    location = location.childrenPointers[location.edgesProcessed]
                    location.parentNode.edgesProcessed += 1
                    downTraversal = True
                    
                    
                    
            #location is edge
            else:
                #downtraversal
                if downTraversal:
                    
                    partialString += location.payload
                    location = location.childNode
                
                #uptraversal
                else:
                    partialString = partialString[:len(partialString)-len(location.payload)]
                    location = location.parentNode
                    
        outputArray = []
        for suffix in suffixesInOrder:
            outputArray.append(len(self.string)-len(suffix))
        return outputArray        
    
def BWT(string):
    
    suffTree = NaiveSuffixTree(string)
    stringSuffixArray = suffTree.getSuffixArray()
    
    string = "$"+string
    
    BWTString = ""
    
    for index in stringSuffixArray:
        BWTString += string[index]
    
    return BWTString



if __name__ == "__main__":
    f = open(sys.argv[1],"r")
    string = f.read().strip()
    
    f = open("output_bwt.txt", "w")
    f.write(BWT(string))
    f.close()
    


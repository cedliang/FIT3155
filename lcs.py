# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 17:59:29 2020

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
        
    #note I have modified NaiveSuffixTree to take two string arguments
    #with two unique delineators
    def __init__(self, string1, string2):
        self.string1 = string1
        self.string2 = string2
        self.string = string1+"$"+string2+"#"
        
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
                
    def getSuffixArray(self,indices = False):
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
            
        if not indices:
            return suffixesInOrder
        return outputArray 
    
    
def LCS(string1, string2):
    suffixTree = NaiveSuffixTree(string1, string2)
    suffixArray = suffixTree.getSuffixArray()[2:]
    
    
    #print(suffixArray)
    
    
    whichStringArray = []
    for suffix in suffixArray:
        if len(suffix)<= len(string2)+1:
            whichStringArray.append(2)
        else:
            whichStringArray.append(1)
          
    #print(whichStringArray)
            
    validAlignmentArray = [None]
    for i in range(1, len(whichStringArray)):
        if whichStringArray[i-1] != whichStringArray[i]:
            validAlignmentArray.append(True)
        else:
            validAlignmentArray.append(False)
      
    #print(validAlignmentArray)
    
    LCSArray = [None]
    for i in range(1,len(suffixArray)):
        
        str1 = suffixArray[i-1]
        str2 = suffixArray[i]
        
        minNumChar = min([len(str1), len(str2)])
        
        mismatch = False
        
        j = 0
        
        while not mismatch and j < minNumChar:
            
            if str1[j] != str2[j]:
                mismatch = True
            j += 1
                
        LCSArray.append(j-1)
    #print(LCSArray)
    
    
    currentMax = 0
    maxIndices = []
    
    for i in range(1,len(suffixArray)):
        if validAlignmentArray[i] == True:
            if LCSArray[i] > currentMax:
                currentMax = LCSArray[i]
                maxIndices = [i]
            elif LCSArray[i] == currentMax:
                maxIndices.append(i)
                
    #print(currentMax)
    #print(maxIndices)
    
    matchIndices = []
    
    for match in maxIndices:
        
        #we note that sometimes, the occurence that is detected is not necessarily the leftmost occurence of 
        #matching patterns within the text, but rather the occurence of the match substring that is lexigraphically
        #the smallest
        #
        #we note however that other occurrences of the match can 'span' from the match location whilst holding 
        #a few conditions:
        #first, whichStringArray for each member of the span (ie, they must be from the same string)
        #second, the number of matching characters must be the same or greater
        #third, the location of these spans must be strictly adjacent.
        #
        #suppose I had a LCSArray as follows:
        #[4, 4, 3, 2, 3, 4]
        #and a whichStringArray as follows:
        #[1, 1, 1, 2, 2, 2]
        #
        #The algorithm has detected a match of length 2 at index 3, but this only 
        #corresponds to the lexigraphically latest
        #occurence of the pattern in the first string, matching with the lexigraphically earliest occurence of the 
        #pattern in the second string, NOT necessarily the leftmost occurrences. Indeed, we notice that
        #due to the 'span' conditions holding true, the suffixes at index 0 and 1 also come from the same string 
        #as the suffix at index 2, and share the same (relevant) prefixes due to the larger than 2 value in the LCSArray, 
        #so these are all also valid matches with the suffixes from string 2 at indices 3, 4 and 5
        #
        #To detect the leftmost occurrence, we must check for these 'spans', and find the leftmost occurrences
        #of the pattern for each span
        
        
                
        if whichStringArray[match - 1] == 1:
            firstStringIndex = match - 1
            
            #leftSpan
            firstStringSpan = [firstStringIndex]
            
            leftSpanIndex = firstStringIndex - 1
            while whichStringArray[leftSpanIndex] == 1 and LCSArray[leftSpanIndex + 1] >= currentMax and leftSpanIndex >= 0:
                firstStringSpan.append(leftSpanIndex)
                leftSpanIndex -= 1
            
            
            secondStringIndex = match
            
            #rightSpan
            secondStringSpan = [secondStringIndex]
            
            rightSpanIndex = secondStringIndex + 1
            while whichStringArray[rightSpanIndex] == 2 and LCSArray[rightSpanIndex] >= currentMax and rightSpanIndex < len(suffixArray):
                secondStringSpan.append(rightSpanIndex)
                rightSpanIndex += 1
            
            
            
        else:

            secondStringIndex = match - 1
        
        
            #leftSpan
            secondStringSpan = [secondStringIndex]
            leftSpanIndex = secondStringIndex - 1
            while whichStringArray[leftSpanIndex] == 2 and LCSArray[leftSpanIndex + 1] >= currentMax and leftSpanIndex >= 0:
                secondStringSpan.append(leftSpanIndex)
                leftSpanIndex -= 1
            
            
            firstStringIndex = match
            
            #rightSpan
            firstStringSpan = [firstStringIndex]
            rightSpanIndex = firstStringIndex + 1
            while whichStringArray[rightSpanIndex] == 1 and LCSArray[rightSpanIndex] >= currentMax and rightSpanIndex < len(suffixArray):
                firstStringSpan.append(rightSpanIndex)
                rightSpanIndex += 1



        
        
        
        matchIndexTuple = []
        #leftmost occurrence means longest suffix in suffixArray
        for element in firstStringSpan:
            if len(suffixArray[element]) > len(suffixArray[firstStringIndex]):
                firstStringIndex = element
        
        for element in secondStringSpan:
            if len(suffixArray[element]) > len(suffixArray[secondStringIndex]):
                secondStringIndex = element
 
        
        #firstString
        matchIndexTuple.append((len(string1)+len(string2)+2)-len(suffixArray[firstStringIndex]))
        
        #secondString
        matchIndexTuple.append((len(string2)+1) - len(suffixArray[secondStringIndex]))
        
        matchIndices.append(matchIndexTuple)
    
    return [currentMax, matchIndices]
    


if __name__ == "__main__":
    f = open(sys.argv[1],"r")
    string1 = f.read().strip()
    f.close()
    
    f = open(sys.argv[2],"r")
    string2 = f.read().strip()
    
    result = LCS(string1, string2)
    
    f = open("output_lcs.txt", "w")
    f.write(str(result[0]) + "\n")
    
    for match in result[1]:
        f.write(str(match[0])+" "+str(match[1])+"\n")
    
    f.close()

        











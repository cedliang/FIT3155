#Cedric Liang 29674662 Assignment 1 Question 2

"""
Created on Fri Sep  4 22:09:44 2020

@author: cedri
"""


# -*- coding: utf-8 -*-
"""
Spyder Editor


"""
import sys

class BoyerMoore:
    def __init__(self, txt, pat):

        #PREPROCESS

        ZSuffixArray = self.computeZSuffixValues(pat)
        GSValues = self.computeGoodSuffixValues(pat, ZSuffixArray)
        MPValues = self.computeMatchedPrefixValues(pat)
        
        #All jump tables have been computed
        
        i = 0
        
        matches = []
        comparisonsCount = 0
        
        #i is the index of the left side of the alignment
        # i+len(pat) - 1 is the index of the right side of the alignment
        
        
        
        #zone to not match due to galil optimisation 
        #first elem is upper index
        #second element is lower index
        #both INCLUSIVE
        #both are on the PATTERN index
        
        skipZone = None
        
        while i < len(txt) - len(pat) + 1:
        
            #textindex
            j= i+len(pat)-1
            #patindex
            k = len(pat)-1 
            
            # j = i+k
            
            

            

            
            while k > -1 and txt[j] == pat[k]  :
                comparisonsCount += 1
                
                
                if skipZone is None:
                    k -= 1
                    j -= 1
                
                elif k == skipZone[0]+1 :
                    k=skipZone[1]-1
                    j=i+k
                    
                else:
                    k -= 1
                    j -= 1
                
                
                        
            #mismatch
            if k > -1:
                comparisonsCount += 1
                
     
                ####The Bad Character Rule is unnecessary in binary matching!
                
                
                #####Good Suffix Shift 1a
                if GSValues[k+1] > 0:
                    

                    
                    
                    GSShift = len(pat)-GSValues[k+1]-1
                    skipZone = [GSValues[k+1], GSValues[k+1] - len(pat) + k+1 ]

                
                
                ###Good Suffix Shift 1b
                elif GSValues[k+1] == 0:
                    


                    GSShift = len(pat)-MPValues[k+1]-1
                    skipZone = [MPValues[k+1], 0]
                    
                
            #exact match
            else:
                matches.append(i)

                GSShift = len(pat)-MPValues[1]-1
                skipZone = [MPValues[1], 0]
                

            
            



            i+= GSShift
                

                
        self.output(matches, comparisonsCount)
                
                
        
    def output(self, matchIndices,comparisonsCount):
        outputArray = []
        for elem in matchIndices:
            outputArray.append(elem + 1)
            
            
        f = open("output_binary_boyermoore.txt", "w")
        for elem in outputArray:
            f.write(str(elem)+"\n")

        f.close()
        
        print("Comparison Count: "+ str(comparisonsCount))

        
        


    #standard ZArray Computation Function
    def computeZArray(self,txt):


            zArray = [0]*len(txt)

            li = 0
            ri = 0



            for i in range(1 ,len(txt)):



                #case 1: explicit comparisons
                if i > ri:



                    #here nMatch is a counter

                    nMatch = 0

                    while ((nMatch + i < len(txt) and txt[nMatch] == txt[nMatch + i])):
                        nMatch += 1



                    if nMatch > 0:
                        zArray[i] = nMatch
                        ri = i + nMatch - 1
                        li = i

                #Case 2
                else:
                    #case 2a

                    if zArray[i-li] < ri - i + 1:



                        zArray[i] = zArray [i - li]

                    #case 2b

                    else:


                        #note here matchTracker is an index, not a counter
                        matchTracker = ri + 1
                        while matchTracker < len(txt) and txt[matchTracker] == txt[matchTracker - i]:
                            matchTracker += 1
                        zArray[i] = matchTracker - i
                        li = i
                        ri = matchTracker - 1






            return zArray







    def computeZSuffixValues(self, pat):
        

        return self.computeZArray(pat[::-1])[::-1]
        
    

    def computeGoodSuffixValues(self, pat, ZSuffixArray):
        m = len(pat)
        goodSuffix = [0]*(m+1)

        for p in range(0,m-1):

            j = m-ZSuffixArray[p]
            goodSuffix[j] = p
        return goodSuffix
    
    def computeMatchedPrefixValues(self, pat):
        

        localZArray = self.computeZArray(pat)

        
        matchedPrefixArray = [0]*len(pat)
        
        for i in range(len(pat)-1, -1, -1):
            
            #base case comparison
            if i == len(pat)-1:
                if pat[0]==pat[i]:
                    matchedPrefixArray[i]==1
            
                    
            else:
                if localZArray[i]+i == len(pat):
                    matchedPrefixArray[i]=localZArray[i]
                else:
                    matchedPrefixArray[i]=matchedPrefixArray[i+1]
            
        
        #add special cases since ZArray computation doesn't cover these
        matchedPrefixArray[0]=len(pat)
        matchedPrefixArray.append(0)    
    
        return matchedPrefixArray
            


if __name__ == "__main__":
    textfile = open(sys.argv[1],"r")
    text = textfile.read()
    patternfile = open(sys.argv[2],"r")
    pattern = patternfile.read()

    runScript = BoyerMoore(text, pattern)

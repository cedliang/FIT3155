#Cedric Liang 29674662 Assignment 1 Question 1: Parameter Matching

import sys


#####################################################################################################
        #################BIJECTIVE FIXED ALPHABET DATA STRUCTURE##########################
#This keeps track of bijective mappings by using two arrays. Since we have a fixed alphabet,
#the index of the array will correspond to the mapping. -1 means no mapping, 0 corresponds to a, 1 corresponds to b
# and so on. For example, if we have a mapping of b in the pattern to c in the text, we will have the arrays
    #patterntext array: [-1, 2, -1, -1, ...]
    #plaintext array:   [-1, -1, 1, -1, ...]


class bijectiveMap:

    #O(1) time
    def __init__(self):
        self.patternTextMap = [-1]*26
        self.plainTextMap = [-1]*26

    #helps our indexing, with lower case a set to 0 index
    #O(1) time
    def getIndex(self, char):
        return ord(char)-97


    #O(1) time
    def addMap(self, txtchar, patchar):
        self.plainTextMap[self.getIndex(txtchar)] = self.getIndex(patchar)
        self.patternTextMap[self.getIndex(patchar)] = self.getIndex(txtchar)


    #O(1) time
    #checks whether there currently exists a valid bijective mapping (no write as to reduce side effects, SRP)
    #returns 1 if a valid mapping exists
    #returns 0 if the mapping does not exist, but there is no clash of mappings, and it's a totally new mapping to
        #be written
    #returns -1 if there is a mapping failure. ie, one of the elements (or both) are already written to another letter
    def checkMapExists(self, txtchar, patchar):
        if self.plainTextMap[self.getIndex(txtchar)] == self.getIndex(patchar) and self.patternTextMap[self.getIndex(patchar)] == self.getIndex(txtchar):
            return 1

        elif self.plainTextMap[self.getIndex(txtchar)] == -1 and self.patternTextMap[self.getIndex(patchar)] == -1:
            return 0
        else:
            return -1


    #O(1) time
    #processes mappings WITH side effects.
    #Returns false if checkMapExists returns -1 (ie, a failure)
    #Returns true if checkMapExists returns 0 or 1. Additionally writes the mapping if it returns 0.
    #
    #NOTE: Also deals with upper case letters and $, but requires an exact match. Will not try to write upper case letters to 
        #the map.
    def checkMapAndAdd(self, txtchar, patchar):
        
        
        if txtchar == "$" or patchar == "$":
            return False
        
        if txtchar.isupper() or patchar.isupper():
            if txtchar == patchar:
                return True
            return False
            
        

        
        var = self.checkMapExists(txtchar, patchar)
        
        
        if  var == -1:
            return False

        if var == 0:
            self.addMap(txtchar, patchar)

        return True


    #print for debugging purposes
    def __str__(self):
        return("PatternMap: "+str(self.patternTextMap)+"\n"+"TextMap: "+str(self.plainTextMap))


###################################################################################
########### O(n^2) naive algorithm for p-matching #####################################
class naiveAlgorithm:

    def __init__(self, txt, pat):

        outputArray = []


        for i in range(0,len(txt)-len(pat)+1):
            if self.match(txt[i:i+len(pat)], pat):
                #need conversion from 0 indexing to 1 indexing
                outputArray.append(i+1)

        print(outputArray)


    #checks if parameters match
    def match(self, substr, pat):

        mappings = None

        for i in range(len(pat)):

            if mappings is None:
                mappings = bijectiveMap()

            mapCheck = mappings.checkMapAndAdd(substr[i], pat[i])

            if mapCheck == False:
                return False


        return True




#runScript = naiveAlgorithm("AaBcBaABCaBaAxBy","aBc")
#runScript = naiveAlgorithm("AAA","BBB")
#runScript = naiveAlgorithm("AAA","AAA")
#runScript = naiveAlgorithm("abcde","bcd")
#runScript = naiveAlgorithm("abCde","aCe")
#runScript = naiveAlgorithm("gatcaaaaaaaacgaaacaaagcaacgacgagcagaaaaatgagcaaacgatatctcaacaaaaagtcgagaccagaggaagacgtagaagaccgaatga","aat")
#print("\n")



####################################################################################################################
######################## Z Algorithm for P-Matching ##############################################################


class PMatchZAlgorithm:
    def __init__(self, txt, pat):

        zArray = self.computeZArray(txt, pat)
        matchIndices = []
        for i in range(len(pat)+1, len(zArray)):
            if zArray[i]==len(pat):
                matchIndices.append(i-len(pat)-1)

        self.output(matchIndices)

    def output(self, matchIndices):
        outputArray = []
        for elem in matchIndices:
            outputArray.append(elem + 1)
            
            
        f = open("output_parameter_matching.txt", "w")
        for elem in outputArray:
            f.write(str(elem)+"\n")
        f.close()



    def computeZArray(self, txt, pat):

        compositeString = pat + "$" + txt
        zArray = [0]*len(compositeString)

        li = 0
        ri = 0



        for i in range(1 ,len(compositeString)):


            #case 1: explicit comparisons
            if i > ri:

                
                #here nMatch is a counter

                nMatch = 0
                mappings = bijectiveMap()
                
                
                
                
                
                while nMatch + i < len(compositeString) and mappings.checkMapAndAdd(compositeString[nMatch + i], compositeString[nMatch]):
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
                    
                    mappings = bijectiveMap()
                    
                    #note here matchTracker is an index, not a counter
                    
                    matchTracker = ri + 1
                    
                    #now we must first write the mappings from i to ri, before performing p-matching
                    #from ri+1 onwards, since the bijective mappings can drift from the 'initial match'
                    
                    #this is really the only difference from the regular ZAlgorithm (apart from using the bijective
                    #map for the direct comparison cases)
                    
                    #we assume these sections are already p-matched so we don't need actual comparisons
                                       
                    
                    
                    for j in range(i, ri + 1):
                        
                        txtchar = compositeString[j]
                        patchar = compositeString[j - i] 
                        
                        if txtchar.islower() and patchar.islower():
                            mappings.addMap(txtchar, patchar)
                    
                    
                    
                    while matchTracker < len(compositeString) and mappings.checkMapAndAdd(compositeString[matchTracker], compositeString[matchTracker - i]):
                        matchTracker += 1
                    zArray[i] = matchTracker - i
                    li = i
                    ri = matchTracker - 1



        return zArray




#runScript = PMatchZAlgorithm("AaBcBaABCaBaAxBy","aBc")
#runScript = PMatchZAlgorithm("AAA","BBB")
#runScript = PMatchZAlgorithm("AAA","AAA")
#runScript = PMatchZAlgorithm("abcde","bcd")
#runScript = PMatchZAlgorithm("abCde","aCe")
#runScript = PMatchZAlgorithm("gatcaaaaaaaacgaaacaaagcaacgacgagcagaaaaatgagcaaacgatatctcaacaaaaagtcgagaccagaggaagacgtagaagaccgaatga","aat")



#call from command line
if __name__ == "__main__":
    textfile = open(sys.argv[1],"r")
    text = textfile.read()
    patternfile = open(sys.argv[2],"r")
    pattern = patternfile.read()

    runScript = PMatchZAlgorithm(text, pattern)

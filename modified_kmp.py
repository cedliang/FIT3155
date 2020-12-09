#Cedric Liang 29674662 Assignment 1 Question 3

"""
Created on Fri Sep  4 22:25:22 2020

@author: cedri
"""


###This is just a regular KMP, I have not had time to optimise it

class KMP:
    
    def __init__(self, txt, pat):
        SPiArray = self.computeSPi(pat)
        
        i = 0
        matches = []
        
        skipHowMany = 0
        
        while i < len(txt) - len(pat) + 1:
            
            #patternindex
            k=skipHowMany
            #textindex
            j=i+k
            
            while k < len(pat) and txt[j] == pat[k]:
                k += 1
                j += 1
            
            #exact match
            if k == len(pat):
                matches.append(i)
                i += len(pat) - SPiArray[len(pat)-1]
                skipHowMany = SPiArray[len(pat)-1]
            #failure
            
            #first character mismatch
            elif k == 0:
                i += 1
                skipHowMany = 0
            else:
                i += k - SPiArray[k-1]
                skipHowMany = SPiArray[k-1]
                
                
        self.output(matches)
                
        
    def output(self, matchIndices):
        outputArray = []
        for elem in matchIndices:
            outputArray.append(elem + 1)
            
            
        f = open("output_kmp.txt", "w")
        for elem in outputArray:
            f.write(str(elem)+"\n")
        f.close()

        
        
        
        
    def computeSPi(self, pat):
        ZArray = self.computeZArray(pat)
        
        SPiArray = [0]*len(pat)

        for j in range(len(pat)-1, 0, -1):

            i = j + ZArray[j]-1
            SPiArray[i]= ZArray[j]
        return SPiArray
    
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





test = KMP("abcdabcdabcd", "abc")


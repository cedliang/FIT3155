# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import sys

#could not get my fib heap to work, so I'm implementing dijkstra's with a binary heap
class binHeap:


    def __str__(self):
        return str(self.heapArray)
    
    #returns the index of a child's parent
    def parentIndex(self, i):
        return ((i+1)//2)-1
    
    def leftChildIndex(self, i):
        return ((i+1)*2)-1
    
    def rightChildIndex(self, i):
        return (i+1)*2
    
    def size(self):
        return len(self.heapArray)
    
    def upRotate(self, i):
        while i > 0:
            if self.heapArray[i][0] < self.heapArray[self.parentIndex(i)][0]:
                #swap
                temp = self.heapArray[self.parentIndex(i)]
                
                self.heapArray[self.parentIndex(i)] = self.heapArray[i]
                self.positionArray[self.heapArray[self.parentIndex(i)][1]] = self.parentIndex(i)
                
                self.heapArray[i] = temp
                self.positionArray[self.heapArray[i][1]] = i
                
                i = self.parentIndex(i)
                
                
                
                
                
            else:
                #break
                i = 0
    
    #returns the index of the smaller child, or the left child if there is only one child
    def minChildIndex(self, i):
        #if there is no right child
        if self.rightChildIndex(i) > len(self.heapArray) - 1:
            return self.leftChildIndex(i)
        else:
            if self.heapArray[self.leftChildIndex(i)][0] > self.heapArray[self.rightChildIndex(i)][0]:
                return self.rightChildIndex(i)
            else:
                return self.leftChildIndex(i)
            
    
    def downRotate(self, i):
        #has a child
        while self.leftChildIndex(i) <= len(self.heapArray) - 1:
            minimumChildIndex = self.minChildIndex(i)
            
            if self.heapArray[i][0] > self.heapArray[minimumChildIndex][0]:
                temp = self.heapArray[i]
                
                self.heapArray[i] = self.heapArray[minimumChildIndex]
                self.positionArray[self.heapArray[i][1]] = i
                
                self.heapArray[minimumChildIndex] = temp
                self.positionArray[self.heapArray[minimumChildIndex][1]] = minimumChildIndex
                
                i = minimumChildIndex
            else:
                break
    
    def extractMin(self):
        returnValue = self.heapArray[0]
        self.positionArray[returnValue[1]] = None
        
        self.heapArray[0] = self.heapArray[-1]
        self.positionArray[self.heapArray[0][1]] = 0
        
        del self.heapArray[-1]
    
        self.downRotate(0)
        return returnValue
        
      
        
    #for testing purposes. checks if the heap constraint is held true
    def checkHeapConstraint(self):
        for i in range(1,len(self.heapArray)):
            if self.heapArray[self.parentIndex(i)][0]>self.heapArray[i][0]:
                return False
        return True
               
    def __init__(self, numVertices, buildList):
        #nodes are [key, payload] tuples 
        self.positionArray = numVertices*[0]
        
        self.heapArray = buildList
        i = self.parentIndex(len(self.heapArray)-1)
        while i >= 0:
            self.downRotate(i)
            i -= 1
                
        
        for i in range(self.size()):
            self.positionArray[self.heapArray[i][1]] = i
            
                
    def changeKey(self, i, newKeyValue):
        currentKeyValue = self.heapArray[i][0] 
        self.heapArray[i][0] = newKeyValue
        if newKeyValue > currentKeyValue:
            self.downRotate(i)
        else:
            self.upRotate(i)
            
    def getIndex(self, payload):
        return self.positionArray[payload]
            
#Binary Heap Testing
# aBinHeap = binHeap([[7, 0], [10, 0], [4, 0], [3, 0], [5, 0]])
# print(aBinHeap)
# print(aBinHeap.checkHeapConstraint())

# aBinHeap.insert([1,0])
# print(aBinHeap)
# print(aBinHeap.checkHeapConstraint())


# print(aBinHeap.extractMin())
# print(aBinHeap)
# print(aBinHeap.checkHeapConstraint())

# aBinHeap.changeKey(3, 1)
# print(aBinHeap)
# print(aBinHeap.checkHeapConstraint())

# aBinHeap.changeKey(0, 1000)
# print(aBinHeap)
# print(aBinHeap.checkHeapConstraint())



#Dijkstra implemented with binary heap. O((|V|+|E|)log|V|) complexity
class Dijkstra:
    def __init__(self, graph, numVertices, origin, destination):
        self.origin = origin
        self.destination = destination
        
        #this is more of a note to myself
        #stores the directed edges. format is the index of self.edges corresponds to the source vertex
        #all edges leaving that vertex are stored as tuples within this array.
        #this edge tuple has index 0 corresponding to the destination vertex and index 1 corresponding to the weight
        #for example
        #self.edges[1] returns an array of all edges leaving vertex 1
        #self.edges[1][0] refers to a specific edge leaving vertex 1
        #self.edges[1][0][1] refers to the weight of this edge
        #
        self.edges = []
        for i in range(numVertices):
            self.edges.append([])
            
        for edge in graph:
            self.edges[edge[0]].append(edge[1:3])
            

        
        self.binHeapConstructArray = []
        for i in range(numVertices):
            if i == origin:
                self.binHeapConstructArray.append([0, i])
            else:
                self.binHeapConstructArray.append([100000000, i])
        
        self.distances = [100000000]*numVertices
        self.prev = []
        for i in range(numVertices):
            self.prev.append(None)
        
        self.binHeap = binHeap(numVertices, self.binHeapConstructArray)
             
        
        while self.binHeap.size() > 0:
            
            
            #currentVertex[0] for distance
            #currentVertex[1] for the vertex to which this distance belongs
            currentVertex = self.binHeap.extractMin()

            
            self.distances[currentVertex[1]] = currentVertex[0] 
            
            edges = self.edges[currentVertex[1]]
            
            #edge[0] for destination
            #edge[1] for weight
            for edge in edges:
                
                #if it's None then already processed and distance is minimal
                if self.binHeap.getIndex(edge[0]) is not None:
                    
                    currentDistanceToDest = self.binHeap.heapArray[self.binHeap.getIndex(edge[0])][0]
                    
                    newDistanceToDest = edge[1] + currentVertex[0]
    
                    
                    if newDistanceToDest < currentDistanceToDest:
    
    

                        
                        self.binHeap.changeKey(self.binHeap.getIndex(edge[0]),newDistanceToDest)
                        self.prev[edge[0]] = currentVertex[1]


        #GENERATE OUTPUT FROM PREV AND DISTANCES
        self.destinationDistance = self.distances[destination]
        destinationPathReverse = []
        
        localIndex = destination

        
        while localIndex is not None:
            destinationPathReverse.append(localIndex)
            localIndex = self.prev[localIndex]
        
        self.destinationPath = destinationPathReverse[::-1]
        


        
    def output(self):
        
        #OUTPUT:
        #returns tuple of distance and path.
        #access distance with array[0], array of nodes visited on this path with array[1]
        return [self.destinationDistance, self.destinationPath]
           
#Dijkstra tests
#[0, 2, 100000000, 3, 3, 4, 6]
#print(Dijkstra([[0,1,2],[0,4,3],[1,3,1],[3,5,4],[4,5,1],[5,6,2]], 7, 0, 6).output())

#[100000000, 2, 0, 1, 4, 5, 7]
#print(Dijkstra([[1,2,3],[2,1,2],[2,3,1],[3,4,3],[4,5,1],[5,6,2]], 7, 2, 6).output())

#[100000000, 0, 3, 1, 100000000, 5, 7]
#print(Dijkstra([[0,1,2],[1,2,3],[2,1,2],[1,3,1],[3,5,4],[4,6,1],[5,6,2]], 7, 1, 6).output())

#[100000000, 0, 3, 1, 4, 5, 5]
#print(Dijkstra([[0,1,2],[1,2,3],[2,1,2],[1,3,1],[3,5,4],[4,6,1],[5,6,2],[1,2,3],[2,1,2],[2,3,1],[3,4,3],[4,5,1],[5,6,2]], 7, 1, 6).output())

#represents an individual treasure hunter
class TreasureHunter:
    def __init__(self, startPoint, treasureLoc, localMap, numVertices, index):
        
        #index within globalMap's treasureHunterArray
        self.index = index
        
        self.treasureMap = localMap
        

        self.destination = treasureLoc
        self.numVertices = numVertices
    
        self.travelPath = Dijkstra(self.treasureMap, numVertices, startPoint, self.destination).output()[1]
        self.travelPath.pop(0)
        self.travelledDistance = 0
        
        #set location to None if currently in between nodes
        self.location = startPoint
        self.currentlyTravellingTowards = None
        self.travelTurnsLeft = 0
        self.currentPathWeight = 0
        
        self.visitedVertices = [self.location]
        
        self.partner = None
        
        
        self.treasureFound = False
        
    def playTurn(self):
        #currently on path case
        if self.location is None:
            
            #middle of path case
            if self.travelTurnsLeft > 1:
                self.travelTurnsLeft -= 1
            
            #arriving at node case
            elif self.travelTurnsLeft == 1:
                self.location = self.currentlyTravellingTowards
                self.currentlyTravellingTowards = None
                self.travelTurnsLeft = 0
                self.travelledDistance += self.currentPathWeight
                self.currentPathWeight = 0
                self.visitedVertices.append(self.location)
                
                if self.location == self.destination:
                    self.treasureFound = True
            

        
        
        #currently on vertex case
        else:
            if not self.treasureFound:
                
                             
                self.currentlyTravellingTowards = self.travelPath.pop(0)
                
                #find (inefficiently) the path to take amongst map vertices
                for edge in self.treasureMap:
                    if edge[0] == self.location:
                        if edge[1] == self.currentlyTravellingTowards:
                            self.currentPathWeight = edge[2]
     
                #destination node is more than 1 away   
                if self.currentPathWeight > 1:
                    self.travelTurnsLeft = self.currentPathWeight - 1
                    self.location = None
                    
                #destination is 1 away, which means next turn immediately arrives at node
                elif self.currentPathWeight == 1:
                    self.location = self.currentlyTravellingTowards
                    self.currentlyTravellingTowards = None
                    self.travelTurnsLeft = 0
                    self.travelledDistance += self.currentPathWeight
                    self.currentPathWeight = 0
                    self.visitedVertices.append(self.location)
                    if self.location == self.destination:
                        self.treasureFound = True
                    

    
    def pairUp(self, otherHunter):
        #pairup is called when hunter is at a node, so there is a precondition to this method that
        #location is not None
        
        #this way, self.location can be called to generate a new Dijkstra
        
        
        
        self.partner = otherHunter
        
        for edge in self.partner.treasureMap:
            self.treasureMap.append(edge)
            
        self.travelPath = Dijkstra(self.treasureMap, self.numVertices, self.location, self.destination).output()[1]
        self.travelPath.pop(0)
        
        
#Hunter Test (NO MERGE)        
#hunter1 = TreasureHunter(0,6,[[0,1,2],[0,4,3],[1,3,1],[3,5,4],[4,5,1],[5,6,2]],7,1)
#for i in range(10):
#    print("Path remaining: "+str(hunter1.travelPath))
#    print("Current Location: "+str(hunter1.location))
#    print("Currently travelling towards: "+str(hunter1.currentlyTravellingTowards))
#    print("Visited vertices: "+str(hunter1.visitedVertices))
#    print("Travelled distance: "+str(hunter1.travelledDistance))
#    print("Treasure found: "+str(hunter1.treasureFound))
#    print("\n")
#    hunter1.playTurn()
        

#hunter test with merge
#hunter2 = TreasureHunter(2, 6, [[1,2,3],[2,1,2],[2,3,1],[3,4,3],[4,5,1],[5,6,2]], 7, 2)
#hunter3 = TreasureHunter(1, 6, [[0,1,2],[1,2,3],[2,1,2],[1,3,1],[3,5,4],[4,6,1],[5,6,2]],7,3)        
#for i in range(10):    
#    hunter2.playTurn()
#    hunter3.playTurn()
##   test with and witout the pair up process
#    if hunter2.location == hunter3.location:
#        hunter2.pairUp(hunter3)
#        hunter3.pairUp(hunter2)
#print("Travelled distance: "+str(hunter2.travelledDistance))
#print("Visited vertices: "+str(hunter2.visitedVertices))


#represents the global gamestate.
class GlobalMap:
    def __init__(self, treasureLoc, numVertices, treasureHunterArray):
        self.treasureLoc = treasureLoc
        self.numVertices = numVertices
        self.treasureHunterArray = treasureHunterArray
        
        
        #global map represents the vertices by index
        self.globalMap = self.computeLocations()
        
    
    

    def computeLocations(self):
        returnArray = []
        for i in range(self.numVertices):
            returnArray.append([])
        for hunter in self.treasureHunterArray:
            if hunter.location is not None:
                returnArray[hunter.location].append(hunter)
        return returnArray
    
    
    #progresses 'gametime' by one turn
    def playTurn(self):
        for hunter in self.treasureHunterArray:
            hunter.playTurn()
        self.globalMap = self.computeLocations()
        

        
    #write gamelogic here
    def startGame(self):

        gameContinue = True
        while gameContinue:
            self.playTurn()
            
            #check game end?
            if len(self.globalMap[self.treasureLoc]) > 0:
                winners = []
                for winningHunter in self.globalMap[self.treasureLoc]:
                    winners.append(winningHunter)
                    gameContinue = False
            
            else:
                #process collisions
                for location in self.globalMap:
                    unpairedHunter = None
                    
                    for hunter in location:
                        #if unpaired
                        if hunter.partner is None:
                            #if no existing unpairedHunter
                            if unpairedHunter is None:
                                unpairedHunter = hunter
                            #existing unpaired hunter, ie, pair them up
                            else:
                                unpairedHunter.pairUp(hunter)
                                hunter.pairUp(unpairedHunter)
        
        return self.output(winners)
    
    def output(self, winners):
        returnArray = [winners[0].travelledDistance]
        for winner in winners:
            returnArray.append(winner.visitedVertices)
        return returnArray
            

#hunter0 = TreasureHunter(0,6,[[0,1,2],[0,4,3],[1,3,1],[3,5,4],[4,5,1],[5,6,2]],7,0)
#hunter1 = TreasureHunter(2, 6, [[1,2,3],[2,1,2],[2,3,1],[3,4,3],[4,5,1],[5,6,2]], 7, 1)
#hunter2 = TreasureHunter(1, 6, [[0,1,2],[1,2,3],[2,1,2],[1,3,1],[3,5,4],[4,6,1],[5,6,2]],7,2)    

#hunterArray = [hunter0, hunter1, hunter2]

#testGame = GlobalMap(6, 7, hunterArray)
#print(testGame.startGame())

if __name__ == "__main__":
    hunterArray = []
    
    numVertices = int(sys.argv[1])
    destination = int(sys.argv[2])
    
    for i in range(3, len(sys.argv)):
        
        hunterMap = []
        
        
        f = open(sys.argv[i],"r")
        
        firstLine = True
        
        
        for line in f:
            if firstLine:
                origin = int(line.strip())
                firstLine = False
            else:
                stringArray = line.split()
                temp = []
                for elem in stringArray:
                    temp.append(int(elem))
                if not temp == []:
                    hunterMap.append(temp)
        hunterArray.append(TreasureHunter(origin,destination,hunterMap,numVertices,i))
        
    runGame = GlobalMap(destination, numVertices, hunterArray)
    
    results = runGame.startGame()
    
        
    f = open("output_adventure.txt", "w")
    f.write(str(results[0])+"\n")
    for i in range(1,len(results)):
        
        for j in range(len(results[i])):
        
            f.write(str(results[i][j])+" ")
        f.write("\n")
    f.close()
                           
                         
        
        
    
    

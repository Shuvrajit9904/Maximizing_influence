# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 11:54:34 2017

@author: Shuvrajit
"""

from collections import defaultdict
#import sys
import random
#import matplotlib as plt

random.seed(57)

class Graph:
    
    #Constructor
    def __init__(self):
        self.graph = defaultdict(list)
        
    def addEdge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
        
    def addEdgeDir(self, u, v):
        self.graph[u].append(v)    
        
    def neighbours(self,u):
        return self.graph[u]
        #print self.graph
    def length(self):
        return len(self.graph)
    
    def adjacencylist(self):
        return self.graph


#Reading Data
#Working On Facebook Data
facebookData = open('facebook_combined.txt')
f = facebookData.read()
facebookData.close()
edges = f.strip().split('\n')

#Constructing Adjacency List for the graph
g = Graph()
for edge in edges:
    #print edge
    vertices = edge.strip().split()
    u = int(vertices[0])
    v = int(vertices[-1])
    g.addEdge(u,v)


#Independent Cascade Model
def cascade(vert, rand, activeState):
    active = []
    count = 0
    ct = 0        
    if len(g.neighbours(vert)) != 0:
        for vertices in g.neighbours(vert):                    
            rand1 = random.random()
            if rand1 > rand:            
                ct += 1
                active.append(vertices)
                #print(vertices)
                activeState[vertices] = True
                #print active
    if len(active) == 0:
        return 1
    else:
        for vertices in active:
            rand2 = random.random()
            if activeState[vertices] == False:
                count += cascade(vertices, rand2, activeState)
    return ct

#Independent Cascade Model(Handles influence of multiple vertices)
def cascadeGroup(vertList, rand, activeState):
    active = []
    count = 0
    ct = 0
    for vert in vertList:
        if len(g.neighbours(vert)) != 0:
            for vertices in g.neighbours(vert):        
                rand1 = random.random()
                if rand1 > rand:            
                    ct += 1
                    active.append(vertices)
                    #print(vertices)
                    activeState[vertices] = True
                    
            #print active
    if len(active) == 0:
        return 1
    else:
        for vertices in active:
            rand2 = random.random()
            if activeState[vertices] == False:
                count += cascade([vertices], rand2, activeState)
    return activeState


active = [False for i in range(g.length())]
print("Calculating Spread of Influence on ego-Facebook Data")
print("The budget for this example is 5(The report Captures spread for varying budget)")

#k is an integer, representing the budget
#k = int(input("What's your Budget(k) for Facebook Data?:"))
k = 5
#Finding out the most influencial nodes
mostInf = []
for ep in range(k):
    mx = 0
    for vert in g.adjacencylist():        
        if vert not in mostInf:
            neighbour = g.neighbours(vert)
            rand = random.random()
            activeCount = cascade(vert, rand, active)
            if activeCount > mx:
                mx = activeCount
                influence = vert
    mostInf.append(influence)
print("The set of 5 most influencial nodes are:")    
print(*mostInf, sep = ' ')


#Set the most influencial nodes as Active
activeInit = [False for i in range(g.length())]
for val in mostInf:
    activeInit[val] = True

#Calculate the influence of most influencial nodes
influenced = cascadeGroup(mostInf,rand,activeInit)
spread = 0
for state in influenced:
    if state == True:
        spread += 1
print("The spread (Counted active nodes) for these selected nodes is:",spread)
#Calculate the influence by randomly selected nodes
randVert = []        
activeInit = [False for i in range(g.length())]
for i in range(k):
    randVert.append(random.randint(0,g.length()))
influencedRand = cascadeGroup(randVert,rand,activeInit)
spreadRand = 0   
for state in influencedRand:
    if state == True:
        spreadRand += 1
print("The spread (Counted active nodes) for randomly selected 5 nodes is:",spreadRand)


print('\n')
print("Calculating Spread of Influence on SalshDot Data")
print("The budget for this example is 50(The report Captures spread for varying budget)")

#Reading Data
#Working On Slashdot Data
slashdot = open('Slashdot0902.txt')
f = slashdot.read()
edges = f.strip().split('\n')

g = Graph()
for edge in edges:
    #print edge
    vertices = edge.strip().split()
    u = int(vertices[0])
    v = int(vertices[-1])
    g.addEdgeDir(u,v)


active = [False for i in range(82169)]
activeInit = [False for i in range(82169)]
   
#k is an integer, representing the budget
#k = int(input("What's your Budget(k) for slashdot Data?:"))
k = 50
#Finding out the most influencial nodes
mostInf = []
for ep in range(k):
    mx = 0
    for vert in g.adjacencylist():        
        if vert not in mostInf:
            neighbour = g.neighbours(vert)
            rand = random.random()
            activeCount = cascade(vert, rand, active)
            if activeCount > mx:
                mx = activeCount
                influence = vert
    mostInf.append(influence)
print("The set of 50 most influencial nodes are:")
print(*mostInf, sep = ' ')

#Set the most influencial nodes as Active

for val in mostInf:
    activeInit[val] = True

#Calculate the influence of most influencial nodes
influenced = cascadeGroup(mostInf,rand,activeInit)
spread = 0
for state in influenced:
    if state == True:
        spread += 1
print("The spread (Counted active nodes) for these selected nodes is:",spread)
print(spread)


#Calculate the influence by randomly selected nodes
randVert = []        
for i in range(k):
    randVert.append(random.randint(0,g.length()))

activeInit = [False for i in range(82169)]
for val in randVert:
    activeInit[val] = True
    
influencedRand = cascadeGroup(randVert,rand,activeInit)
spreadRand = 0   
for state in influencedRand:
    if state == True:
        spreadRand += 1
print("The spread (Counted active nodes) for randomly selected 50 nodes is:",spreadRand)
print(spreadRand)



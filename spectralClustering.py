# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


from collections import defaultdict
#import sys
import random
#import matplotlib as plt
from sklearn.cluster import SpectralClustering
import matplotlib.pyplot as plt
import numpy as np


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



mx = 0
adjlist = g.adjacencylist()
for key in adjlist:
    if key >= mx:
        mx = key
    temp_mx = max(adjlist[key])
    if temp_mx > mx:
        mx = temp_mx
        

adjmat = [[0 for i in range(mx+1)] for j in range(mx+1)]

for key in adjlist:
    neighbours = adjlist[key]
    for n in neighbours:
        adjmat[key][n] = 1
        adjmat[n][key] = 1
    


#Independent Cascade Model
def cascade(vert, rand, activeState, ct):
    
    active = []
    count = 0
    #ct = 0        
    if len(g.neighbours(vert)) != 0:
        #print("here")
        for vertices in g.neighbours(vert):
            if activeState[vertices] != True:  
                #print("Inside ActiveState")
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
            #count += cascade(vertices, rand2, activeState, ct)
            cascade(vertices, rand2, activeState, ct)
    
    #print("here")
    return ct

#Independent Cascade Model(Handles influence of multiple vertices)
def cascadeGroup(vertList, rand, activeState):
    active = []
    count = 0
    ct = 0
    for vert in vertList:
        if len(g.neighbours(vert)) != 0:
            for vertices in g.neighbours(vert):
                if activeState[vertices] != True:
                    rand1 = random.random()
                    if rand1 > rand:            
                        ct += 1
                        active.append(vertices)
                        #print(vertices)
                        activeState[vertices] = True
                    
            #print active
    if len(active) == 0:
        return activeState
    else:
        for vertices in active:
            rand2 = random.random()
            #if activeState[vertices] == False:
            cascade(vertices, rand2, activeState,0)
    return activeState

def calMostInf(g, clust):
        mx = 0
        influence = clust[0]
        for vert in clust:
            #neighbour = g.neighbours(vert)
            rand = random.random()
            activeCount = cascade(vert, rand, active)
            if activeCount > mx:
                mx = activeCount
                influence = vert
        return influence



active = [False for i in range(g.length())]
print("Calculating Spread of Influence on ego-Facebook Data")
print("The budget for this example is 5(The report Captures spread for varying budget)")



mostInf = []
for ep in range(500):
    mx = 0
    for vert in g.adjacencylist():        
        if vert not in mostInf:
            neighbour = g.neighbours(vert)
            rand = random.random()
            activeCount = cascade(vert, rand, active, 0)
            if activeCount > mx:
                mx = activeCount
                influence = vert
    mostInf.append(influence)
#print("The set of 5 most influencial nodes are:")    
#print(*mostInf, sep = ' ')
                

#Set the most influencial nodes as Active
activeInit = [False for i in range(g.length())]
for val in mostInf:
    activeInit[val] = True

#print(mostInf)
#Calculate the influence of most influencial nodes
#print("check1:", len(mostInf))
influenced = cascadeGroup(mostInf,rand,activeInit)
spread = 0
for state in influenced:
    if state == True:
        spread += 1
greedy_spread.append(spread)
#print("The spread (Counted active nodes) for these selected nodes is:",spread)




'''

#k is an integer, representing the budget
#k = int(input("What's your Budget(k) for Facebook Data?:"))
greedy_all = []
clustered_all = []

for epoch in range(1):
    
    print("Sucking at Iteration:", epoch)
    greedy_spread = []
    clustered_spread = []
    
    for k in [2,5,10,20,30,40,50]:
        #k = 60
        #Finding out the most influencial nodes
        #print(k)
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
        #print("The set of 5 most influencial nodes are:")    
        #print(*mostInf, sep = ' ')
                        
        
        #Set the most influencial nodes as Active
        activeInit = [False for i in range(g.length())]
        for val in mostInf:
            activeInit[val] = True
        
        #print(mostInf)
        #Calculate the influence of most influencial nodes
        #print("check1:", len(mostInf))
        influenced = cascadeGroup(mostInf,rand,activeInit)
        spread = 0
        for state in influenced:
            if state == True:
                spread += 1
        greedy_spread.append(spread)
        #print("The spread (Counted active nodes) for these selected nodes is:",spread)
        
        
        sc = SpectralClustering(k, affinity='precomputed', n_init=100)
        sc.fit(adjmat) 
        
        vert_cluster = [[] for i in range(k)]
        
        for idx, clst in enumerate(sc.labels_):
            vert_cluster[clst].append(idx)
        
        activeInit = [False for i in range(g.length())]    
        for clst in vert_cluster:
            mostInf = calMostInf(g, clst)
            activeInit[mostInf] = True
            #print("check2:", mostInf)
            influenced = cascadeGroup([mostInf],rand,activeInit)
            
            
        spread = 0
        for state in influenced:
            if state == True:
                spread += 1
                
        clustered_spread.append(spread)
        #print("The spread (Counted active nodes) in clustering:",spread)
    greedy_all.append(greedy_spread)
    clustered_all.append(clustered_spread)
    
    
greedy_all = np.asarray(greedy_all)
clustered_all = np.asarray(clustered_all)

greedy_smoothed = []
clustered_smoothed = []

for i in [2,5,10,20,30,40,50]:
    greedy_smoothed.append(np.mean(greedy_all[:,i]))
    clustered_smoothed.append(np.mean(clustered_all[:,i]))

    
cost = [i for i in [2,5,10,20,30,40,50]]
plt.plot(cost, greedy_all[0])
plt.plot(cost, clustered_all[0] )
plt.title("Lower Cost Comparision")
plt.xlabel('Cost')
plt.ylabel('Spread')
plt.legend(['Greedy', 'Clustering'])
plt.show()

plt.plot(cost[32:], greedy_smoothed[32:])
plt.plot(cost[32:], clustered_smoothed[32:] )
plt.title("Higher Cost Comparision")
plt.xlabel('Cost')
plt.ylabel('Spread')
plt.legend(['Greedy', 'Clustering'])
plt.show()
        
plt.plot(cost, greedy_smoothed)
plt.plot(cost, clustered_smoothed)
plt.title("Complete Range Comparision")

plt.xlabel('Cost')
plt.ylabel('Spread')
plt.legend(['Greedy', 'Clustering'])
plt.show()
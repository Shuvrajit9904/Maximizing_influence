'''
Algorithm Project Fall 2017
Maximizing the influence of social networks
''' 


import networkx as nx
import time 
import heapq as hq
import random
import time
from priorityQueue import PriorityQueue as PQ


#Independent Cascade Model
#a is the set of initial nodes (k)
#A is set of initial Active nodes
#B is the set of activated nodes in each iteration
def IC_model(G, a, p):

    A=set(a)
    #print A
    B=set(a)
    #print B
    Done=False

    while not Done:
        nextB=set()
        for n in B:
            for m in set(G.neighbors(n)) - A:
                #print set(G.neighbors(n)) - A
                prob=random.random()    #range [0.0, 1.0)
                #print prob
                if prob>p:     
                    nextB.add(m)
                   #print nextB
        B=set(nextB)
        #print B
        if not B:
            Done=True
        A|=B
        #print len(A)
        #print A
    return len(A)


# Weighted Cascade Model
#a is the set of initial nodes (k)
#A is set of initial Active nodes
#B is the set of activated nodes in each iteration
#each edge from node u to v is assigned probability 1/in-degree(v) of activating v
def WC_model(G, a):                 
                                    
    A = set(a)                      
    B = set(a)                     
    Done = False
 
    if nx.is_directed(G):
        node_degree = G.in_degree
    else:
        node_degree = G.degree

    while not Done:
        nextB = set()
        for n in B:
            for m in set(G.neighbors(n)) - A:
                prob = random.random()	#range [0.0, 1.0)
                p = 1.0/node_degree(m)
                if prob <= p:
                    nextB.add(m)
        B = set(nextB)
        if not B:
            Done = True
        A |= B
        #print len(A)
    return len(A)


def high_degree_nodes_gen(k, G):
    most_inf=[]
    if nx.is_directed(G):
        n_degree=G.out_degree
    else:
        n_degree=G.degree
    
    #print G.nodes()
    V=[(n_degree(i),i) for i in G.nodes()]
    V.sort(reverse=True)
    #print V
    N=[t[1] for t in V]
    #print N
    
    for i in range(1,k+1):
        most_inf.append(N[:i])

    print most_inf



def single_discount_high_degree_nodes_gen(k, G):
    if nx.is_directed(G):
        n_degree=G.out_degree
    else:
        n_degree=G.degree
    
    most_inf=[]
    for i in range(k):
        maxoutdegree_i = -1
        v_i = -1
        for v in list(set(G.nodes()) - set(most_inf)):
            outdegree = n_degree(v)
            for u in most_inf:
                if G.has_edge(v, u):
                   outdegree -=1
            if outdegree > maxoutdegree_i:
               maxoutdegree_i = outdegree
               v_i = v
        most_inf.append(v_i)       


#Compute cumulative distance from node to set S

def cumulativeSum (G, S, node):
    cum_d = 0
    for u in S:
        try:
            cum_d += 1+G[node][u]
        except:
            pass
    return cum_d

def farthestNodes(k, G, m=1):
    S=[]
    S_dist=PQ()
    for v in G.nodes():
        if v not in S:
            if m ==1:
               S_dist.add_task(v, cumulativeSum(G, S, v))
    while len(S)<k:
           u, priority= S_dist.pop_item()
           S.append(u)
           for v in G[u].keys():
              if v not in S:
                 [priority, count, task] = S_dist.entry_finder[v]
                 if m == 1:
                       S_dist.add_task(v, priority-1)
    #print S
    
if __name__ =='__main__':
    

    #file='Slashdot0902.txt'
    fh=open("Slashdot0902.txt","rb")
    G=nx.read_edgelist(fh, create_using=nx.DiGraph(), nodetype=int, data=False)
    
    B=single_discount_high_degree_nodes_gen(50, G)
    farthestNodes(50, G, 1)
    p=0.9


    print"*******************Degree Discount Heuristic*********************************"
    b=[2494, 4805, 398, 381, 226, 37, 5706, 4826, 5513, 49, 3482, 217, 2483, 9190, 5685, 5383, 46363, 2830, 385, 5520, 6116, 6513, 2880, 408, 2553, 2828, 8, 1531, 405, 17, 5390, 5652, 6295, 1835, 4828, 7812, 3407, 504, 18363, 5211, 8560, 195, 5453, 7999, 5856, 1651, 3483, 601, 6660, 66746]
    

    print"k=50 nodes selected after running the degree discount heuristic"
    print b
    Y=IC_model(G, b, p)
    Z=WC_model(G,b)
    

    print "The number of activated nodes with Independent Cascade model"
    print Y
    print "The number of activated nodes with Weighted Cascade Model"
    print Z
  
    


    

    print"************Farthest Node Heuristic**************************************"
    a= [0, 1, 4, 128, 154, 169, 9, 49, 4844, 398, 2370, 3, 516, 195, 405, 8, 17, 28, 1229, 408, 413, 189, 96, 50, 2362, 1374, 2494, 2488, 342, 1880, 2379, 2010, 1542, 2413, 11, 4823, 2491, 2542, 1020, 1723, 2500, 2517, 1509, 1559, 1070, 324, 5516, 1531, 86, 1631]
    
    
    print"k=50 nodes selected after running the farthest node heuristic"
    print a
    Y=IC_model(G, a, p)
    Z=WC_model(G,a)
    

    print "The number of activated nodes with Independent Cascade model"
    print Y
    print "The number of activated nodes with Weighted Cascade Model"
    print Z




     
   

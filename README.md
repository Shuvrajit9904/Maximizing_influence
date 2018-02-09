# Maximizing_influence
Algorithm Project for Fall 2017

Instructions to run the program.

Networkx module needs to be installed to run the program `heuristics.py`. 
This module reads the data set and converts it to a graph object. 

The link to data set is https://snap.stanford.edu/data/soc-Slashdot0902.html.

The results were plotted using the Google line chart. 
Separate html/javascript code was written to render the line charts according to our data. 

The program outputs the number of activated nodes with k = 50 for degree discount and farthest node heuristic.
The farthest node heuristic keeps the track of farthest node using a priority queue implementation. 
The following document was followed for the implementation of priority queue:
https://docs.python.org/2/library/heapq.html#priority-queue-implementation-note


How to run the program:
A)
1. Unzip the code. 
2. `heuristics.py` and `priorityQueue.py` should be in the same folder. 
3. Install networkx module for python (pip install networkx)
4. Run `python heuristics.py`

B)
1. In order to get the result for Greedy Heuristic run the following command in the relevant directory(submission):
./run.sh



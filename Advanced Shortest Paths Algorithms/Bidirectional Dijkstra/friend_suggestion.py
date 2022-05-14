#!/usr/bin/python3

import sys
#import queue

'''
To solve this problem alternatively relax the nodes in forward path from s and backward path from t till a common node v is
processed in both forward and backward paths. Store all these nodes in forward and backward path in a common list "workset"

Now find the minimum of distance from s to node x + t to node x for all x in the "workset". This will be required min path

- Worst case running time is O((|V|+|E|)log|V|)
- For road networks it speedup can be 2X but for social networks it can be 1000 times faster
- Memory consumptions is 2X to store G and GR as compared to Djikstra's Algo
'''


import heapq

class BiDij:
    def __init__(self, n):
        self.n = n;                             # Number of nodes
        self.inf = n*10**6                      # All distances in the graph are smaller
        self.d = [[self.inf]*n, [self.inf]*n]   # Initialize distances for forward and backward searches
        self.visited = [False]*n                  # visited[v] == True iff v was visited by forward or backward search
        self.workset = []                       # All the nodes visited by forward or backward search

    def clear(self):
#    """Reinitialize the data structures for the next query after the previous query."""
        for v in self.workset:
            self.d[0][v] = self.d[1][v] = self.inf
            self.visited[v] = False;
        del self.workset[0:len(self.workset)]

    def visit(self, q, side, v, dist): # Relax
#    """Try to relax the distance to node v from direction side by value dist."""
        # Implement this method yourself
        if self.d[side][v] > dist:
            self.d[side][v] = dist
            heapq.heappush(q[side], [self.d[side][v], v]) # Pushing (min_dist, min_index) to heap
            self.workset.append(v)
 
    def extract_min(self, q, side):
        min_dist, min_index = heapq.heappop(q[side])
        return min_index
        
    def process(self, q, side, v, adj, cost):
        for i, u in enumerate(adj[v]):
            self.visit(q, side, u, self.d[side][v] + cost[v][i])

    def shortest_path(self, v):
        distance = self.inf
        for u in self.workset:
            if self.d[0][u] + self.d[1][u] < distance:
                distance = self.d[0][u] + self.d[1][u]                 
        return distance if distance is not self.inf else -1

    def query(self, adj, cost, s, t):
        self.clear()
#        q = [queue.PriorityQueue(), queue.PriorityQueue()]
        q0, q1 = [], []
        heapq.heapify(q0), heapq.heapify(q1)
        q = [q0, q1]
        self.visit(q, 0, s, 0)
        self.visit(q, 1, t, 0)
        
        while len(q[0]) != 0 and len(q[1]) != 0:
            for side in [0,1]:
                v = self.extract_min(q, side) 
                self.process(q, side, v, adj[side], cost[side])
                if self.visited[v]: # Stopping the relaxing as soon as common node is found
                    return self.shortest_path(v)
                self.visited[v] = True         
        return -1

def readl():
    return map(int, sys.stdin.readline().split())
#    return list(map(int, input().split()))

if __name__ == '__main__':
    n,m = readl()
    adj = [[[] for _ in range(n)], [[] for _ in range(n)]] # Index 0 is adj list for G and 1 is GR
    cost = [[[] for _ in range(n)], [[] for _ in range(n)]]
    for e in range(m):
        u,v,c = readl()
        adj[0][u-1].append(v-1)
        cost[0][u-1].append(c)
        adj[1][v-1].append(u-1)
        cost[1][v-1].append(c)
    t, = readl()
    bidij = BiDij(n)
    for i in range(t):
        s, t = readl()
        print(bidij.query(adj, cost, s-1, t-1))

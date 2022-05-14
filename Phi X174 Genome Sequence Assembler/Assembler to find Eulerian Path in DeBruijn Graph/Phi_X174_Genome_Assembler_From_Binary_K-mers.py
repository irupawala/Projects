# Uses Python3

import sys
import threading 
sys.setrecursionlimit(200000)

def createVertices(edges):
    nodes_list = []
    for node in edges:
        nodes_list.append(node[:-1]) # Prefix
        nodes_list.append(node[1:]) # Suffix
    return nodes_list

def createAdjacencyList(edges, nodes):
    adj = [[] for _ in range(len(nodes))]
    in_degree = [0 for _ in range(len(nodes))]
    out_degree = [0 for _ in range(len(nodes))]
    
    for index, edge in enumerate(edges):
        edge_prefix = edge[:-1]
        edge_suffix = edge[1:]
        adj[nodes.index(edge_prefix)].append(nodes.index(edge_suffix))
        out_degree[nodes.index(edge_prefix)] += 1
        in_degree[nodes.index(edge_suffix)] += 1   
        
    return adj, in_degree, out_degree

def graphHasEulerianCycle(in_degree, out_degree):
    start_node, end_node, count = 0,0,0
    for i in range(len(in_degree)):
        diff = in_degree[i] - out_degree[i]
        # for eulerian path to exist difference between in_degree and out_degree needs to be 0
        # except start node which will have one outgoing edge
        # and end node which will have one incoming edge
        if diff == 1:
            end_node = i
        if diff == -1:
            start_node = i
        if diff == 1 or diff == -1:
            count+=1
    if count > 2: return (0,-1,-1)
    else: return (1, start_node, end_node)

def dfs(adj, current_node, path):  
    # While the current node still has outgoing edges
    while len(adj[current_node]) != 0:     
        # select the next unvisited outgoing edge
        next_node = adj[current_node].pop()
        path = dfs(adj, next_node, path)
    
    path.append(int(current_node))    
    return path

def heirholzer(m,edges):    
    nodes = createVertices(edges)
    nodes = sorted(set(nodes))
    adj, in_degree, out_degree = createAdjacencyList(edges, nodes)
    eulerian_exists, start_node, end_node = graphHasEulerianCycle(in_degree, out_degree)
    if eulerian_exists: 
        path = dfs(adj, start_node, [])
    return nodes, path[::-1]

def find_overlap(node, neighbor): # Used at the end of genome to find overlap between first and last edge
    min_overlap_len = 1
    
    start = 0
    while True:
        start = node.find(neighbor[0:min_overlap_len], start)
        if start == -1:
            return (-1, 0)
        if neighbor.startswith(node[start:]):
            overlap_start = start
            overlap_length = len(node) - overlap_start
            return (overlap_start, overlap_length)
        start += 1

def print_output(nodes, path): 
    genome = ""
    for i, next_node_index in enumerate(path):
        
        if i == 0:
            genome = nodes[next_node_index]
        else:
            genome += nodes[next_node_index][-1]
        
    len_edge = len(nodes[0]) + 1 
    first_edge = genome[0:len_edge]
    last_edge = genome[len(genome)-len_edge:]
    overlap_start, overlap_length = find_overlap(last_edge, first_edge)
    if overlap_length > 0: return genome[0:len(genome)-overlap_length]
    else: return genome
    
if __name__ == "__main__":
#def main():
#    input = sys.stdin.read()
#    edges = list(map(str, input.split()))
#    edges = ['AAC', 'ACG', 'CGT', 'GTA', 'TAA']
    edges = ['ACGTACGTAC', 'CGTACGTACG', 'GTACGTACGT', 'TACGTACGTG', 'ACGTACGTGT', 'CGTACGTGTC', 'GTACGTGTCA', 'TACGTGTCAC', 'ACGTGTCACG', 'CGTGTCACGT', 'GTGTCACGTA', 'TGTCACGTAC', 'GTCACGTACG', 'TCACGTACGT', 'CACGTACGTA']

#    edges = list(map(str, input().split()))  
    m = len(edges)
    nodes, path = heirholzer(m,edges)
    print(print_output(nodes, path))
    
#threading.Thread(target=main).start()


'''
Sample Inputs

edges = ['AAC', 'ACG', 'CGT', 'GTA', 'TAA']
edges = ['AAT', 'ATG', 'ATG', 'ATG', 'CAT', 'CCA', 'GAT', 'GCC', 'GGA', 'GGG', 'GTT', 'TAA', 'TGC', 'TGG', 'TGT']
edges = ['ACGTACGTAC', 'CGTACGTACG', 'GTACGTACGT', 'TACGTACGTG', 'ACGTACGTGT', 'CGTACGTGTC', 'GTACGTGTCA', 'TACGTGTCAC', 'ACGTGTCACG', 'CGTGTCACGT', 'GTGTCACGTA', 'TGTCACGTAC', 'GTCACGTACG', 'TCACGTACGT', 'CACGTACGTA']
edges = ['AGCTT', 'GCTTG', 'CTTGA', 'TTGAG', 'TGAGA', 'GAGAT', 'AGATT', 'GATTC', 'ATTCA', 'TTCAG', 'TCAGA', 'CAGAT', 'AGATG', 'GATGG', 'ATGGC', 'TGGCT', 'GGCTA', 'GCTAT', 'CTATG', 'TATGC', 'ATGCG', 'TGCGT', 'GCGTA', 'CGTAA', 'GTAAC', 'TAACT']
edges = ['AGCTT', 'GCTTG', 'CTTGA', 'TTGAG', 'TGAGA', 'GAGAT', 'AGATT', 'GATTC', 'ATTCA']

'''

# TinyGraph algorithms

import tinygraph
import tinygraph.fastutils
from queue import Queue

import numpy as np

from tinygraph.fastutils import get_connected_components
from tinygraph.fastutils import get_shortest_paths

# @profile
# def get_shortest_test(tg, weighted):
#     if not weighted or not np.issubdtype(tg.adjacency.dtype, np.number):
#         distances = np.array([[0 if v == tinygraph.default_zero(tg.adjacency.dtype) 
#                             else 1 for i,v in enumerate(row)] for j,row in 
#                             enumerate(tg.adjacency)],dtype=np.float64)
#     else:
#         distances = np.array([[0 if v == 0 else v for i,v in enumerate(row)] for 
#                             j,row in enumerate(tg.adjacency)],dtype=np.float64)
#     distances = np.array(tinygraph.fastutils._floyd_warshall(distances, tg.node_N))
#     for i in range(tg.node_N):
#         if distances[i][i] < 0:
#             raise Exception("Graph has a negative cycle.")
#     return distances

def get_min_cycles(tg):
    """
    Determines if a node in a graph is part of a cycle, and if so, returns the 
    minimum  sized such cycle (by number of nodes). 
    ? Do we want to create separate functions or try to extend this to
    ? get the minimum cycle by weights or some edge/vertex property?

    Inputs:
        tg (TinyGraph): graph to find cycles in.

    Outputs:
        cycle ([{int}]): A list of the minimum length cycle (by number of nodes)
            for each node in tg. Cycles are represented by a set of the nodes in
            the cycle, and the list is order by node (cycle[0] is min cycle that
            includes node 0).
    """
    # Keep track of min cycle for each node.
    cycles = []
    for i in range(tg.node_N):
        cc = set()
        # Create a FIFO queue to keep track of the nodes which are the same 
        # number of steps from i. Also keep a set which is the nodes on the path 
        # to that node.
        q = Queue()
        cycle_found = False
        init_path = {i,}
        for j in tg.get_neighbors(i):
            q.put((j, init_path))
        while q.qsize() > 1 and not cycle_found:
            currentN, path = q.get()
            new_path = path.copy()
            new_path.add(currentN)
            for j in tg.get_neighbors(currentN):
                if not j in new_path:
                    q.put((j,new_path))
                elif j == i and len(new_path) > 2:
                    cc = new_path
                    cycle_found = True
        cycles.append(cc)
    return cycles

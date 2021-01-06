# TinyGraph algorithms

import tinygraph
import tinygraph.fastutils
from queue import Queue

from tinygraph.fastutils import get_connected_components
# from tinygraph.fastutils import get_shortest_paths

@profile
def get_shortest_paths(tg, weighted):
    """
    Get the distance from each node to each other node on the shortest path. 
    Uses Floyd-Warshall to calculate the distances of the shortest paths.

    Inputs:
        tg (TinyGraph): The graph to find the shortest paths in.

    Outputs:
        distances ([[int]]): A list of the distance to each node. The lists are
            ordered by node number, so distances[0] is a list of the distances 
            from node 0 to the other nodes (e.g. distances[0][3] = distance from
            node 0 to node 3 shortest path from 0 to 3; distances[2][2] = 0 is 
            distance from node 2 to itself). If no path exists between the 
            nodes, the result is None.
        weighted (bool): Whether to consider the weights of the edges, or to 
            consider only the lengths of the path. If weighted is true, the 
            distance of a path is calculated by the sum of the weights on the 
            path. If false, the distance is calculated by the number of nodes on
            the path.
    """
    distances = [[0 if i == j else None for i in range(tg.node_N)]\
                                        for j in range(tg.node_N)]
    for e1, e2, w in tg.edges(weight=True):
        if weighted:
            distances[e1][e2] = w 
            distances[e2][e1] = w
        else:
            distances[e1][e2] = 1 
            distances[e2][e1] = 1
    for k in range(tg.node_N):
        for j in range(tg.node_N):
            for i in range(tg.node_N):
                if not distances[i][k] is None and not distances[k][j] is None:
                    newL = distances[i][k] + distances[k][j]
                    if distances[i][j] is None or distances[i][j] > newL:
                        distances[i][j] = newL
    for i in range(tg.node_N):
        if distances[i][i] < 0:
            raise Exception("Graph has a negative cycle.")
    return distances

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

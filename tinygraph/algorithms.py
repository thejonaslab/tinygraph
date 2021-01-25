# TinyGraph algorithms

import tinygraph
import tinygraph.fastutils
from queue import Queue

import numpy as np

from tinygraph.fastutils import get_connected_components
from tinygraph.fastutils import get_shortest_paths

def is_connected(tg):
    """
    Determines if a graph is fully connected.

    Inputs:
        tg (TinyGraph): graph to check for connectedness.

    Outputs:
        connected (bool): whether the graph is fully connected.
    """
    return len(get_connected_components(tg)) == 1

def get_min_cycles(tg):
    """
    Determines if a vertex in a graph is part of a cycle, and if so, returns the 
    minimum  sized such cycle (by number of vertices). 

    Inputs:
        tg (TinyGraph): graph to find cycles in.

    Outputs:
        cycle ([{int}]): A list of the minimum length cycle (by number of 
            vertices) for each vertex in tg. Cycles are represented by a set of 
            the vertices in the cycle, and the list is order by vertex (cycle[0]
            is min cycle that includes vertex 0).
    """
    # Keep track of min cycle for each vertex.
    cycles = []
    for i in range(tg.vert_N):
        cc = set()
        # Create a FIFO queue to keep track of the vertices which are the same 
        # number of steps from i. Also keep a set which is the vertices on the 
        # path to that vertex.
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

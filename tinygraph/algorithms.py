# TinyGraph algorithms

import tinygraph
from queue import Queue

def get_connected_components(tg):
    """
    Get a list of the connected components in the TinyGraph instance.

    Inputs:
        tg (TinyGraph): graph to find components of.

    Outputs:
        cc ({{int}}): A set of connected components of tg, where each connected
            component is given by a set of the nodes in the component.
    """
    # Track which nodes have not been visited yet, and keep a set with all of 
    # the connected components.
    unseen = set(range(tg.node_N))
    components = set()
    while unseen:
        # While there are still unvisited nodes, start from an unvisited node
        # and explore its connected component.
        comp = set()
        bfs = set()
        start = unseen.pop()
        bfs.add(start)
        while bfs:
            # Explore a new node in the connected component, adding it to the 
            # connected component set and adding its neighbors to the set to 
            # explore next.
            current = bfs.pop()
            comp.add(current)
            for n in tg.get_neighbors(current):
                if n in unseen:
                    bfs.add(n)
        # Add this connected component to the set of connected components.
        components.add(comp)
    return components
            
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
        init_path = set([i])
        for j in tg.get_neighbors(i):
            q.put((j, init_path))
        while q.qsize() > 0 and not cycle_found:
            currentN, path = q.get()
            new_path = path.copy()
            new_path.add(currentN)
            for j in tg.get_neighbors(currentN):
                if len(new_path) > 2 and j == i:
                    cc = new_path
                    cycle_found = True
                elif not j in new_path:
                    q.put((j,path))
        cycles.append(cc)
    return cycles

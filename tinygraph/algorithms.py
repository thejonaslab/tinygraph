# TinyGraph algorithms

import tinygraph

def get_connected_components(tg):
    """
    Get a list of the connected components in the TinyGraph instance.

    Inputs:
        tg (TinyGraph): graph to find components of.

    Outputs:
        cc ([[int]]): A list of connected components, where each connected
            component is given by a list of the nodes in the component.
    """
    pass
            
def get_min_cycle(tg, n):
    """
    Determines if a node in a graph is part of a cycle, and if so, returns the 
    minimum  sized such cycle (by number of nodes). 
    ? Do we want to create separate functions or try to extend this to
    ? get the minimum cycle by weights or some edge/vertex property?

    Inputs:
        tg (TinyGraph): graph to find cycles in.
        n (int): node to search for cycles from.

    Outputs:
        cycle ([int]): The minimum length cycle (by number of nodes) containing
            n or None if no cycle exists.
    """
    pass

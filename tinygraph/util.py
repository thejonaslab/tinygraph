import numpy as np
import tinygraph as tg




def graph_equality(g1, g2):
    """
    Naive check for equality between two graphs. Note that
    this just directly compares adj matrices and the like, 
    this does NOT CHECK FOR ISOMORPHISM
    """

    if not np.array_equal(g1.adjacency, g2.adjacency):
        return False

    if set(g1.v.keys()) != set(g2.v.keys()):
        return False

    if set(g1.e.keys()) != set(g2.e.keys()):
        return False

    for k in g1.v.keys():
        if not np.array_equal(g1.v[k], g2.v[k]):
            return False
    

    for k in g1.e.keys():
        if not np.array_equal(g1.e[k], g2.e[k]):
            return False

    return True
    

    

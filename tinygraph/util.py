import numpy as np
import tinygraph as tg
from tinygraph import EdgeProxy



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
        if not np.array_equal(g1.e_p[k], g2.e_p[k]):
            return False

    return True
    
def permute(g, perm):
    """
    Permute the vertices of a graph to create a new TinyGraph instance.

    Inputs:
        g (TinyGraph): Original TinyGraph to permute. 
        perm (map): A mapping from old vertices to new vertices, such that 
            perm[old_vertex] = new_vertex. 

    Outputs:
        new_g (TinyGraph): A new TinyGraph instance with each vertex, and its
            corresponding vertex and edge properties, permuted.
    """
    new_g = tg.TinyGraph(g.node_N, g.adjacency.dtype, 
                    {p:val.dtype for p, val in g.v.items()},
                    {p:val.dtype for p, val in g.e.items()})
    for (e1, e2, w, d) in g.edges(weight=True, edge_props=g.e.keys()):
        new_g[perm[e1],perm[e2]] = w 
        for prop, val in d.items():
            new_g.e[prop][perm[e1], perm[e2]] = val
    for ind, d in g.vertices(vert_props=g.v.keys()):
        for prop, val in d.items():
            new_g.v[prop][perm[ind]] = val
    return new_g
    

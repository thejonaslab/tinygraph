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

    if not g1.props == g2.props:
        return False

    return True

def subgraph_relabel(g, node_list):
    """
    Helper function to perform the work of permute and subgraph.
    Formally, it returns the subgraph of g induced by node_list (as the set of vertices)

    Inputs:
        g (TinyGraph): Original Tinygraph

        node_list (list): list of indices of nodes to take as the nodes of the subgraph
            Contrary to permute(...), here we expect node_list[new_vertex] = old_vertex
            in order to support dropping (and possibly duplicating) old vertices

    Outputs:
        sg (TinyGraph): subgraph with nodes in the same order as node_list
    """
    N = len(node_list)
    new_g = tg.TinyGraph(N, g.adjacency.dtype,
                    {p:val.dtype for p, val in g.v.items()},
                    {p:val.dtype for p, val in g.e.items()})
    # Copy graph props
    new_g.props = {k:v for k, v in g.props.items()}

    # Magic index converter eliminates python-for-loops
    # at the expense of ignoring sparsity (moves everything)
    new_list = np.arange(N) # list of the new vertices
    # node_list is a list of old vertices ordered by destination indices
    ii = (np.repeat(new_list,  N),  np.tile(new_list,  N))
    jj = (np.repeat(node_list, N),  np.tile(node_list, N))

    # Copy edge values
    new_g.adjacency[ii] = g.adjacency[jj]

    # Copy vertex properties
    for prop in g.v.keys():
        new_g.v[prop][:] = g.v[prop][node_list]

    # Copy edge properties
    for prop in g.e.keys():
        new_g.e_p[prop][ii] = g.e_p[prop][jj]

    return new_g

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
    if  len(perm) != g.node_N \
        or not np.array_equal(np.unique(perm), np.arange(g.node_N)):
        raise IndexError("Invalid permutation passed to permute!")

    # flip the order of stuff in perm
    perm_inv = np.argsort(perm)

    return subgraph_relabel(g, perm_inv)


def subgraph(g, node_list):
    """
    Returns induced subgraph of g on nodes in node_list.
    Grabs all the relevant properties as well.
    Raises an index error in case of invalid nodes in node_list.

    Inputs:
        g (TinyGraph): Original Tinygraph
        node_list (list): list of indices of nodes to take as the nodes of the subgraph

    Output:
        sg (TinyGraph): subgraph
    """
    if np.any(np.array(node_list) > g.node_N) \
       or np.any(np.array(node_list) < 0):
        raise IndexError(f"node_list contains out-of-bounds indices!")

    return subgraph_relabel(g, node_list)

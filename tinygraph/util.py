import numpy as np
import tinygraph as tg
from tinygraph import EdgeProxy
import warnings

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

def subgraph_relabel(g, node_iter):
    """
    Helper function to perform the work of permute and subgraph.
    Formally, it returns the subgraph of g induced by node_iter (as the set of vertices)
    Maintains the ordering of node_iter in constructing the new subgraph.

    Inputs:
        g (TinyGraph): Original Tinygraph

        node_iter (iterable): list of indices of nodes to take as the nodes of the subgraph
            Contrary to permute(), here we expect node_iter[new_vertex] = old_vertex
            in order to support dropping (and possibly duplicating) old vertices

    Outputs:
        sg (TinyGraph): subgraph with nodes in the same order as node_iter
    """
    N = len(node_iter)
    new_g = tg.TinyGraph(N, g.adjacency.dtype,
                    {p:val.dtype for p, val in g.v.items()},
                    {p:val.dtype for p, val in g.e.items()})
    # Copy graph props
    new_g.props = {k:v for k, v in g.props.items()}

    if N == 0:
        # Weird things happen if we keep going ;_;
        return new_g

    # Magic index converter eliminates python-for-loops
    # at the expense of ignoring sparsity (moves everything)
    new_list = np.arange(N) # list of the new vertices
    # node_iter is a list of old vertices ordered by destination indices
    ii = (np.repeat(new_list,  N),  np.tile(new_list,  N))
    jj = (np.repeat(node_iter, N),  np.tile(node_iter, N))

    # Copy edge values
    new_g.adjacency[ii] = g.adjacency[jj]

    # Copy vertex properties
    for prop in g.v.keys():
        new_g.v[prop][:] = g.v[prop][node_iter]

    # Copy edge properties
    for prop in g.e.keys():
        new_g.e_p[prop][ii] = g.e_p[prop][jj]

    return new_g

def permute(g, perm):
    """
    Permute the vertices of a graph to create a new TinyGraph instance.

    Inputs:
        g (TinyGraph): Original TinyGraph to permute.
        perm (dict/list/iterable): A mapping from old vertices to new vertices, such that
            perm[old_vertex] = new_vertex.

    Outputs:
        new_g (TinyGraph): A new TinyGraph instance with each vertex, and its
            corresponding vertex and edge properties, permuted.
    """
    # Internally uses a list
    perm = [perm[i] for i in range(len(perm))]

    if  len(perm) != g.node_N \
        or not np.array_equal(np.unique(perm), np.arange(g.node_N)):
        raise IndexError("Invalid permutation passed to permute!")

    # Flip the order of stuff in perm
    perm_inv = np.argsort(perm)

    return subgraph_relabel(g, perm_inv)

def subgraph(g, nodes):
    """
    Returns induced subgraph of g on nodes in node_list.
    Grabs all the relevant properties as well.
    Raises an index error in case of invalid nodes in node_list.

    Inputs:
        g (TinyGraph): Original TinyGraph
        nodes (iterable): list(/iterable) of indices of nodes to take
            as the nodes of the subgraph

    Output:
        sg (TinyGraph): induced subgraph
    """
    # Internally uses a list
    nodes = list(nodes)

    if  np.any(np.array(nodes) > g.node_N) \
        or np.any(np.array(nodes) < 0):
        raise IndexError(f"nodes list/set contains out-of-bounds indices!")

    return subgraph_relabel(g, nodes)


def merge(g1, g2):
    """
    Produces a new graph resulting from taking the (disjoint) superset of vertices in g1 and g2.
    Raises a TypeError in case the adjacency matrices are of different dtypes.
    Raises a warning in case the vertex or edge properties are different.

    Combine the graph properties, but in case of key collision favors g1's value.


    Inputs:
        g1 (TinyGraph): Original TinyGraph, has precedence for global graph properties
        g2 (TinyGraph): Other original TinyGraph

    Output:
        new_g (TinyGraph): result of the merge
            note: data is detached from any data living within g1 or g2
    """
    # Check for type matching
    if g1.adjacency.dtype != g2.adjacency.dtype:
        raise TypeError("g1 and g2 do not share adjacency matrix types!")
    adj_type = g1.adjacency.dtype

    vp_type1 = {p:val.dtype for p, val in g1.v.items()}
    vp_type2 = {p:val.dtype for p, val in g2.v.items()}
    for k in vp_type1.keys():
        if k in vp_type2.keys():
            if vp_type1[k] != vp_type2[k]:
                raise TypeError(f"dtype for vertex property {k} does not match!")
    vp_types = {**vp_type1, **vp_type2}


    ep_type1 = {p:val.dtype for p, val in g1.e.items()}
    ep_type2 = {p:val.dtype for p, val in g2.e.items()}
    for k in ep_type1.keys():
        if k in ep_type2.keys():
            if ep_type1[k] != ep_type2[k]:
                raise TypeError(f"dtype for vertex property {k} does not match!")
    ep_types = {**ep_type1, **ep_type2}

    # Warnings after errors
    if set(g1.v.keys()) != set(g2.v.keys()):
        warnings.warn("Graph merge: vertex properties don't all match!")
    if set(g1.e.keys()) != set(g2.e.keys()):
        warnings.warn("Graph merge: edge properties don't all match!")

    # Initialize the new merged graph
    N = g1.node_N + g2.node_N
    new_g = tg.TinyGraph(N, adj_type, vp_types, ep_types)

    new_g.props = {**g2.props, **g1.props} # g1 later gives it precedence

    # Vertex properties
    i1 = np.arange(g1.node_N)
    i2 = np.arange(g1.node_N, g1.node_N+g2.node_N)

    for prop, prop_type in vp_types.items():
        # Load stuff from g1
        new_g.v[prop][i1] = g1.v[prop] if prop in vp_type1.keys() \
            else tg.default_zero(prop_type)

        # Load stuff from g2
        new_g.v[prop][i2] = g2.v[prop] if prop in vp_type2.keys() \
            else tg.default_zero(prop_type)

    # Edge indices for easy manipulation
    i11 = (np.repeat(i1, len(i1)), np.tile(i1, len(i1)))
    i12 = (np.repeat(i1, len(i2)), np.tile(i2, len(i1)))
    i21 = (np.repeat(i2, len(i1)), np.tile(i1, len(i2)))
    i22 = (np.repeat(i2, len(i2)), np.tile(i2, len(i2)))

    # Edge weights
    new_g.adjacency[i11] = g1.adjacency.flatten()
    new_g.adjacency[i22] = g2.adjacency.flatten()

    new_g.adjacency[i12] = tg.default_zero(adj_type)
    new_g.adjacency[i21] = tg.default_zero(adj_type)

    # Edge properties
    for prop, prop_type in ep_types.items():
        new_g.e_p[prop][i11] = g1.e_p[prop].flatten() if prop in ep_type1.keys() \
            else tg.default_zero(prop_type)

        new_g.e_p[prop][i22] = g2.e_p[prop].flatten() if prop in ep_type2.keys() \
            else tg.default_zero(prop_type)

        new_g.e_p[prop][i12] = tg.default_zero(prop_type)
        new_g.e_p[prop][i21] = tg.default_zero(prop_type)

    return new_g

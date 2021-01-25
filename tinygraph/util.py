import numpy as np
import tinygraph as tg
from tinygraph import EdgeProxy
from copy import deepcopy
import warnings

def graph_equality(g1, g2):
    """
    Naive check for equality between two graphs. Note that this just directly 
    compares adj matrices and the the like. This does NOT CHECK FOR ISOMORPHISM.

    Inputs:
        g1 (TinyGraph): First graph instance.
        g2 (TinyGraph): Second graph instance.

    Outputs:
        equal (bool): Are the two graph instances equal to each other.
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

def _subgraph_relabel(g, vert_iter):
    """
    Helper function to perform the work of permute and subgraph. Not intended 
    for use by end-users. See instead functions permute and subgraph below.

    Returns the subgraph of g induced by vert_iter (as the set of vertices), 
    maintaining the ordering of vert_iter in constructing the new subgraph.

    Inputs:
        g (TinyGraph): Original Tinygraph

        vert_iter (iterable): iterable containing indices of vertices to take as
            the vertices of the subgraph. Contrary to permute(), here we expect
                vert_iter[new_vertex] = old_vertex
            to support dropping (and possibly duplicating) old vertices.

    Outputs:
        sg (TinyGraph): subgraph with vertices in the same order as vert_iter.
    """
    N = len(vert_iter)
    new_g = tg.TinyGraph(N, g.adjacency.dtype,
                    {p:val.dtype for p, val in g.v.items()},
                    {p:val.dtype for p, val in g.e.items()})
    # Copy graph props
    # new_g.props = {k:v for k, v in g.props.items()}
    new_g.props = deepcopy(g.props)

    if N == 0:
        # Weird things happen if we keep going ;_;
        return new_g

    # Magic index converter eliminates python-for-loops
    # at the expense of ignoring sparsity (moves everything)
    new_list = np.arange(N) # list of the new vertices
    #vert_iter is a list of old vertices ordered by destination indices
    old_indices = (np.repeat(new_list,  N),  np.tile(new_list,  N))
    new_indices = (np.repeat(vert_iter, N),  np.tile(vert_iter, N))

    # Copy edge values
    new_g.adjacency[old_indices] = g.adjacency[new_indices]

    # Copy vertex properties
    for prop in g.v.keys():
        new_g.v[prop][:] = g.v[prop][vert_iter]

    # Copy edge properties
    for prop in g.e.keys():
        new_g.e_p[prop][old_indices] = g.e_p[prop][new_indices]

    return new_g

def permute(g, perm):
    """
    Permute the vertices of a graph to create a new TinyGraph instance.

    Inputs:
        g (TinyGraph): Original TinyGraph to permute.
        perm (iterable): A mapping from old vertices to new vertices, such that
            perm[old_vertex] = new_vertex.

    Outputs:
        new_g (TinyGraph): A new TinyGraph instance with each vertex, and its
            corresponding vertex and edge properties, permuted.
    """
    # Internally uses a list
    perm = [perm[i] for i in range(len(perm))]

    if  len(perm) != g.vert_N \
        or not np.array_equal(np.unique(perm), np.arange(g.vert_N)):
        raise IndexError("Invalid permutation passed to permute!")

    # Flip the order of stuff in perm
    perm_inv = np.argsort(perm)

    return _subgraph_relabel(g, perm_inv)

def subgraph(g, vertices):
    """
    Returns induced subgraph of g on vertices in vert_list.
    Grabs all the relevant properties as well.
    Raises an index error in case of invalid vertices in vert_list.

    Inputs:
        g (TinyGraph): Original TinyGraph.
        vertices (iterable): iterable of indices of vertices to take
            as the vertices of the subgraph.

    Output:
        sg (TinyGraph): induced subgraph.
    """
    # Internally uses a list
    vertices = list(vertices)

    if  np.any(np.array(vertices) > g.vert_N) \
        or np.any(np.array(vertices) < 0):
        raise IndexError(f"vertices iterable contains out-of-bounds indices!")

    return _subgraph_relabel(g, vertices)


def merge(g1, g2):
    """
    Produces a new graph resulting from taking the (disjoint) superset of 
    vertices in g1 and g2. Raises a TypeError in case the adjacency matrices are
    of different dtypes. Raises a warning in case the vertex or edge properties 
    are different. Combines the graph properties, but in case of key collision 
    favors g1's value.

    Inputs:
        g1 (TinyGraph): Original TinyGraph - global graph properties precedence.
        g2 (TinyGraph): Other original TinyGraph.

    Output:
        new_g (TinyGraph): result of the merge. Note: data is detached from any
            data living within g1 or g2.
    """
    # Check for type matching
    if g1.adjacency.dtype != g2.adjacency.dtype:
        raise TypeError("g1 and g2 do not share adjacency matrix types: "
                        f"({g1.adjacency.dtype} vs {g2.adjacency.dtype})!")
    adj_type = g1.adjacency.dtype

    vp_type1 = {p:val.dtype for p, val in g1.v.items()}
    vp_type2 = {p:val.dtype for p, val in g2.v.items()}
    for k in vp_type1.keys():
        if k in vp_type2.keys():
            if vp_type1[k] != vp_type2[k]:
                raise TypeError(f"dtype for vertex property '{k}' does not"
                                f"match: {vp_type1[k]} vs {vp_type2[k]}")
    vp_types = {**vp_type1, **vp_type2}


    ep_type1 = {p:val.dtype for p, val in g1.e.items()}
    ep_type2 = {p:val.dtype for p, val in g2.e.items()}
    for k in ep_type1.keys():
        if k in ep_type2.keys():
            if ep_type1[k] != ep_type2[k]:
                raise TypeError(f"dtype for edge property '{k}' does not match:"
                                f" {ep_type1[k]} vs {ep_type2[k]}")
    ep_types = {**ep_type1, **ep_type2}

    # Warnings after errors
    if set(g1.v.keys()) != set(g2.v.keys()):
        warnings.warn(f"util.merge: vertex properties don't all match but will "
                      f"be merged automatically: {set(g1.v.keys())} and "
                      f"{set(g2.v.keys())} will result in "
                      f"{set(g1.v.keys()).union(set(g2.v.keys()))}")
    if set(g1.e.keys()) != set(g2.e.keys()):
        warnings.warn(f"util.merge: edge properties don't all match but will be"
                      f" merged automatically: {set(g1.e.keys())} and "
                      f"{set(g2.e.keys())} will result in "
                      f"{set(g1.e.keys()).union(set(g2.e.keys()))}")

    # Initialize the new merged graph
    N = g1.vert_N + g2.vert_N
    new_g = tg.TinyGraph(N, adj_type, vp_types, ep_types)

    new_g.props = {**g2.props, **g1.props} # g1 later gives it precedence

    # Vertex properties
    i1 = np.arange(g1.vert_N)
    i2 = np.arange(g1.vert_N, g1.vert_N+g2.vert_N)

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
        new_g.e_p[prop][i11] = g1.e_p[prop].flatten() \
            if prop in ep_type1.keys() else tg.default_zero(prop_type)

        new_g.e_p[prop][i22] = g2.e_p[prop].flatten() \
            if prop in ep_type2.keys() else tg.default_zero(prop_type)

        new_g.e_p[prop][i12] = tg.default_zero(prop_type)
        new_g.e_p[prop][i21] = tg.default_zero(prop_type)

    return new_g

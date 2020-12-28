# Functions for interactions between networkx and tinygraph.

import numpy as np
import networkx
import tinygraph as tg

# For slightly cleaner type inference
import numbers

def tg_from_nx(ng, adj_type=np.int32, weight_prop=None, vp_types={}, ep_types={},
               error_mode=True):
    """
    Initialize a TinyGraph instance from a networkx graph instance.
    Grabs only the requested vertex and edge properties;
    If weight_prop is set, then the adjacency matrix will contain
      values from edges' `weight` property.

    Inputs:
        ng (networkx Graph):
            Graph to translate to TinyGraph.

        adj_type:
            Tell what adjacency type to expect (for TinyGraph creation).

        vp_types (dictionary of prop(string)->type):
            Tell us which vertex properties to grab (and how much space to allocate).

        ep_types (dictionary of prop(string)->type):
            Tell us which edge properties to grab (and how much space to allocate).

        error_mode (bool):
            In case properties aren't found, we raise a KeyError by default.
            Setting error_mode to false would result in quietly filling in values.

    Outputs:
        tg (TinyGraph): TinyGraph instance corresponding to networkx graph.
    """
    # First create an instance with the right node size
    g = tg.TinyGraph(ng.order(), \
                     adj_type=adj_type, \
                     vp_types=vp_types, \
                     ep_types=ep_types)
    # g.node_names = list(ng.nodes.keys())
    # g.graph = ng.graph

    # Get vertex properties
    v_names = list(ng.nodes.keys())
    v_props = list(ng.nodes.values())
    v_name_to_num = dict([(vn, i) for i, vn in enumerate(ng.nodes.keys())])
    g.v['name'] = np.array(v_names, dtype=np.object)

    for vi in range(ng.order()):
        v_prop = v_props[vi]

        for vp in vp_types.keys():
            if vp in v_prop.keys():
                g.v[vp][vi] = v_prop[vp]
            elif error_mode:
                raise KeyError("Property {} absent from vertex {}".format( \
                                vp, v_names[vi]))

            # Default values
            elif issubclass(vp_types[vp], numbers.Number):
                # Is this a desirably default value?
                g.v[vp][vi] = -1
            else:
                # Seems clearer to put None than "" for strings
                g.v[vp][vi] = None


    # Get edge properties and also adjacency matrix
    e_names = list(ng.edges.keys())
    e_props = list(ng.edges.values())
    for ei in range(ng.size()):
        e_prop = e_props[ei]
        v1_num = v_name_to_num[e_names[ei][0]]
        v2_num = v_name_to_num[e_names[ei][1]]

        # Ignore self-connected edges
        # But if there are multiple edges, maybe just overwrite..
        if v1_num == v2_num:
            if error_mode:
                print("Warning: Skipping a self-edge")
            continue

        # Fetch properties
        for ep in ep_types.keys():
            if ep in e_prop.keys():
                # Two entries because undirected graph
                g.e[ep][v1_num, v2_num] = e_prop[ep]
                g.e[ep][v2_num, v1_num] = e_prop[ep]
            else:
                raise KeyError("Property {} absent from edge {}".format( \
                                ep, e_names[ei]))

        # Build adjacency matrix with possibly weighted entries
        if weight_prop is None:
            g.adjacency[v1_num, v2_num] = 1
            g.adjacency[v2_num, v1_num] = 1
        else:
            if weight_prop in e_prop.keys():
                g.adjacency[v1_num, v2_num] = e_prop[weight_prop]
                g.adjacency[v2_num, v1_num] = e_prop[weight_prop]
            elif error_mode:
                raise KeyError("Weight Property '{}' absent from edge {}".format( \
                               weight_prop, e_names[ei]))
            else:
                # Currently set to 0, but should we allow for legal edges
                # with weight 0? (in which case we should change this to -1)
                g.adjacency[v1_num, v2_num] = 0
                g.adjacency[v2_num, v1_num] = 0
    return g


def tg_to_nx(g, weight_prop=None):
    """
    Get a networkx copy of the current graph.
    Grabs all the properties it can find and uses the node_names property for node names.

    Inputs:
        tg (TinyGraph): graph to translate to networkx.
        weight_prop:    key to put the adjacency matrix values into
                        (None to interpret as unweighted)

    Outputs:
        g (networkx Graph): networkx graph of TinyGraph instance.
    """
    # In case weight_prop is already a property
    if weight_prop in g.e.keys():
        print("tg_to_nx warning: weight_prop collides with an existing property. "
              "Will overwrite existing values during conversion!")

    # Make the new network
    ng = networkx.Graph()
    # ng.graph = g.graph

    # Fetch vertices
    node_names = [g.v['name'][i] for i in range(g.node_N)] \
        if 'name' in g.v.keys() else list(range(g.node_N))

    ng.add_nodes_from(node_names)
    for i in range(g.node_N):
        iname = node_names[i]
        for key in g.v.keys():
            ng.nodes[iname][key] = g.v[key][i]

    # Fetch edges
    # Loop is such that i<j
    for i in range(g.node_N):
        iname = node_names[i]
        for j in range(i+1, g.node_N):
            jname = node_names[j]
            edge_val = g[i, j]

            # Consider there to be an edge if the weight is > 0
            # No legal negative edge weights allowed!
            if edge_val > 0:
                ng.add_edge(iname, jname)
                for ep in g.e.keys():
                    ng.edges[iname, jname][ep] = g.e[ep][i, j]

                # Now write to the `weight_prop` property (possibly overwriting)
                ng.edges[iname, jname][weight_prop] = edge_val

    return ng


def to_binary(g, fileobj): 
    """
    Convert tiny graph to fast binary representation for storage.
    Note this is just a compressed npz from numpy with some 
    help around attribute names
    Inputs:
         tg: TinyGraph
         fileobj : Python file-like object 

    Returns : None
    """
    
    fields = {'adjacency' : g.adjacency}
    for k, v in g.v:
        fields[f'vp_{k}'] = v
    for k, v in g.e:
        fields[f'ep_{k}'] = v
        
    np.savez_compressed(fileobj, **fields)
    
def from_binary(fileobj):
    """
    Load TinyGraph from binary representation. Note there
    is minimal sanity checking here for speed. 

    Input:
        fileobj : Python file-like object
    Returns:
        new tinygraph
    """
    d = np.load(fileobj)
    adj = d['adjacency']
    vp = {}
    ep = {}
    for k in d.keys():
        if k.startswith("vp_"):
            vp[k[3:]] = d[k]
        elif k.startswith("ep_"):
            ep[k[3:]] = d[k]
        elif k == 'adjacency':
            pass
        else:
            raise ValueErorr(f"unknown field {k} in npz file")
    g = tg.TinyGraph(adj.shape[0], adj.dtype, 
                   vp_types = {k : v.dtype for k, v in vp.items()}, 
                   ep_types = {k : v.dtype for k, v in ep.items()}, 
                  )
    g.adjacency[:] = adj

    # copy over the properties directly
    for k, v in vp.items():
        g.v[k][:] = v
    for k, v in ep.items():
        g.e[k][:] = v
        
    return g

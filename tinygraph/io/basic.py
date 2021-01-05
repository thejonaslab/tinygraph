# Functions for interactions between networkx and tinygraph.

import numpy as np
import networkx
import tinygraph as tg
import json

# For slightly cleaner type inference
import numbers

def from_nx(ng, adj_type=np.int32,
            weight_prop=None,
            name_prop=None,
            vp_types={}, ep_types={},
            raise_error_on_missing_prop=True):
    """
    Initialize a TinyGraph instance from a networkx graph instance.
    Grabs only the requested vertex and edge properties;
    If weight_prop is set, then the adjacency matrix will contain
      values from edges' `weight` property.

    Inputs:
        ng (networkx Graph):
            Graph to translate to TinyGraph.

        adj_type:
            the adjacency type to expect (for TinyGraph creation).

        weight_prop:
            Name of the weight property in the networkx graph (put in adj matrix).
            If None, value defaults to 1.

        name_prop:
            vertex property to put the networkx node name into (e.g., 'name').
            None results in discarding the vertex name.

        vp_types (dictionary of prop(string)->type):
            vertex properties to grab (and how much space to allocate).

        ep_types (dictionary of prop(string)->type):
            edge properties to grab (and how much space to allocate).

        raise_error_on_missing_prop (bool):
            In case properties aren't found, we raise a KeyError by default.
            Setting raise_error_on_missing_prop to false would result in quietly filling in values.

    Outputs:
        tg (TinyGraph): TinyGraph instance corresponding to networkx graph.
    """
    # First create an instance with the right node size
    g = tg.TinyGraph(ng.order(), \
                     adj_type=adj_type, \
                     vp_types=vp_types, \
                     ep_types=ep_types)

    # Get vertex properties
    v_names = list(ng.nodes.keys())
    v_props = list(ng.nodes.values())
    v_name_to_num = dict([(vn, i) for i, vn in enumerate(ng.nodes.keys())])
    if name_prop is not None:
        g.v[name_prop] = np.array(v_names, dtype=np.str)

    for vi in range(ng.order()):
        v_prop = v_props[vi]

        for vp in vp_types.keys():
            # Grab the properties, but try to be graceful
            if vp in v_prop.keys():
                g.v[vp][vi] = v_prop[vp]
            elif raise_error_on_missing_prop:
                raise KeyError(f"Property '{vp}' absent from vertex {v_names[vi]}")
            # else:
            #     try:
            #         g.v[vp][vi] = tg.default_zero(vp_types[vp])
            #     except ValueError:
            #         g.v[vp][vi] = None

            # Default values
            elif issubclass(vp_types[vp], numbers.Number):
                # Is this a desirable default value?
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
            raise ValueError(f"Error: Conversion from networkx graph to tinygraph "
                             f"failed. Self-connected edge found for vertex "
                             f"{e_names[ei][0]}.")
            continue
        # Build adjacency matrix with possibly weighted entries
        if weight_prop is None:
            g[v1_num, v2_num] = tg.default_one(adj_type)
        else:
            # Want to load weights
            if weight_prop in e_prop.keys():
                g[v1_num, v2_num] = e_prop[weight_prop]
            elif raise_error_on_missing_prop:
                raise KeyError(f"Weight Property '{weight_prop}' absent "
                               f"from edge {e_names[ei]}")
            else:
                # If no weight is given, set to one for now
                g[v1_num, v2_num] = tg.default_one(adj_type)
        # Fetch properties
        for ep in ep_types.keys():
            if ep in e_prop.keys():
                # TODO: Update once the edge proxy is implemented
                eprop = e_prop[ep]
            elif not raise_error_on_missing_prop:
                eprop = tg.default_zero(ep_types[ep])
            else:
                raise KeyError(f"Property '{ep}' absent from edge {e_names[ei]}")
            g.e[ep][v1_num, v2_num] = eprop
            g.e[ep][v2_num, v1_num] = eprop

    # global properties
    for k, v in ng.graph.items():
        g.props[k] = v
    
    return g


def to_nx(g, weight_prop=None, name_prop=None, vp_subset=None, ep_subset=None):
    """
    Get a networkx copy of the current graph.
    Grabs all the properties it can find and uses the node_names property for node names.

    Inputs:
        tg (TinyGraph): graph to translate to networkx.
        weight_prop:
            key to put the adjacency matrix values into (None to interpret as unweighted)
        name_prop:
            vertex property from g to take as the node name (e.g. 'name').
            If None is supplied, the name will be the vertex number.
            If an invalid string (not a key of g.v) is passed, a KeyError will be raised
        vp_subset:
            Vertex properties to take; None to take all.
            A KeyError will be raised if not all are found.
        ep_subset:
            Edge properties to take; None to take all.
            A KeyError will be raised if not all are found.

    Outputs:
        g (networkx Graph): networkx graph of TinyGraph instance.
    """
    # In case weight_prop is already a property
    if weight_prop in g.e.keys():
        print("tg_to_nx warning: weight_prop collides with an existing property. "
              "Will overwrite existing values during conversion!")

    # Make the new network
    ng = networkx.Graph()

    # Fetch nodes' names
    if name_prop is None:
        # Default to indices
        node_names = list(range(g.node_N))
    elif name_prop in g.v.keys():
        # Take the passed vertex property if avaliable
        node_names = [g.v[name_prop][i] for i in range(g.node_N)]
    else:
        raise KeyError(f"Error: to_nx could not find name_prop "
                       f"({name_prop}) for the passed tinygraph")

    # Make None to mean the full set for convenience
    # But, if name_prop is set, ignore the name
    if vp_subset is None:
        vp_subset = list(g.v.keys())
    if name_prop and name_prop in vp_subset:
        vp_subset.remove(name_prop)

    # If weight_prop is set, add the edge weight property
    if ep_subset is None:
        ep_subset = g.e.keys()

    # Drop node names and vertex properties
    ng.add_nodes_from(node_names)
    for i in range(g.node_N):
        iname = node_names[i]

        for key in vp_subset:
            if key in g.v.keys():
                ng.nodes[iname][key] = g.v[key][i]
            else:
                raise KeyError(f"Error: to_nx could not find requested "
                               f"vertex property {key}.")

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
                for ep in ep_subset:
                    if ep in g.e.keys():
                        ng.edges[iname, jname][ep] = g.e[ep][i, j]
                    else:
                        raise KeyError(f"Error: to_nx could not find requested "
                                       f"edge property {ep}.")

                # Now write to the `weight_prop` property (possibly overwriting)
                if weight_prop is not None:
                    ng.edges[iname, jname][weight_prop] = edge_val

    for k, v in g.props.items():
        ng.graph[k] = v
        
    return ng


def to_binary(g, fileobj):
    """
    Convert tiny graph to fast binary representation for storage.
    Note this is just a compressed npz from numpy with some
    help around attribute names. Note that per-graph properties
    are serialized as a json string. 
    Inputs:
         tg: TinyGraph
         fileobj : Python file-like object

    Returns : None
    """

    fields = {'adjacency' : g.adjacency}
    for k, v in g.v.items():
        fields[f'vp_{k}'] = v
    for k, v in g.e.items():
        fields[f'ep_{k}'] = v


    if len(g.props) > 0:
        props = json.dumps(g.props)        
        fields['props'] = np.array(props)
        
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
    props = {}
    for k in d.keys():
        if k.startswith("vp_"):
            vp[k[3:]] = d[k]
        elif k.startswith("ep_"):
            ep[k[3:]] = d[k]
        elif k == 'adjacency':
            pass
        elif k == 'props':
            props = json.loads(d[k].tobytes())
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

    g.props = props

    return g

.. _quickstart:

Quickstart
==========

This walkthrough will demonstrate the basic functionality of TinyGraph, and show
the most important features and algorithms.

TinyGraph is a package that uses numpy arrays, so we recommend importing numpy
in order to get the most out of TinyGraph. Networkx is also useful as it
interfaces well with TinyGraph and has additional features.

Basic functionality
----------------------------

Setting up a graph can be done simply by initializing the number of vertices in
the graph. By default, edge weights are floats, and can be assigned as shown here.

.. code-block:: python

    import numpy as np
    import networkx as nx
    
    import tinygraph as tg

    vertex_n = 10
    g = tg.TinyGraph(vertex_n)
    
    g[0,1] = 2.7
    g[3,4] = 3.1
    
    print(g.vert_N)
    print(g.edge_N)

TinyGraph also supports vertex and edge properties. Properties, including edge
weight types can be of any type. However, they will be stored in numpy array, so
using numpy types can improve performance. Edge and vertex properties can be
accessed using .e and .v, respectively. Edge weights, edge properties, and
vertex properties are all given default 0 values on initialization, where the
default 0 for booleans is False and for strings it is an empty string. However,
attempting to access or set edge properties for edges that do not exist will
throw an error.

.. code-block:: python

    g = tg.TinyGraph(vertex_n,adj_type=np.int32,vp_types={'color': np.int32,
                                                          'is_special': np.bool},
                                                ep_types={'width': np.int32})
    
    g[0,1] = 1
    g[3,4] = 2
    
    g.v['is_special'][5] = True\
    g.v['color'][:] = 10
    
    g.e['width'][3,4] = 4

We also have simple functions for looping over the edges and vertices, given a
list of properties to return. The properties will be returned in a map for each
edge or vertex. For each edge, the weight can also be returned, if the parameter
is passed as True.

.. code-block:: python

    for e1, e2, w, props in g.edges(True, ['width']):
        print(e1, e2, w, props['width'])

    for v, props in g.vertices(['color','is_special']):
        if props['is_special']:
            print(v, props['color'])

There are other functions for making copies, getting a vertex's neighbors and
adding or removing vertices, edge properties or vertex properties. Edges can be
removed by setting their weight to 0.

Working with Networkx
----------------------------

Networkx has an extensive library of graph functions, including for generating
and displaying graphs. TinyGraph provides easy interface with networkx to take
advantage of those functions. For example, networkx provides a function for
drawing graphs.

.. code-block:: python

    ng = nx.generators.classic.cycle_graph(4)
    ng.graph['name'] = "Cycle"
    ng.nodes[0]['color'] = 0
    ng.nodes[1]['color'] = 1
    ng.nodes[2]['color'] = 0 
    ng.nodes[3]['color'] = 1 
    ng.edges[0, 1]['weight'] = 1
    ng.edges[1, 2]['weight'] = 2
    ng.edges[2, 3]['weight'] = 3
    ng.edges[3, 0]['weight'] = 4
    
    node_colors = [0, 1, 0, 1]
    nx.draw(ng, node_color=node_colors)

Using TinyGraph's to and from networkx functions, we can get translate between
networkx and TinyGraph accurately.

.. code-block:: python

    g = tg.io.from_nx(ng, name_prop='name', vp_types={'color': np.int})

    assert tg.io.to_nx(g, name_prop='name').nodes.data() == ng.nodes.data()

Working with RDKit
----------------------------

TinyGraph was developed with the intention of being used as a way to perform
graph algorithms on molecules. We therefore provide easy interfacing with RDKit,
including to and from the RDKit molecules.

.. code-block:: python

    from rdkit import Chem
    import tinygraph.io.rdkit
    
    mol = Chem.MolFromSmiles('CC')
    mol = Chem.AddHs(mol)
    g = tg.io.rdkit.from_rdkit_mol(mol, use_charge=True, use_chiral=True)
    nx.draw(tg.io.to_nx(g))

    new_mol = tg.io.rdkit.to_rdkit_mol(g, charge_prop='charge',chiral_prop='chiral')
    new_smiles = Chem.MolToSmiles(new_mol)

Algorithms
----------------------------

TinyGraph implements its own version of common graph algorithms which are
efficient on the small, undirected, self-loop free graphs it supports. TinyGraph
implements its own connected components, minimum cycle detection, and shortest
path algorithms. For details on all of TinyGraph's algorithms, see :ref:`api`.

.. code-block:: python

    import tinygraph.algorithms as algs\n",
    
    g3 = tg.TinyGraph(vertex_n,adj_type=np.int32,vp_types={'color': np.int32,
                                                          'is_special': np.bool},
                                                ep_types={'width': np.int32})
    
    g3[0,1] = 1
    g3[3,4] = 2
    g3[1,2] = 2
    g3[0,2] = 1
    g3[0,3] = 1
    g3[4,5] = 1
    g3[0,5] = 4
    g3[6,7] = 1
    g3[8,9] = 2

    print(algs.get_connected_components(g3))

    print(algs.get_min_cycles(g3))

    sp_w = algs.get_shortest_paths(g3, True)
    sp_uw = algs.get_shortest_paths(g3, False)
    
    print(sp_uw[0][5])
    print(sp_w[0][5])

Saving and Loading TinyGraphs
----------------------------

TinyGraph has functions for saving and loading graphs to and from binary. The
expectation is that there may be datasets containing millions of graphs.
TinyGraph's io has been benchmarked for strong space and time performance on
saving and loading.

.. code-block:: python

    import io
    outbuf = io.BytesIO()
    tg.io.to_binary(g, outbuf)
    s = outbuf.getvalue() # mostly not human-readable but great for writing to disk!

    inbuf = io.BytesIO(s)
    g2 = tg.io.from_binary(inbuf)

Extra Utilities
----------------------------

Lastly, TinyGraph provides graph utility functions for ease of use. This includes
graph equality, permuting graphs, taking subgraphs and merging graphs.

To permute a graph, pass any map from the old vertices to the new vertices.
Permute returns a new graph, translating over the edges, weights and properties
from the original.

.. code-block:: python

    perm = {0: 5, 1: 2, 2:1, 3: 7, 4:0, 5: 6, 6: 4, 7: 3}
    # 0 -> 5, 1->2, etc.
    g_permuted = tg.util.permute(g, perm)
    print(g_permuted)

Subgraph takes in an iterable and returns a new graph with only the provided
vertices, reindexed by their position on the iterable. Edges and properties are
again brought over.

.. code-block:: python

    just_carbons = set([0, 1])
    g_c = tg.util.subgraph(g, just_carbons)
    print(g_c)

Lastly, merge combines two graphs, putting the first graph's vertices as the
first vertices. Edges and properties are maintained where possible, with default
values put in if a property is not present in one of the graphs. When collisions
occur, priority is given to the first graph, such as if the adjacency matrix data
types are different.

.. code-block:: python

    g_both = tg.util.merge(g_c, g)
    print(g_both)
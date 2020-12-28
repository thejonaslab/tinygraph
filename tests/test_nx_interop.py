# Test the interaction between networkx graphs and tinygraph

import numpy as np
import networkx
import tinygraph as tg
import pytest


        
@pytest.mark.xfail
def basic_from_nx():
    "Basic test for main functionality"
    # Should look like methane except the weightings are meaningless
    ng = networkx.Graph()
    ng.add_weighted_edges_from([ \
        ('C1', 'H1', 1),   \
        ('C1', 'H2', 2),   \
        ('C1', 'H3', 0.5), \
        ('C1', 'H4', 1.8)  \
    ])
    ng.nodes['C1']['element'] = 'Carbon'
    ng.nodes['H1']['element'] = 'Hydrogen'
    ng.nodes['H2']['element'] = 'Hydrogen'
    ng.nodes['H3']['element'] = 'Hydrogen'
    # ng.nodes['H4']['element'] = 'Hydrogen' # omitted to test the exception-handling

    ng.nodes['C1']['atomic number'] = 6

    ng.edges['C1', 'H1']['bond'] = True
    ng.edges['C1', 'H2']['bond'] = True
    ng.edges['C1', 'H3']['bond'] = True
    ng.edges['C1', 'H4']['bond'] = True

    t = tg.io.tg_from_nx(ng,
                         adj_type=np.float,
                         weight_prop='weight',
                         vp_types={'element': np.object, 'atomic number': np.int},
                         ep_types={'bond': np.bool},
                         error_mode=False
    )
    ng2 = tg.io.tg_to_nx(t, weight_prop='weight')
    return ng, t, ng2

# @pytest.mark.xfail
def test_basic_from_nx():
    ng, t, ng2 = basic_from_nx()

    # Assertion statements...
    assert(ng.order() == ng2.order())
    assert(ng.size()  == ng2.size())
    assert(ng.nodes.keys()   == ng2.nodes.keys())

    # Add more careful stuff too..

    # Check vertex properties up to 'name'
    # But new entries can be produced
    for v in ng.nodes:
        props = ng.nodes[v].keys()
        for prop in props:
            if prop in ng2.nodes[v].keys():
                assert(ng.nodes[v][prop] == ng2.nodes[v][prop])
            else:
                assert(prop == 'name')

    # Edge properties up to 'weight'
    for e in ng.edges:
        assert(e in ng2.edges())

        for prop in props:
            if prop in ng2.edges[e].keys():
                assert(ng.edges[e][prop] == ng2.edges[e][prop])
            else:
                assert(prop == 'weight')

# @pytest.mark.xfail
def test_triangle():
    t = tg.TinyGraph(3, vp_types={'name': np.str})
    t[0, 1] = 1
    t[1, 2] = 1.1
    t[2, 0] = 3

    t.v['name'][0] = 'a'
    t.v['name'][1] = 'b'
    t.v['name'][2] = 'c'

    ng = tg.io.tg_to_nx(t, weight_prop = 'weight')
    t2 = tg.io.tg_from_nx(ng, weight_prop='weight', vp_types={'name': np.str})

    assert(np.all(t.adjacency == t2.adjacency))
    assert(np.all(t.v['name'] == t2.v['name']))

# @pytest.mark.xfail
def test_vanishing_edge():
    """Current behavior is for 0-weighted edges to vanish"""
    t = tg.TinyGraph(2)
    t[0, 1] = 0
    ng = tg.io.tg_to_nx(t)
    t2 = tg.io.tg_from_nx(ng)

    assert (np.all(t2.adjacency == 0))

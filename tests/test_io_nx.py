# Test the interaction between networkx graphs and tinygraph

import numpy as np
import networkx
import tinygraph as tg
import pytest
import graph_test_suite

# Graph test suite tests
basic_suite = graph_test_suite.create_suite()
vp_suite = graph_test_suite.create_suite_vert_prop()
ep_suite = graph_test_suite.create_suite_edge_prop()
gl_suite = graph_test_suite.create_suite_global_prop()

suite = {**basic_suite, **vp_suite, **ep_suite, **gl_suite}

nx_suite = graph_test_suite.create_netx_suite()

@pytest.mark.slow
@pytest.mark.parametrize("test_name", [k for k in nx_suite.keys()])
def test_nx_suite_netx(test_name):
    """
    Run the netx tests from the graph test suite. Converts graph into networkx
    and back into tinygraph, then checks for graph equality (using tg.util).
    """
    for g in nx_suite[test_name]:
        # Convert to networkx and back

        # Get name if applicable
        name_arg = 'name' if 'name' in g.v.keys() else None
        ng = tg.io.to_nx(g, weight_prop='weight', name_prop=name_arg)

        # Extract data types (may be suboptimal but works..)
        vp_types = dict(map(lambda k: (k, g.v[k].dtype), g.v))
        ep_types = dict(map(lambda k: (k, g.e[k].dtype), g.e.keys()))
        g2 = tg.io.from_nx(ng,
                           adj_type=g.adjacency.dtype,
                           weight_prop='weight', name_prop=name_arg,
                           vp_types=vp_types,
                           ep_types=ep_types)

        assert tg.util.graph_equality(g, g2)

@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_nx_suite(test_name):
    """
    Run the basic tests from the graph test suite. Converts graph into networkx
    and back into tinygraph, then checks for graph equality (using tg.util).
    """
    for g in suite[test_name]:
        # Convert to networkx and back

        # Get name if applicable
        name_arg = 'name' if 'name' in g.v.keys() else None
        ng = tg.io.to_nx(g, weight_prop='weight', name_prop=name_arg)

        # Extract data types (may be suboptimal but works..)
        vp_types = dict(map(lambda k: (k, g.v[k].dtype), g.v))
        ep_types = dict(map(lambda k: (k, g.e[k].dtype), g.e.keys()))
        g2 = tg.io.from_nx(ng,
                           adj_type=g.adjacency.dtype,
                           weight_prop='weight', name_prop=name_arg,
                           vp_types=vp_types,
                           ep_types=ep_types)

        assert tg.util.graph_equality(g, g2)

# Custom tests
def basic_from_nx(raise_error_on_missing_prop):
    """Basic test for main functionality"""
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


    t = tg.io.from_nx(ng,
                      adj_type=np.float,
                      weight_prop='weight',
                      name_prop='name',
                      vp_types={'element': np.object, 'atomic number': np.int},
                      ep_types={'bond': np.bool},
                      raise_error_on_missing_prop=raise_error_on_missing_prop
    )
    ng2 = tg.io.to_nx(t, weight_prop='weight', name_prop='name')
    return ng, t, ng2

def test_basic_from_nx():
    """Should succeed to convert a graph back and forth"""
    ng, t, ng2 = basic_from_nx(raise_error_on_missing_prop=False)

    # Assertion statements...
    assert ng.order() == ng2.order()
    assert ng.size()  == ng2.size()
    assert ng.nodes.keys() == ng2.nodes.keys()

    # Check vertex properties up to 'name'
    # But new entries can be produced
    for v in ng.nodes:
        props = ng.nodes[v].keys()
        for prop in props:
            if prop in ng2.nodes[v].keys():
                assert ng.nodes[v][prop] == ng2.nodes[v][prop]
            else:
                assert prop == 'name'

    # Edge properties up to 'weight'
    for e in ng.edges:
        assert e in ng2.edges()

        for prop in props:
            if prop in ng2.edges[e].keys():
                assert ng.edges[e][prop] == ng2.edges[e][prop]
            else:
                assert prop == 'weight'


def test_triangle():
    """Makes a cycle graph and checks for perservation of the adjacency matrix"""
    t = tg.TinyGraph(3, vp_types={'name': np.str})
    t[0, 1] = 1
    t[1, 2] = 1.1
    t[2, 0] = 3

    t.v['name'][0] = 'a'
    t.v['name'][1] = 'b'
    t.v['name'][2] = 'c'

    ng = tg.io.to_nx(t, weight_prop = 'weight')
    t2 = tg.io.from_nx(ng, weight_prop='weight', vp_types={'name': np.str})

    assert tg.util.graph_equality(t, t2)


def test_nx_modification():
    """Ensure modifications behave the same way"""
    t = tg.TinyGraph(3)

    # Add a new vertex and edge to ng
    ng = tg.io.to_nx(t, weight_prop = 'weight', name_prop=None)
    ng.add_node(3, name=3)
    ng.add_edge(2, 3, weight=5)

    # Add the same vertex and edge in t
    t.add_vertex(weight=5)
    t[2, 3] = 5
    t[3, 2] = 5

    t2 = tg.io.from_nx(ng, weight_prop='weight', name_prop=None)
    assert np.all(t.adjacency == t2.adjacency)
    assert tg.util.graph_equality(t, t2)

# Beware! Test cases that highlight potentially counter-intuitive behavior!
def test_vanishing_edge():
    """Current behavior is for 0-weighted edges to vanish"""
    t = tg.TinyGraph(2)
    t[0, 1] = 0
    ng = tg.io.to_nx(t)
    t2 = tg.io.from_nx(ng)

    assert np.all(t2.adjacency == 0)

def test_default_values():
    """
    Test/demonstrate the default value behavior when errors are not raised.
    """
    g = networkx.Graph()
    g.add_node('a', color=0)
    g.add_node('b')
    g.add_node('c')

    g.add_edge('a', 'b', weight=3)
    g.add_edge('b', 'c')

    t = tg.io.from_nx(g,
                      weight_prop='weight',
                      name_prop='name',
                      vp_types={'color': np.int}, ep_types={'weight': np.int},
                      raise_error_on_missing_prop=False)

    g2 = tg.io.to_nx(t,
                     weight_prop='weight',
                     name_prop='name')

    # The vertices and edges are unchanged
    assert list(g.nodes.keys()) == list(g2.nodes.keys())
    assert list(g.edges.keys()) == list(g2.edges.keys())

    # But default values have been filled in
    assert g.nodes.data() != g2.nodes.data()
    assert 'color' not in g.nodes['b'].keys()
    assert 'color' in     g2.nodes['b'].keys()
    assert g2.edges['b', 'c']['weight'] == 1

def neighbors_graph():
    """Basic graph for reuse among tests"""
    g = tg.TinyGraph(4,
                     vp_types={'name': np.dtype("<U10"), 'pet': np.dtype("<U10")},
                     ep_types={'neighbors': np.bool, 'friends': np.bool})
    g.v['name'][:] = ['Hank', 'Frank', 'Tank', 'Yank']
    g.v['pet'][:] = ['Socks', 'Spot', 'Coffee', 'Cat']

    g[0, 1] = 1
    g.e['neighbors'][0, 1] = True
    g.e['friends'][0, 1] = True

    g[0, 2] = 1
    g.e['neighbors'][0, 2] = False
    g.e['friends'][0, 2] = False
    return g

def test_subset_to_nx():
    """Verify the desired properties are transfered to the networkx graph"""
    g = neighbors_graph()
    ng = tg.io.to_nx(g,
                     weight_prop='custom_weight',
                     name_prop='name',
                     vp_subset=['pet'],
                     ep_subset=['friends'])

    # Name is not included as a vertex attribute
    assert list(ng.nodes['Hank'].keys()) == ['pet']

    # The only edge attributes are 'friends' and 'weight'
    assert 2 == len(ng.edges['Hank', 'Frank'].keys())
    assert 'custom_weight' in ng.edges['Hank', 'Frank'].keys()
    assert 'friends' in ng.edges['Hank', 'Frank'].keys()

def test_subset_to_nx_default_behavior():
    """Verify the desired properties are transfered to the networkx graph
    when we use the default options (None for vp_subset, ep_subset)
    """
    g = neighbors_graph()
    ng = tg.io.to_nx(g,
                     weight_prop='wait',
                     name_prop='name',
                     vp_subset=None,
                     ep_subset=None)

    # 'name' field is removed automatically
    assert list(ng.nodes['Hank'].keys()) == ['pet']

    # grabs everything and adds a 'weight' property
    assert 3 == len(ng.edges['Hank', 'Frank'].keys())
    assert 'wait' in ng.edges['Hank', 'Frank'].keys()
    assert 'friends' in ng.edges['Hank', 'Frank'].keys()
    assert 'neighbors' in ng.edges['Hank', 'Frank'].keys()

def test_subset_to_nx_default_behavior_plain():
    """Verify the desired properties are transfered to the networkx graph
    when we use the default options (None for vp_subset, ep_subset)
    and we remove the weight and name nodes
    """
    g = neighbors_graph()
    ng = tg.io.to_nx(g,
                     weight_prop=None,
                     name_prop=None,
                     vp_subset=None,
                     ep_subset=None)

    # 'name' field is not removed this time
    assert 2 == len(ng.nodes[0].keys())
    assert 'pet' in ng.nodes[0].keys()
    assert 'name' in ng.nodes[0].keys()

    # 'weight' field is not generated
    assert 2 == len(ng.edges[0, 1].keys())
    assert 'friends' in ng.edges[0, 1].keys()
    assert 'neighbors' in ng.edges[0, 1].keys()


# Make sure errors are raised properly
def test_fail_from_nx():
    """Complains for a conversion missing a property on a node"""
    with pytest.raises(KeyError):
        ng, t, ng2 = basic_from_nx(raise_error_on_missing_prop=True)

def test_self_loop():
    """Self-edges always raise ValueErrors"""
    ng = networkx.Graph()
    ng.add_node(0)
    ng.add_edge(0, 0, weight=1) # self edge
    with pytest.raises(ValueError):
        t = tg.io.from_nx(ng, weight_prop='weight')

def test_bad_vertex_subset():
    """Ensure a KeyError is raised on an invalid subset request"""
    t = tg.TinyGraph(3, ep_types={'weight': np.int})
    t[0, 1] = 2
    t[1, 2] = 4

    with pytest.raises(KeyError):
        ng = tg.io.to_nx(t, vp_subset=['color'])

def test_bad_edge_subset():
    g = tg.TinyGraph(2, vp_types={'color': np.int})
    with pytest.raises(KeyError):
        ng = tg.io.to_nx(g,
                         weight_prop='weight',
                         name_prop='name',
                         vp_subset=['color'],
                         ep_subset=['friends']) # no friends :/

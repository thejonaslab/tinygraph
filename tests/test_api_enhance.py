import tinygraph as tg
from tinygraph.util import graph_equality, subgraph_relabel, permute, subgraph
import numpy as np
import pytest
import graph_test_suite

basic_suite = graph_test_suite.create_suite()
vp_suite = graph_test_suite.create_suite_vert_prop()
ep_suite = graph_test_suite.create_suite_edge_prop()
prop_suite = graph_test_suite.create_suite_global_prop()

suite = {**basic_suite, **vp_suite, **ep_suite, **prop_suite}


def test_vertices():
    """
    Simple test of getting vertex properties.
    """
    g = tg.TinyGraph(5, np.int32, vp_types = {'color': np.int32,
                                                'elem': np.bool})
    g.v['color'][0] = 3
    g.v['color'][1] = 4
    g.v['color'][2] = 5
    g.v['color'][3] = 6
    g.v['color'][4] = 1
    g.v['elem'][0] = True
    g.v['elem'][1] = False
    g.v['elem'][2] = True
    g.v['elem'][3] = False
    g.v['elem'][4] = True
    color = [3,4,5,6,1]
    elem = [True, False, True, False, True]
    assert len(g.vertices(vert_props={})[0]) == 2
    for i, d in g.vertices(vert_props = ['color', 'elem']):
        assert d['color'] == color[i]
        assert d['elem'] == elem[i]

def test_edges():
    """
    Simple test of getting edge properties.
    """
    g = tg.TinyGraph(5, np.int32, ep_types = {'color': np.int32,
                                                'elem': np.bool})
    g[0,4] = 10
    g[1,0] = 20
    g[2,1] = 30
    g[3,2] = 40
    g[4,3] = 50
    g.e['color'][0,1] = 3
    g.e['color'][1,2] = 4
    g.e['color'][2,3] = 5
    g.e['color'][3,4] = 6
    g.e['color'][4,0] = 1
    g.e['elem'][4,0] = True
    g.e['elem'][0,1] = False
    g.e['elem'][1,2] = True
    g.e['elem'][2,3] = False
    g.e['elem'][3,4] = True
    weights = {(0,4):10,(0,1):20,(1,2):30,(2,3):40,(3,4):50}
    elem = {(0,4):True,(0,1):False,(1,2):True,(2,3):False,(3,4):True}
    assert len(g.edges(edge_props={})[0]) == 3
    for i, j, w in g.edges(weight = True):
        assert w == weights[(i,j)]
    for i, j, d in g.edges(edge_props = ['elem']):
        assert len(d) == 1
        assert d['elem'] == elem[(i,j)]

def test_remove_edge():
    """
    Simple test of removing edges.
    """
    g = tg.TinyGraph(5, np.int32, ep_types = {'color': np.int32,
                                                'elem': np.bool})
    g[0,4] = 10
    g[1,0] = 20
    g[2,1] = 30
    g[3,2] = 40
    g[4,3] = 50
    g.e['color'][0,1] = 3
    g.e['color'][1,2] = 4
    g.e['color'][2,3] = 5
    g.e['color'][3,4] = 6
    g.e['color'][4,0] = 1
    g[0,4] = 0
    g[1,0] = 0
    with pytest.raises(IndexError, match='No such edge'):
        g.e['color'][1,4] = 6
    with pytest.raises(IndexError, match='No such edge.'):
        g.e['color'][0,1]
    assert g.e['color'][1,2] == 4
    assert g.e['color'][2,3] == 5
    assert g.e['color'][3,4] == 6
    with pytest.raises(IndexError, match='No such edge.'):
        g.e['color'][4,0]

def test_permute():
    """
    Test permuting a graph to be equal to another, or permuting back and forth
    to stay equal to itself.
    """
    g1 = tg.TinyGraph(5, np.int32,
                      vp_types = {'color' : np.int32},
                      ep_types = {'color2' : np.int32})
    g2 = tg.TinyGraph(5, np.int32,
                      vp_types = {'color' : np.int32},
                      ep_types = {'color2' : np.int32})
    g1[0,1] = 5
    g2[3,4] = 5
    g1[2,3] = 1
    g2[1,2] = 1
    g1.v['color'][0] = 10
    g2.v['color'][4] = 10
    g1.e['color2'][2,3] = 4
    g2.e['color2'][2,1] = 4

    pG11 = permute(g1,   [3,4,1,2,0])
    pG12 = permute(g1,   [4,3,1,2,0])
    pG13 = permute(pG11, [4,2,3,0,1])

    assert not graph_equality(g2, pG11)
    assert graph_equality(g2, pG12)
    assert graph_equality(g1, pG13)

def test_permute_path():
    """Another case"""
    g = tg.TinyGraph(4, np.bool, vp_types={'name': np.dtype('<U20')})
    perm = [2, 3, 1, 0]
    inv_perm = np.argsort(perm) # [3, 2, 0, 1]
    g.v['name'][:] = ['a', 'b', 'c', 'd']
    g[0, 1] = 1
    g[1, 2] = 1
    g[2, 3] = 1

    # import pdb; pdb.set_trace()
    h  = permute(g, perm)
    gp = permute(h, inv_perm)
    assert graph_equality(g, gp)

def test_permute_identity():
    """Ensure that the identity permutation preserves graph equality"""
    g1 = tg.TinyGraph(5, np.int32,
                      vp_types = {'color' : np.int32},
                      ep_types = {'color2' : np.int32})
    g1[0, 1] = 5
    g1[1, 3] = 3
    g1[2, 3] = 1
    g1[0, 4] = 2
    g1.v['color'][0] = 10
    g1.e['color2'][2,3] = 4

    g2 = permute(g1, [0, 1, 2, 3, 4])

    assert graph_equality(g1, g2)

def test_permute_error_handling():
    """Demonstrate behavior in case not handed a proper permutation"""
    g1 = tg.TinyGraph(5, np.int32,
                      vp_types = {'color' : np.int32},
                      ep_types = {'color2' : np.int32})
    g1[0, 1] = 5
    g1[1, 3] = 3
    g1[2, 3] = 1
    g1[0, 4] = 2
    g1.v['color'][0] = 10
    g1.e['color2'][2,3] = 4


    bad_perm_1 = [0]
    bad_perm_2 = [1, 3, 3, 4, 4]
    bad_perm_3 = [1, 3, 3, 4, 4, 2, 2, 1]
    bad_perm_4 = [-5, 0, 3, 3, 4, 6]


    # Is this behavior we want?
    with pytest.raises(IndexError):
        bg1 = permute(g1, bad_perm_1)

    with pytest.raises(IndexError):
        bg2 = permute(g1, bad_perm_2)

    with pytest.raises(IndexError):
        bg3 = permute(g1, bad_perm_3)

    with pytest.raises(IndexError):
        bg4 = permute(g1, bad_perm_4)

def test_permute_dict():
    """Pass the permutation as a dictionary"""
    perm = [2, 3, 1, 0]
    # perm_dict = dict(zip(range(4), perm))
    # purposely written out of order
    perm_dict = {3:0, 0:2, 2:1, 1:3}
    g = tg.TinyGraph(4, np.bool,
                     vp_types = {'name' : np.dtype('<U20')})
    g.v['name'][:] = ['a', 'b', 'c', 'd']

    h = permute(g, perm_dict)

    assert list(h.v['name']) == ['d', 'c', 'a', 'b']

def test_subgraph_complete():
    """Limiting case of a full graph"""
    g = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    sg = subgraph(g, range(5))

    assert graph_equality(g, sg)

def test_subgraph_empty():
    """Limiting case of an empty graph"""
    g = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    sg = subgraph(g, [])

    assert sg.node_N == 0
    assert not graph_equality(g, sg)

def test_subgraph_list():
    """Check functionality for a list of nodes"""
    rng = np.random.RandomState(0)
    nodes = rng.choice(5, 3, replace=False)

    g = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    g.add_vert_prop('name', np.dtype('<U20'))
    g.v['name'][:] = ['a', 'b', 'c', 'd', 'e']

    sg = subgraph(g, nodes)

    assert sg.node_N == 3
    assert np.array_equal(sg.v['name'], np.array(g.v['name'])[nodes])

    for n1, n2 in sg.edges():
        assert sg[n1, n2] == g[nodes[n1], nodes[n2]]

def test_subgraph_set():
    """Check functionality for a set of nodes (as in vertex subset)"""
    rng = np.random.RandomState(0)
    nodes = set(rng.choice(5, 3, replace=False))

    g = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    g.add_vert_prop('name', np.dtype('<U20'))
    g.v['name'][:] = ['a', 'b', 'c', 'd', 'e']

    sg = subgraph(g, nodes)

    node_list = sorted(list(nodes))
    assert np.array_equal(sg.v['name'], np.array(g.v['name'])[node_list])

@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_permutation_inversion(test_name):
    """Use the graph suite to permute and un-permute a graph"""
    rng = np.random.RandomState(0)

    for g in suite[test_name]:
        # Get order and a random permutation
        N = g.node_N
        perm     = rng.permutation(N)
        inv_perm = np.argsort(perm)

        # Permute the permutation
        # m e t a
        order = rng.permutation(N)
        inv_perm_dict = dict(zip(np.arange(N)[order], inv_perm[order]))

        # Use the list version
        h = permute(g, perm)
        g2 = permute(h, inv_perm)
        assert graph_equality(g, g2)

        # Use the dict version
        g3 = permute(h, inv_perm_dict)
        assert graph_equality(g, g3)

@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_subgraph(test_name):
    """Use the test suite to grab subgraphs (using sets)"""
    rng = np.random.RandomState(0)

    for g in suite[test_name]:
        # Get order and a random permutation
        N = g.node_N
        SN = rng.randint(N)
        node_list = sorted(rng.choice(N, SN, replace=False))
        nodes = set(node_list)

        h = subgraph(g, nodes)

        # Check global properties
        assert h.props == g.props

        # Check vertex properties
        for n in h.vertices():
            for k in g.v.keys():
                assert h.v[k][n] == g.v[k][node_list[n]]

        # Check edge properties and weights
        for n1, n2 in h.edges():
            assert h[n1, n2] == g[node_list[n1], node_list[n2]]
            for k in g.e.keys():
                assert h.e[k][n1, n2] == g.e[k][node_list[n1], node_list[n2]]

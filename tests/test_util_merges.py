import tinygraph as tg
from tinygraph.util import graph_equality, merge
import numpy as np
import pytest
import graph_test_suite

basic_suite = graph_test_suite.create_suite()
vp_suite = graph_test_suite.create_suite_vert_prop()
ep_suite = graph_test_suite.create_suite_edge_prop()
prop_suite = graph_test_suite.create_suite_global_prop()

suite = {**basic_suite, **vp_suite, **ep_suite, **prop_suite}

def test_merge_simple():
    """Merge two graphs, each with two vertices and no properties"""
    g1 = tg.TinyGraph(2)
    g1[0, 1] = 2
    g2 = tg.TinyGraph(2)
    g2[0, 1] = 3

    gg = merge(g1, g2)

    result = np.zeros((4, 4), dtype=np.int32)
    result[0, 1] = 2
    result[1, 0] = 2
    result[2, 3] = 3
    result[3, 2] = 3

    assert gg.node_N == 4
    assert np.array_equal(gg.adjacency, result)

def test_merge_empty():
    """Merge two empty graphs"""
    g1 = tg.TinyGraph(0, np.bool)
    g2 = tg.TinyGraph(0, np.bool)

    gg  = merge(g1, g2)
    gg2 = merge(g2, g1)

    assert 0 == gg.node_N
    assert 0 == gg2.node_N

def test_merge_identity():
    """Merge with an empty graph"""
    g1 = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    g2 = tg.TinyGraph(0, np.bool)

    gg = merge(g1, g2)
    gh = merge(g2, g1)

    assert graph_equality(g1, gg)
    assert graph_equality(g1, gh)

def test_prop_types():
    g1 = tg.TinyGraph(2, np.int32, vp_types={'name':np.dtype('<U10')}, ep_types={'length':np.double})
    g1.v['name'][:] = ['aaa', 'baa']
    g1.props['name'] = 'base'
    g1[0, 1] = 1
    g1.e['length'][0, 1] = 2.2

    g2 = tg.TinyGraph(2, np.double, vp_types={}, ep_types={'length':np.double})
    with pytest.raises(TypeError):
        merge(g1, g2)

    g3 = tg.TinyGraph(2, np.int32, vp_types={}, ep_types={'length':np.int})
    g3.props['name'] = 'secondary'
    g3[0, 1] = 2
    g3.e['length'][0, 1] = 4
    with pytest.raises(TypeError):
        merge(g1, g3)

    g4 = tg.TinyGraph(2, np.int32, vp_types={}, ep_types={'length':np.double})
    g4.props['name'] = 'secondary'
    g4[0, 1] = 2
    g4.e['length'][0, 1] = 4.0
    with pytest.warns(UserWarning):
        gg = merge(g1, g4)
        assert np.array_equal(gg.v['name'], ['aaa', 'baa', '', ''])

    g5 = tg.TinyGraph(2, np.int32, vp_types={'name':np.dtype('<U10')}, ep_types={'length':np.double})
    g5.props['name'] = 'secondary'
    g5.v['name'][:] = ['hello', 'world']
    g5[0, 1] = 2
    g5.e['length'][0, 1] = 4.0

    gh = merge(g1, g5)
    assert gh.props['name'] == 'base'
    assert np.array_equal(gh.v['name'], ['aaa', 'baa', 'hello', 'world'])
    assert gh.e['length'][0, 1] == g1.e['length'][0, 1]
    assert gh.e['length'][2, 3] == g5.e['length'][0, 1]

@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_subgraph(test_name):
    """Use the test suite to grab subgraphs (using sets)"""
    for i in range(len(suite[test_name])-1):
        g1 = suite[test_name][i]
        g2 = suite[test_name][i+1]

        gg = merge(g1, g2)

        # Preliminary
        assert gg.node_N == g1.node_N + g2.node_N

        # Just check for transfer of global property names
        for key in g1.props.keys():
            assert key in gg.props.keys()
        for key in g2.props.keys():
            assert key in gg.props.keys()

        # Check vertex properties in bulk
        for key in g1.v.keys():
            assert key in gg.v.keys()
            assert np.array_equal(gg.v[key][:g1.node_N], g1.v[key])
        for key in g2.v.keys():
            assert key in gg.v.keys()
            assert np.array_equal(gg.v[key][g1.node_N:], g2.v[key])

        # Check edges through the EdgeProxy instead of e_p like in the function
        for key in g1.e.keys():
            assert key in gg.e.keys()
            for n1, n2 in g1.edges():
                assert g1.e[key][n1, n2] == gg.e[key][n1, n2]

        for key in g2.e.keys():
            assert key in gg.e.keys()
            for n1, n2 in g2.edges():
                assert g2.e[key][n1, n2] == gg.e[key][g.node_N+n1, g.node_N+n2]

        # Adjacency
        assert np.array_equal(g1.adjacency, gg.adjacency[:g1.node_N, :g1.node_N])
        assert np.array_equal(g2.adjacency, gg.adjacency[g1.node_N:, g1.node_N:])

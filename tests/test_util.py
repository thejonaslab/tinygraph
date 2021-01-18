import tinygraph as tg
from tinygraph.util import graph_equality, permute, subgraph, merge
import numpy as np
import pytest
import graph_test_suite

basic_suite = graph_test_suite.create_suite()
vp_suite = graph_test_suite.create_suite_vert_prop()
ep_suite = graph_test_suite.create_suite_edge_prop()
prop_suite = graph_test_suite.create_suite_global_prop()

suite = {**basic_suite, **vp_suite, **ep_suite, **prop_suite}

### Permute ###

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
    """Another case to ensure permutations work in the expected direction"""
    g = tg.TinyGraph(4, np.bool, vp_types={'name': np.dtype('<U20')})
    perm = [2, 3, 1, 0]
    inv_perm = np.argsort(perm) # [3, 2, 0, 1]
    assert np.array_equal(inv_perm, [3, 2, 0 ,1])
    g.v['name'][:] = ['a', 'b', 'c', 'd']
    g[0, 1] = 1
    g[1, 2] = 1
    g[2, 3] = 1

    h  = permute(g, perm)
    assert list(h.v['name']) == ['d', 'c', 'a', 'b']
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
    """Pass the permutation as a dictionary and ensure the permutation
    operates in the desired direction"""
    perm = [2, 3, 1, 0]
    # perm_dict = dict(zip(range(4), perm))
    # purposely written out of order
    perm_dict = {3:0, 0:2, 2:1, 1:3}
    g = tg.TinyGraph(4, np.bool,
                     vp_types = {'name' : np.dtype('<U20')})
    g.v['name'][:] = ['a', 'b', 'c', 'd']

    h = permute(g, perm_dict)

    assert list(h.v['name']) == ['d', 'c', 'a', 'b']

@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_permutation_inversion_suite(test_name):
    """Use the graph suite to permute and un-permute a graph"""
    rng = np.random.RandomState(0)

    for g in suite[test_name]:
        # Get order and a random permutation
        N = g.vert_N
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

#### Subgraph test cases ###

def test_subgraph_complete():
    """Limiting case of a full graph"""
    g = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    sg = subgraph(g, range(5))

    assert graph_equality(g, sg)

def test_subgraph_empty():
    """Limiting case of an empty graph"""
    g = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    sg = subgraph(g, [])

    assert sg.vert_N == 0
    assert not graph_equality(g, sg)

def test_subgraph_list():
    """Check functionality for a list of vertices"""
    rng = np.random.RandomState(0)
    vertices = rng.choice(5, 3, replace=False)

    g = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    g.add_vert_prop('name', np.dtype('<U20'))
    g.v['name'][:] = ['a', 'b', 'c', 'd', 'e']

    sg = subgraph(g, vertices)

    assert sg.vert_N == 3
    assert np.array_equal(sg.v['name'], np.array(g.v['name'])[vertices])

    for n1, n2 in sg.edges():
        assert sg[n1, n2] == g[vertices[n1], vertices[n2]]

def test_subgraph_set():
    """Check functionality for a set of vertices (as in vertex subset)"""
    rng = np.random.RandomState(0)
    vertices = set(rng.choice(5, 3, replace=False))

    g = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    g.add_vert_prop('name', np.dtype('<U20'))
    g.v['name'][:] = ['a', 'b', 'c', 'd', 'e']

    sg = subgraph(g, vertices)

    vert_list = sorted(list(vertices))
    assert np.array_equal(sg.v['name'], np.array(g.v['name'])[vert_list])

def test_subgraph_error():
    """Check error-handling for out-of-bounds stuff"""
    vertices = set([0, 1, 12])
    g = tg.TinyGraph(5)
    with pytest.raises(IndexError):
        sg = subgraph(g, vertices)

    vertices2 = set([-1, 0, 3, 4])
    with pytest.raises(IndexError):
        sg2 = subgraph(g, vertices2)

def test_subgraph_duplicate():
    """Check that we can duplicate vertices if we like"""
    vertices = [0, 0, 1]
    g = tg.TinyGraph(2, vp_types={'name':np.dtype('<U10')})
    g.v['name'][:] = ['a', 'b']
    g[0, 1] = 1

    sg = subgraph(g, vertices)

    adj = np.zeros((3, 3), dtype=np.int32)
    adj[0, 2] = 1
    adj[2, 0] = 1
    adj[1, 2] = 1
    adj[2, 1] = 1
    assert sg.vert_N == 3
    assert np.array_equal(adj, sg.adjacency)
    assert np.array_equal(['a', 'a', 'b'], sg.v['name'])


@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_subgraph_suite(test_name):
    """Use the test suite to grab subgraphs"""
    rng = np.random.RandomState(0)

    for g in suite[test_name]:
        # Get order and a random permutation
        N = g.vert_N
        SN = rng.randint(N)
        vert_list = rng.choice(N, SN, replace=False)
        vertices = sorted(vert_list)

        h = subgraph(g, vertices)

        # Check global properties
        assert h.props == g.props

        # Check vertex properties
        for n in h.vertices():
            for k in g.v.keys():
                assert h.v[k][n] == g.v[k][vertices[n]]

        # Check edge properties and weights
        for n1, n2 in h.edges():
            assert h[n1, n2] == g[vertices[n1], vertices[n2]]
            for k in g.e.keys():
                assert h.e[k][n1, n2] == g.e[k][vertices[n1], vertices[n2]]

        # Check behavior with vertices
        g.add_vert_prop('old_vertex_id', np.int)
        g.v['old_vertex_id'][:] = np.arange(g.vert_N)

        # Unclear what ordering will result from iterating over vertset
        # so just check that we can reconstruct the original
        vertset = set(vert_list)
        h_set = subgraph(g, vertset)

        # Attempt to reconstruct the subgraph `h` made with `vertices`.
        # Note that h_set.v['old_vertex_id'] has indices that lie outside
        # the normal range. So, we perform an argsort and a reverse argsort
        # which brings all the indices in range and preserves the order.
        order = np.argsort(h_set.v['old_vertex_id'])
        h_rec = permute(h_set, order)
        h_rec.remove_vert_prop('old_vertex_id')

        assert graph_equality(h, h_rec)


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

    assert gg.vert_N == 4
    assert np.array_equal(gg.adjacency, result)

def test_merge_empty():
    """Merge two empty graphs"""
    g1 = tg.TinyGraph(0, np.bool)
    g2 = tg.TinyGraph(0, np.bool)

    gg  = merge(g1, g2)
    gg2 = merge(g2, g1)

    assert 0 == gg.vert_N
    assert 0 == gg2.vert_N

def test_merge_identity():
    """Merge with an empty graph"""
    g1 = graph_test_suite.gen_random(5, np.bool, [True], 0.5)
    g2 = tg.TinyGraph(0, np.bool)

    gg = merge(g1, g2)
    gh = merge(g2, g1)

    assert graph_equality(g1, gg)
    assert graph_equality(g1, gh)

def test_merge_prop_types():
    """
    Check for desired behavior in case of mismatched property types
    (both for global types and vertex/edge proprty types)
    """
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
def test_merge_suite(test_name):
    """Use the test suite to grab merges"""
    for i in range(len(suite[test_name])-1):
        g1 = suite[test_name][i]
        g2 = suite[test_name][i+1]

        gg = merge(g1, g2)

        # Preliminary
        assert gg.vert_N == g1.vert_N + g2.vert_N

        # Just check for transfer of global property names
        for key in g1.props.keys():
            assert key in gg.props.keys()
        for key in g2.props.keys():
            assert key in gg.props.keys()

        # Check vertex properties in bulk
        for key in g1.v.keys():
            assert key in gg.v.keys()
            assert np.array_equal(gg.v[key][:g1.vert_N], g1.v[key])
        for key in g2.v.keys():
            assert key in gg.v.keys()
            assert np.array_equal(gg.v[key][g1.vert_N:], g2.v[key])

        # Check edges through the EdgeProxy instead of e_p like in the function
        for key in g1.e.keys():
            assert key in gg.e.keys()
            for n1, n2 in g1.edges():
                assert g1.e[key][n1, n2] == gg.e[key][n1, n2]

        for key in g2.e.keys():
            assert key in gg.e.keys()
            for n1, n2 in g2.edges():
                assert g2.e[key][n1, n2] == gg.e[key][g.vert_N+n1, g.vert_N+n2]

        # Adjacency
        assert np.array_equal(g1.adjacency, gg.adjacency[:g1.vert_N, :g1.vert_N])
        assert np.array_equal(g2.adjacency, gg.adjacency[g1.vert_N:, g1.vert_N:])

# Currently not-thorough testing just to speed validation of the basic library functionality

import numpy as np
import tinygraph as tg
from tinygraph.tinygraph import _extract_1d_dtype, _extract_2d_dtype
import graph_test_suite
import io
import pytest

suite = graph_test_suite.get_full_suite()

def test_create_graphs_types():
    """
    Simple tests to try creating graphs of various dtypes
    """

    g1_bool = tg.TinyGraph(5, np.bool)
    g1_bool[3, 2] = True
    assert g1_bool[2, 3] == True
    assert g1_bool[3, 2] == True

    g1_int32 = tg.TinyGraph(5, np.int32)
    g1_int32[3, 2] = 7
    assert g1_int32[3, 2] == 7
    assert g1_int32[2, 3] == 7


    g1_float64 = tg.TinyGraph(5, np.float64)
    g1_float64[3, 2] = 3.14
    assert g1_float64[3, 2] == 3.14
    assert g1_float64[2, 3] == 3.14

def test_graph_properties():
    """
    Testing graph properties
    """
    g1 = tg.TinyGraph(5, np.int32,
                      vp_types = {'color' : np.int32},
                      ep_types = {'color2' : np.int32})

    g1.v['color'][2] = 5
    g1.v['color'][3] = 8

    g1[2,3] = 1
    g1.e['color2'][2, 3] = 10

    assert g1.v['color'][2] == 5
    assert g1.v['color'][3] == 8
    assert g1.e['color2'][2, 3] == 10

def test_misbehavior():
    """
    Tests for illegal behavior handling
    """
    g = tg.TinyGraph(3,vp_types = {"color": np.int32},\
                        ep_types = {"width": np.int32})
    with pytest.raises(KeyError,match='Expecting exactly two endpoints.'):
        g[0] = 3
    with pytest.raises(KeyError, match='Expecting exactly two endpoints.'):
        g[0,1,2] = 3
    with pytest.raises(IndexError, match='Self-loops are not allowed.'):
        g[1,1] = 3
    with pytest.raises(KeyError,match='Expecting exactly two endpoints.'):
        e = g[0]
    with pytest.raises(KeyError, match='Expecting exactly two endpoints.'):
        e = g[0,1,2]
    with pytest.raises(KeyError,match='Expecting exactly two endpoints.'):
        g.e['width'][0] = 3
    with pytest.raises(KeyError, match='Expecting exactly two endpoints.'):
        g.e['width'][0,1,2] = 3
    with pytest.raises(KeyError,match='Expecting exactly two endpoints.'):
        e = g.e["width"][0]
    with pytest.raises(KeyError, match='Expecting exactly two endpoints.'):
        e = g.e['width'][0,1,2]
    with pytest.raises(IndexError):
        g.v['color'][0,2] = 1
    with pytest.raises(IndexError):
        v = g.v['color'][0,2]

def test_basic_functionality():
    t = tg.TinyGraph(2, vp_types={'color': np.int32})
    assert(t.vert_N == 2)

    t[1,0] = 1
    assert(t.edge_N == 1)

    t.add_vertex(props={'color': 3})
    t[1,2] = 1
    assert(t.vert_N == 3)
    assert(t.edge_N == 2)

    t.remove_vertex(0)
    assert(t.edge_N == 1)
    assert(t.vert_N == 2)
    assert(t.v['color'][1] == 3)
    assert(t.v['color'][0] == 0)

def test_items():
    t = tg.TinyGraph(3, vp_types={'name': np.str})

    t.v['name'][0] = 'a'
    t.v['name'][1] = 'b'
    t.v['name'][2] = 'c'

    assert(t.v['name'][0] == 'a')
    assert(t.v['name'][1] == 'b')
    assert(t.v['name'][2] == 'c')

def test_add_props():
    """
    Simple test of adding and removing properties
    """

    g = tg.TinyGraph(10, np.float32, ep_types={'color' : np.int32})

    g.add_vert_prop('color1', np.float32)

    assert 'color1' in g.v

    g.add_edge_prop('color2', np.float32)

    assert 'color2' in g.e

    assert len(g.e) == 2


    g.remove_edge_prop('color2')
    assert len(g.e) == 1

    g.remove_vert_prop('color1')
    assert len(g.v) == 0

def test_get_neighbors():
    """
    Simple test of getting the neighbors for various vertices.
    """
    g = tg.TinyGraph(6)
    g[0,1] = 1
    g[0,2] = 1
    g[1,2] = 1
    g[0,3] = 1
    g[0,5] = 1
    g[3,4] = 1
    g[4,5] = 1

    assert np.array_equal(g.get_neighbors(0), np.array([1,2,3,5]))
    assert np.array_equal(g.get_neighbors(1), np.array([0,2]))
    assert np.array_equal(g.get_neighbors(2), np.array([0,1]))
    assert np.array_equal(g.get_neighbors(3), np.array([0,4]))
    assert np.array_equal(g.get_neighbors(4), np.array([3,5]))
    assert np.array_equal(g.get_neighbors(5), np.array([0,4]))

def test_copy():
    """
    Copy the graph and ensure that changes are not propagated.
    """
    # Problem 1: setting an attribute before the edge exists seems to carry over?
    g = tg.TinyGraph(3,
                     adj_type=np.int,
                     vp_types={'name': np.dtype("<U10")},
                     ep_types={'edgename': np.dtype("<U20")})
    g.v['name'][0] = "Alice"
    g.v['name'][1] = "Bob"
    g.v['name'][2] = "Eve"

    g[0, 1] = 1
    g[1, 2] = 2
    g[2, 0] = 1

    g.e['edgename'][0, 1] = "main"
    g.e['edgename'][2, 0] = "intercept 1"
    g.e['edgename'][1, 2] = "intercept 2"

    # Deep copy
    h = g.copy()

    # Trimming h's edges doesn't affect g's adjacency matrix
    h[1, 2] = 0
    h[0, 2] = 0
    assert np.all(g.adjacency == [[0, 1, 1], [1, 0, 2], [1, 2, 0]])
    assert np.all(h.adjacency == [[0, 1, 0], [1, 0, 0], [0, 0, 0]])

    # Also change the vertex properties
    h.v['name'][0] = "Adam"
    h.v['name'][1] = "Barbara"
    h.v['name'][2] = "Ernie"
    assert np.all(g.v['name'] == ["Alice", "Bob", "Eve"])
    assert np.all(h.v['name'] == ["Adam", "Barbara", "Ernie"])

    # And edge properties
    h.e['edgename'][0, 1] = 'Maine!'
    assert np.all(h.e_p['edgename'] == [["", "Maine!", ""],
                                        ["Maine!", "", ""],
                                        ["", "", ""]])
    assert np.all(g.e_p['edgename'] == [["", "main", "intercept 1"],
                                        ["main", "", "intercept 2"],
                                        ["intercept 1", "intercept 2", ""]])

def test_graph_props():
    """
    Simple tests of per-graph properties

    """
    
    g1 = tg.TinyGraph(10)
    g1.props['foo'] = 'bar'

    g2 = tg.TinyGraph(10)
    g2.props['foo'] = 'bar'

    assert tg.util.graph_equality(g1, g2)

    g2.props['baz'] = 7
    
    assert not tg.util.graph_equality(g1, g2)

@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_copy_suite(test_name):
    """
    Test graph copy against suite
    """
    for g in suite[test_name]:
        g1 = g.copy()
        assert tg.util.graph_equality(g1, g)
        

def test_vert_prop_with_multiple_dims():
    """
    There are some issues with per-vert properties having structured types, 
    like copying doesn't work
    """
    N = 10
    M = 5
    g1 = tg.TinyGraph(10, vp_types = {'big' : '4float32'})

    g2 = g1.copy()
    
                      



def test_extract_low_dimension_dtypes():

    x = np.zeros(10, 'float32,float32')
    assert x.shape == (10,)

    # this is the undesired behavior
    x = np.zeros(10, '3float32')
    assert x.shape == (10,3)

    new_dt = _extract_1d_dtype(x)

    assert new_dt == np.dtype('3float32')

    x = np.zeros(10, dtype=('float32', (3, 2)))
    
    new_dt = _extract_1d_dtype(x)
    print('the new dt is', new_dt)
    assert new_dt == np.dtype(('float32', (3, 2)))


    # now 2d 
    x = np.zeros((10,15), 'float32,float32')
    assert x.shape == (10,15)
    
    # this is the undesired behavior
    x = np.zeros((10, 15), '3float32')
    assert x.shape == (10,15, 3)

    new_dt = _extract_2d_dtype(x)

    assert new_dt == np.dtype(('float32', (3,)))

    
    

# Currently not-thorough testing just to speed validation of the basic library functionality

import numpy as np
import tinygraph as tg


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

    g1.e['color2'][2, 3] = 10 

    assert g1.v['color'][2] == 5
    assert g1.v['color'][3] == 8
    assert g1.e['color2'][2, 3] == 10
        
    
def test_basic_functionality():
    t = tg.TinyGraph(2, vp_types={'color': np.int32})
    assert(t.node_N == 2)

    t.add_node(props={'color': 3})
    assert(t.node_N == 3)

    t.remove_node(0)
    assert(t.node_N == 2)
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



# def test_add_edge():
#     """
#     Add an edge 
#     """

#     g = tg.TinyGraph(10, np.float32, ep_types={'color' : np.int32})

#     g.add_edge(1, 2, 5.0)

#     assert g[1, 2] == 5.0
    
#     g.add_edge(3, 4, 2.0, color=10)

#     assert g[3, 4] == 2.0
#     assert g.e['color'][3, 4] == 10

    
#     assert g.get_edge_props(3,4)  == {'color' : 10}


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
    g = tg.TinyGraph(6)
    g[0,1] = 1
    g[0,2] = 1
    g[1,2] = 1
    g[0,3] = 1
    g[0,5] = 1
    g[3,4] = 1
    g[4,5] = 1

    assert g.get_neighbors(0) == [1,2,3,5]
    assert g.get_neighbors(1) == [0,2]
    assert g.get_neighbors(2) == [0,1]
    assert g.get_neighbors(3) == [0,4]
    assert g.get_neighbors(4) == [3,5]
    assert g.get_neighbors(5) == [0,4]
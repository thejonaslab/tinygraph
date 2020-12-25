# Currently not-thorough testing just to speed validation of the basic library functionality

import numpy as np
import tinygraph as tg

def basic_functionality():
    t = tg.TinyGraph(2, vert_props={'color': np.int32})
    # print("Original Adjacency Matrix")
    # print(t.adjacency)
    assert(t.node_N == 2)

    t.add_node({'color': 3})
    # print("After node insertion")
    # print(t.adjacency)
    assert(t.node_N == 3)

    t.remove_node(0)
    # print("After node removal")
    # print(t.adjacency)
    assert(t.node_N == 2)
    assert(t.v['color'][1] == 3)
    assert(t.v['color'][0] == -1)

def test_items():
    t = tg.TinyGraph(3, vert_props={'name': np.str})

    t.v['name'][0] = 'a'
    t.v['name'][1] = 'b'
    t.v['name'][2] = 'c'

    assert(t.v['name'][0] == 'a')
    assert(t.v['name'][1] == 'b')
    assert(t.v['name'][2] == 'c')

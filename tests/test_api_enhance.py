import tinygraph as tg
from tinygraph.util import graph_equality #, subgraph_relabel, permute, subgraph
import numpy as np
import pytest
import graph_test_suite

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

import tinygraph as tg 
from util import graph_equality
import numpy as np

def test_remove_edge():
    """
    Simple test of removing edges.
    """

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
    for i, j, w in g.edges(weight = True):
        assert w == weights[(i,j)]
    for i, j, d in g.edges(edge_props = ['elem']):
        assert len(d) == 1
        assert d['elem'] == elem[(i,j)] 

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

    pG11 = g1.permute([3,4,1,2,0])
    pG12 = g1.permute([4,3,1,2,0])
    pG13 = pG11.permute([4,2,3,0,1])

    assert not graph_equality(g2, pG11)
    assert graph_equality(g2, pG12)
    assert graph_equality(g1, pG13)
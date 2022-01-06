import tinygraph as tg
import tinygraph.algorithms as algs
from tinygraph.io import to_nx
import pytest
import graph_test_suite
import networkx as nx
import numpy as np

suite = graph_test_suite.get_full_suite()

def test_cc_empty():
    """
    Empty graph has no connected components.
    """
    g = tg.TinyGraph(0)

    assert algs.get_connected_components(g) == []
    assert algs.is_connected(g) == False

def test_cc_one_comp():
    """
    Test graph with one connected component.
    """
    g = tg.TinyGraph(5)
    g[0,1] = 1
    g[0,2] = 1
    g[2,3] = 1
    g[3,4] = 1

    assert algs.get_connected_components(g) == [set(range(5)),]
    assert algs.is_connected(g) == True

def test_cc_multi_comp():
    """
    Test graph with mulitple connected components.
    """
    g = tg.TinyGraph(6)
    g[0,1] = 1
    g[0,2] = 1
    g[1,2] = 1
    g[3,4] = 1
    g[4,5] = 1

    assert algs.get_connected_components(g) == [set(range(3)),set(range(3,6))]
    assert algs.is_connected(g) == False

# @pytest.mark.parametrize("test_name", [k for k in suite.keys()])
# def test_random(test_name):
#     """
#     Test randomly generated graphs against networkx algorithms.
#     """
#     for g in suite[test_name]:

#         tg_cc = algs.get_connected_components(g)
#         tg_sp = algs.get_shortest_paths(g,False)

#         nx_g = to_nx(g, weight_prop = "weight")
#         nx_cc = nx.connected_components(nx_g)
#         nx_sp = dict(nx.all_pairs_shortest_path_length(nx_g))
        
#         for cc in nx_cc:
#             assert cc in tg_cc

#         for i in range(g.vert_N):
#             for j in range(g.vert_N):
#                 if not j in nx_sp[i]:
#                     assert tg_sp[i][j] == np.inf
#                 else:
#                     assert tg_sp[i][j] == nx_sp[i][j]

def test_cycles_empty():
    """
    An empty graph has no vertices to be in cycles.
    """
    g = tg.TinyGraph(0)

    assert algs.get_min_cycles(g) == [] 

def test_cycles_medium():
    """
    Test some medium sized graphs with various sized cycles.
    """
    g1 = tg.TinyGraph(6)
    g1[0,1] = 1
    g1[0,2] = 1
    g1[1,2] = 1
    g1[0,3] = 1
    g1[0,5] = 1
    g1[3,4] = 1
    g1[4,5] = 1

    assert algs.get_min_cycles(g1) == [{0, 1, 2}, {0, 1, 2}, {0, 1, 2},\
                                        {0, 3, 4, 5},{0, 3, 4, 5},{0, 3, 4, 5}]

    g2 = tg.TinyGraph(9)
    g2[0,8] = 1
    g2[7,8] = 1
    g2[6,8] = 1
    g2[3,7] = 1
    g2[3,6] = 1
    g2[2,3] = 1
    g2[5,6] = 1
    g2[1,2] = 1
    g2[1,4] = 1
    g2[4,5] = 1

    assert algs.get_min_cycles(g2) == [set(), \
                                        {1, 2, 3, 4, 5, 6}, \
                                        {1, 2, 3, 4, 5, 6}, \
                                        {3, 7, 8, 6}, \
                                        {1, 2, 3, 4, 5, 6}, \
                                        {1, 2, 3, 4, 5, 6}, \
                                        {3, 7, 8, 6}, \
                                        {3, 7, 8, 6}, \
                                        {3, 7, 8, 6} ]

def test_paths_empty():
    """
    Test shortest paths on an empty graph.
    """
    g = tg.TinyGraph(0,adj_type=np.bool)

    with pytest.raises(TypeError, match='Graph weights are not numbers.'):
        algs.get_shortest_paths(g,True)

    np.testing.assert_equal(algs.get_shortest_paths(g,False),
                                np.zeros((0,0),dtype=np.float64))

def test_paths_fully_connected():
    """
    Test shortest paths on a fully connected graph.
    """
    print("Fully connected")
    g = tg.TinyGraph(5)
    g[0,1] = 1
    g[1,2] = 1
    g[2,3] = 1
    g[3,4] = 1
    g[4,0] = 1

    np.testing.assert_equal(algs.get_shortest_paths(g,True),\
                                        np.array([[0,1,2,2,1],\
                                                [1,0,1,2,2],\
                                                [2,1,0,1,2],\
                                                [2,2,1,0,1],\
                                                [1,2,2,1,0]],dtype=np.float64))

def test_paths_fully_connected_with_path():
    """
    Test shortest paths on a fully connected graph.
    """
    g = tg.TinyGraph(5)
    g[0,1] = 1
    g[1,2] = 1
    g[2,3] = 1
    g[3,4] = 1
    g[4,0] = 1

    dists, paths = algs.get_shortest_paths(g,True,True)

    np.testing.assert_equal(dists,\
                            np.array([[0,1,2,2,1],\
                                    [1,0,1,2,2],\
                                    [2,1,0,1,2],\
                                    [2,2,1,0,1],\
                                    [1,2,2,1,0]],dtype=np.float64))

    np.testing.assert_equal(paths,\
                            np.array([[0,1,1,4,4],\
                                    [0,1,2,2,0],\
                                    [1,1,2,3,3],\
                                    [4,2,2,3,4],\
                                    [0,0,3,3,4]],dtype=np.float64))

def test_paths_disjointed():
    """
    Test shortest paths on a graph with at least two components.
    """
    g = tg.TinyGraph(8)
    g[0,1] = 1
    g[0,2] = 1
    g[1,2] = 3
    g[2,3] = 1
    g[3,4] = 1
    g[5,6] = 4
    g[6,7] = 2
    g[7,5] = 1 

    dists, paths = algs.get_shortest_paths(g,True,True)

    np.testing.assert_equal(dists,\
                    np.array([[0,1,1,2,3,np.inf,np.inf,np.inf],\
                                [1,0,2,3,4,np.inf,np.inf,np.inf],\
                                [1,2,0,1,2,np.inf,np.inf,np.inf],\
                                [2,3,1,0,1,np.inf,np.inf,np.inf],\
                                [3,4,2,1,0,np.inf,np.inf,np.inf],\
                                [np.inf,np.inf,np.inf,np.inf,np.inf,0,3,1],\
                                [np.inf,np.inf,np.inf,np.inf,np.inf,3,0,2],\
                                [np.inf,np.inf,np.inf,np.inf,np.inf,1,2,0]]\
                                ,dtype=np.float64))

    np.testing.assert_equal(paths,\
                    np.array([[0,1,2,2,2,np.inf,np.inf,np.inf],\
                                [0,1,0,0,0,np.inf,np.inf,np.inf],\
                                [0,0,2,3,3,np.inf,np.inf,np.inf],\
                                [2,2,2,3,4,np.inf,np.inf,np.inf],\
                                [3,3,3,3,4,np.inf,np.inf,np.inf],\
                                [np.inf,np.inf,np.inf,np.inf,np.inf,5,7,7],\
                                [np.inf,np.inf,np.inf,np.inf,np.inf,7,6,7],\
                                [np.inf,np.inf,np.inf,np.inf,np.inf,5,6,7]]\
                                ,dtype=np.float64))

def test_negative_cycles():
    """
    Test shortest path on a graph with a negative cycle (expect raise error).
    """
    g = tg.TinyGraph(3)
    g[0,1] = 1
    g[1,2] = -5
    g[2,0] = 1

    with pytest.raises(Exception, match='Graph has a negative cycle.'):
        algs.get_shortest_paths(g,True)
    assert np.array_equal(algs.get_shortest_paths(g,False),np.array([[0,1,1],
                                                [1,0,1],
                                                [1,1,0]],dtype=np.float64))
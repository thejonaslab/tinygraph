import tinygraph as tg
import tinygraph.algorithms as algs
from tinygraph.io import tg_to_nx
import pytest
import graph_test_suite
import networkx as nx

def test_cc_empty():
    """
    Empty graph has no connected components.
    """
    g1 = tg.TinyGraph(0)

    assert algs.get_connected_components(g1) == []

def test_cc_one_comp():
    """
    Test graph with one connected component.
    """
    g2 = tg.TinyGraph(5)
    g2[0,1] = 1
    g2[0,2] = 1
    g2[2,3] = 1
    g2[3,4] = 1

    assert algs.get_connected_components(g2) == [set(range(5)),]

def test_cc_multi_comp():
    """
    Test graph with mulitple connected components.
    """
    g3 = tg.TinyGraph(6)
    g3[0,1] = 1
    g3[0,2] = 1
    g3[1,2] = 1
    g3[3,4] = 1
    g3[4,5] = 1

    assert algs.get_connected_components(g3) == [set(range(3)),set(range(3,6))]

basic_suite = graph_test_suite.create_suite()
vp_suite = graph_test_suite.create_suite_vert_prop()
ep_suite = graph_test_suite.create_suite_edge_prop()

suite = {**basic_suite, **vp_suite, **ep_suite}


@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_random_cc(test_name):
    """
    Test randomly generated graphs against networkx cc.
    """
    for g in suite[test_name]:

        tg_cc = algs.get_connected_components(g)

        netx = tg_to_nx(g, weight_prop = "weight")
        nx_cc = nx.connected_components(netx)
        
        for cc in nx_cc:
            assert cc in tg_cc

def test_cycles_empty():
    """
    An empty graph has no nodes to be in cycles.
    """
    g4 = tg.TinyGraph(0)

    assert algs.get_min_cycles(g4) == [] 

def test_cycles_medium():
    """
    Test some medium sized graphs with various sized cycles.
    """
    g5 = tg.TinyGraph(6)
    g5[0,1] = 1
    g5[0,2] = 1
    g5[1,2] = 1
    g5[0,3] = 1
    g5[0,5] = 1
    g5[3,4] = 1
    g5[4,5] = 1

    assert algs.get_min_cycles(g5) == [{0, 1, 2}, {0, 1, 2}, {0, 1, 2},\
                                        {0, 3, 4, 5},{0, 3, 4, 5},{0, 3, 4, 5}]

    g6 = tg.TinyGraph(9)
    g6[0,8] = 1
    g6[7,8] = 1
    g6[6,8] = 1
    g6[3,7] = 1
    g6[3,6] = 1
    g6[2,3] = 1
    g6[5,6] = 1
    g6[1,2] = 1
    g6[1,4] = 1
    g6[4,5] = 1

    assert algs.get_min_cycles(g6) == [set(), \
                                        {1, 2, 3, 4, 5, 6}, \
                                        {1, 2, 3, 4, 5, 6}, \
                                        {3, 7, 8, 6}, \
                                        {1, 2, 3, 4, 5, 6}, \
                                        {1, 2, 3, 4, 5, 6}, \
                                        {3, 7, 8, 6}, \
                                        {3, 7, 8, 6}, \
                                        {3, 7, 8, 6} ]

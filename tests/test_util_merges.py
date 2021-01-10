import tinygraph as tg
from tinygraph.util import graph_equality, merge
import numpy as np
import pytest
import graph_test_suite

# basic_suite = graph_test_suite.create_suite()
# vp_suite = graph_test_suite.create_suite_vert_prop()
# ep_suite = graph_test_suite.create_suite_edge_prop()
# prop_suite = graph_test_suite.create_suite_global_prop()

# suite = {**basic_suite, **vp_suite, **ep_suite, **prop_suite}


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

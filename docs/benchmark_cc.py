"""
Simple stand-alone test to benchmark cc
"""
import sys; sys.path.append("../tests")
import graph_test_suite
import time
import networkx as nx

import tinygraph as tg
import tinygraph.algorithms as algs
from tinygraph.io import tg_to_nx
import numpy as np
import pandas as pd

np.random.seed(0)

NODE_N = 128
res = []
for i in range(100):
    g = graph_test_suite.gen_random(NODE_N, np.int32, [1], 0.02)    
    t1 = time.time()
    tg_cc = algs.get_connected_components(g)
    t2 = time.time()
    
    netx = tg_to_nx(g, weight_prop = "weight")

    nx_cc = list(nx.connected_components(netx))
    assert len(list(nx_cc)) == len(tg_cc)
    for cc in nx_cc:
        assert cc in tg_cc
    res.append({"runtime_ms" : (t2-t1)*1000,
                "components" : len(tg_cc),
                "node_N" : g.node_N})

df = pd.DataFrame(res)
print("average number of nodes:", df.node_N.mean())
print("average number of components:",  df.components.mean())
print("average runtime:", df.runtime_ms.mean(), "ms")

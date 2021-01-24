"""
Simple stand-alone test to benchmark cc
"""
import sys; sys.path.append("../tests")
import graph_test_suite
import time
import networkx as nx

import tinygraph as tg
import tinygraph.algorithms as algs
from tinygraph.io import to_nx
import numpy as np
import pandas as pd

np.random.seed(0)

VERT_N = 128
res = []
for i in range(100):
    g = graph_test_suite.gen_random(VERT_N, np.int32, [1], 0.02)    
    t1 = time.time()
    tg_cc = algs.get_connected_components(g)
    t2 = time.time()
    
    nx_g = to_nx(g, weight_prop = "weight")

    nx_cc = list(nx.connected_components(nx_g))
    assert len(list(nx_cc)) == len(tg_cc)
    for cc in nx_cc:
        assert cc in tg_cc
    res.append({"runtime_ms" : (t2-t1)*1000,
                "components" : len(tg_cc),
                "vert_N" : g.vert_N})

df = pd.DataFrame(res)
print("average number of vertices:", df.vert_N.mean())
print("average number of components:",  df.components.mean())
print("average runtime:", df.runtime_ms.mean(), "ms")

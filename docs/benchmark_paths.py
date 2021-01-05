"""
Simple stand-alone test to benchmark shortest paths
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

NODE_N = 128
res = []
for i in range(100):
    g = graph_test_suite.gen_random(NODE_N, np.int32, [1], 0.02)    
    t1 = time.time()
    tg_sp = algs.get_shortest_paths(g)
    t2 = time.time()

    netx = to_nx(g, weight_prop = "weight")

    nx_sp = list(nx.all_pairs_shortest_path_length(netx))
    for i in range(NODE_N):
        for j in range(NODE_N):
            # pass
            assert tg_sp[i][j] == nx_sp[i][j]
    res.append({"runtime_ms" : (t2-t1)*1000,
                "node_N" : g.node_N})

df = pd.DataFrame(res)
print("average number of nodes:", df.node_N.mean())
print("average runtime:", df.runtime_ms.mean(), "ms")
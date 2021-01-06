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
    tg_sp = algs.get_shortest_paths(g,False)
    t2 = time.time()
    t_uw = t2 - t1
    t1 = time.time()
    tg_sp_w = algs.get_shortest_paths(g,True)
    t2 = time.time()
    t_w = t2 - t1

    netx = to_nx(g, weight_prop = "weight")

    nx_sp = dict(nx.all_pairs_shortest_path_length(netx))
    for i in range(NODE_N):
        for j in range(NODE_N):
            if not j in nx_sp[i]:
                assert tg_sp[i][j] is None
            else:
                assert tg_sp[i][j] == nx_sp[i][j]
    res.append({"runtime_uw_ms" : t_uw*1000,
                "node_N" : g.node_N,
                "runtime_w_ms" : t_w*1000})

df = pd.DataFrame(res)
print("average number of nodes:", df.node_N.mean())
print("average runtime unweighted:", df.runtime_uw_ms.mean(), "ms")
print("average runtime weighted:", df.runtime_w_ms.mean(), "ms")
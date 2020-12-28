"""
Test suite of example graphs. This only includes very basic
cases and pathological cases; for a richer repertoire
of graphs use networkx and the io.from_nx functions. 

"""
import numpy as np
import tinygraph as tg

def gen_empty(N, dtype):
    """

    Generate a random empty graph of the given dtype
    """

    return gen_random(N, dtype, [tg.default_one(dtype)], 0.0)

def gen_fully_connected(N, dtype):
    """
    generate a random fully-connected graph of the given dtype
    """
    return gen_random(N, dtype, [tg.default_one(dtype)], 1.0)


def gen_linear(N, dtype):
    """

    """

    e = gen_empty(N, dtype)
    for i in range(N-1):
        e[i, i+1] = tg.default_one(dtype)
    return e

def gen_random(N, dtype, edge_weights, prob_edge):
    """
    Generate a random graph of the given dtype with 
    a fixed edge probability. 0 = empty graph, 1.0 = full graph, 
    possible edge weight values from edge_weights

    """

    g = tg.TinyGraph(N, dtype)
    for i in range(N):
        for j in range(i+1, N):
            if np.random.rand() < prob_edge:
                g[i, j] = np.random.choice(edge_weights)
    return g



def create_suite(seed=0):
    """
    returns a dict of graphs for testing, 
    designed to be used in a pytest fixture
    """

    out_graphs = {}
    for N in [1, 2, 4, 8, 16, 32, 64, 128]:
        for dtype in [np.bool, np.int32, np.float32, np.complex64]:
            basename = f"{N}_{str(dtype)[3:]}"

            name = f"empty_{basename}"
            out_graphs[name] = [gen_empty(N, dtype)]
            
            name = f"fullyconnected_{basename}"
            out_graphs[name] = [gen_fully_connected(N, dtype)]
            
            name = f"linear_{basename}"
            out_graphs[name] = [gen_linear(N, dtype)]


    SAMPLE_N = 50
    for N in [4, 7, 16, 32, 100]:
        for prob_edge in [0.1, 0.5, 0.9]:
            dtype = np.bool
            edge_weights = [True]
            
            
            name = f"random_{prob_edge:.1f}_{str(dtype)[3:]}_{N}"
            out_graphs[name] = [gen_random(N, dtype, edge_weights, prob_edge) \
                                for _ in range(SAMPLE_N)]

            dtype = np.int32
            
            name = f"random_{prob_edge:.1f}_{str(dtype)[3:]}_{N}"
            out_graphs[name] = []
            for i in range(SAMPLE_N):
                edge_weights = np.random.randint(1, np.random.randint(2, max(N//2, 3)),
                                                 size=np.random.randint(1, N//2))
                
                out_graphs[name].append(gen_random(N, dtype, edge_weights, prob_edge))
    return out_graphs
        
            
            
            

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



def add_random_ep(g, dt, rng=None):
    """
    Add a random edge property of dtype dt to g and fill it with
    with random values
    """
    if rng is None:
        rng = np.random.RandomState()

    name = "prop" + str(rng.randint(1000000))
    g.add_vert_prop(name, dt)

    for i in range(g.vert_N):
        for j in range(i +1, g.vert_N):
            if g.adjacency[i, j] > 0:
                if dt == np.bool:
                    g.e[name][i, j] = rng.choice([False, True])
                    
                elif dt == np.int32:
                    g.e[name][i, j] = rng.randint(1, 100)
                    
                elif dt == np.float64:
                    g.e[name][i, j] = rng.rand()
                    
                    
def add_random_vp(g, dt, rng=None):
    """
    Add a random vert property of dtype dt to g and fill it with
    with random values
    """
    if rng is None:
        rng = np.random.RandomState()

    name = "prop" + str(rng.randint(1000000))
    g.add_vert_prop(name, dt)

    for i in range(g.vert_N):
        if dt == np.bool:
            g.v[name][i] = rng.choice([False, True])

        elif dt == np.int32:
            g.v[name][i] = rng.randint(1, 100)

        elif dt == np.float64:
            g.v[name][i] = rng.rand()


    
def create_suite(seed=0, rng=None):
    """
    returns a dict of graphs for testing, 
    designed to be used in a pytest fixture
    """

    if rng is None:
        rng = np.random.RandomState(seed)
    
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


    SAMPLE_N = 5
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
                edge_weights = rng.randint(1, rng.randint(2, max(N//2, 3)),
                                                 size=rng.randint(1, N//2))
                
                out_graphs[name].append(gen_random(N, dtype, edge_weights, prob_edge))

                
            dtype = np.float64
            name = f"random_{prob_edge:.1f}_{str(dtype)[3:]}_{N}"
            out_graphs[name] = []
            for i in range(SAMPLE_N):
                edge_weights = rng.rand(rng.randint(1, N//2)) + 0.5
                
                out_graphs[name].append(gen_random(N, dtype, edge_weights, prob_edge))

                
    return out_graphs
        
            
            
            
def create_suite_vert_prop(seed=0):
    
    rng = np.random.RandomState(seed)
    suite = create_suite(rng=rng)

    out_suite = {}

    for k, v in suite.items():
        for g in v:
            for i in range(rng.randint(1, 4)):
                add_random_vp(g, rng.choice([np.bool, np.int32, np.float64]))
        out_suite[f'vp_{k}'] = v
    return suite
            
def create_suite_edge_prop(seed=0):
    
    rng = np.random.RandomState(seed)
    suite = create_suite(rng=rng)

    out_suite = {}
    
    for k, v in suite.items():
        for g in v:
            for i in range(rng.randint(1, 4)):
                add_random_vp(g, rng.choice([np.bool, np.int32, np.float64]))
        out_suite[f'ep_{k}'] = v

    return suite
            

def create_suite_global_prop(seed=0):
    
    rng = np.random.RandomState(seed)
    suite = create_suite(rng=rng)

    out_suite = {}

    for k, v in suite.items():
        for g in v:
            possible_props = {'foo' : 1,
                              'bar' : 1.0,
                              'baz' : [1, 2, 3],
                              'quxx' : {'foo' : 100},
                              'quxxx' : None}
            number = np.random.randint(1, len(possible_props)+1)
            for i in range(number):
                k = rng.choice(list(possible_props.keys()))
                g.props[k] = possible_props[k] 
            
        out_suite[f'global_prop_{k}'] = v
    return suite

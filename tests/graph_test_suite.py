"""
Test suite of example graphs. This includes some very basic
cases and pathological cases; a richer repertoire
of graphs is included through networkx and the io.from_nx function. 

"""
import numpy as np
import tinygraph as tg
import networkx as nx
from tinygraph.io import from_nx

def gen_empty(N, dtype, rng):
    """

    Generate a random empty graph of the given dtype
    """

    return gen_random(N, dtype, [tg.default_one(dtype)], 0.0, rng)

def gen_fully_connected(N, dtype, rng):
    """
    generate a random fully-connected graph of the given dtype
    """
    return gen_random(N, dtype, [tg.default_one(dtype)], 1.0, rng)


def gen_linear(N, dtype, rng):
    """

    """

    e = gen_empty(N, dtype, rng)
    for i in range(N-1):
        e[i, i+1] = tg.default_one(dtype)
    return e

def gen_ladder(N, dtype):
    """
    Use networkx to generate a ladder graph (two paths with pairs connected) 
    with N vertices on each side of the ladder.
    """
    ng = nx.generators.classic.ladder_graph(N)
    return from_nx(ng, adj_type=dtype)

def gen_random(N, dtype, edge_weights, prob_edge, rng=None):
    """
    Generate a random graph of the given dtype with 
    a fixed edge probability. 0 = empty graph, 1.0 = full graph, 
    possible edge weight values from edge_weights

    """
    if rng is None:
        rng = np.random.RandomState()
        
    g = tg.TinyGraph(N, dtype)
    for i in range(N):
        for j in range(i+1, N):
            if rng.rand() < prob_edge:
                g[i, j] = rng.choice(edge_weights)
    return g

def add_random_ep(g, dt, rng=None):
    """
    Add a random edge property of dtype dt to g and fill it with
    with random values
    """
    if rng is None:
        rng = np.random.RandomState()

    name = "prop" + str(rng.randint(1000000))
    g.add_edge_prop(name, dt)

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
            basename = f"{N}_{str(dtype)[8:-2]}"

            name = f"empty_{basename}"
            out_graphs[name] = [gen_empty(N, dtype, rng)]
            
            name = f"fullyconnected_{basename}"
            out_graphs[name] = [gen_fully_connected(N, dtype, rng)]
            
            name = f"linear_{basename}"
            out_graphs[name] = [gen_linear(N, dtype, rng)]
          

    SAMPLE_N = 5
    for N in [4, 7, 16, 32, 100]:
        for prob_edge in [0.1, 0.5, 0.9]:
            
            dtype = np.bool
            edge_weights = [True]
            
            name = f"random_{prob_edge:.1f}_{str(dtype)[8:-2]}_{N}"
            out_graphs[name] = [gen_random(N, dtype, edge_weights, prob_edge, rng) \
                                for _ in range(SAMPLE_N)]
        

            dtype = np.int32
            name = f"random_{prob_edge:.1f}_{str(dtype)[8:-2]}_{N}"
            out_graphs[name] = []
            for i in range(SAMPLE_N):
                edge_weights = rng.randint(1, rng.randint(2, max(N//2, 3)),
                                                 size=rng.randint(1, N//2))
                
                out_graphs[name].append(gen_random(N, dtype, edge_weights, prob_edge, rng))


            dtype = np.float64
            name = f"random_{prob_edge:.1f}_{str(dtype)[8:-2]}_{N}"
            out_graphs[name] = []
            for i in range(SAMPLE_N):
                edge_weights = rng.rand(rng.randint(1, N//2)) + 0.5
                
                out_graphs[name].append(gen_random(N, dtype, edge_weights, prob_edge, rng))


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
    return out_suite
            
def create_suite_edge_prop(seed=0):
    
    rng = np.random.RandomState(seed)
    suite = create_suite(rng=rng)

    out_suite = {}
    
    for k, v in suite.items():
        for g in v:
            for i in range(rng.randint(1, 4)):
                add_random_ep(g, rng.choice([np.bool, np.int32, np.float64]),
                              rng)
        out_suite[f'ep_{k}'] = v

    return out_suite
            

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
            number = rng.randint(1, len(possible_props)+1)
            for i in range(number):
                k = rng.choice(list(possible_props.keys()))
                g.props[k] = possible_props[k] 
            
        out_suite[f'global_prop_{k}'] = v
    return out_suite

def create_nx_suite(seed=0, rng=None):
    """
    returns a dict of graphs generated by networkx for testing, 
    designed to be used in a pytest fixture
    """
    if rng is None:
        rng = np.random.RandomState(seed)

    out_graphs = {}
    
    for N in [1, 2, 4, 8, 16, 32, 64, 128]:
        for dtype in [np.bool, np.int32, np.float32, np.complex64]:
            basename = f"{N}_{str(dtype)[8:-2]}"
            name = f"ladder_{basename}"
            out_graphs[name] = [gen_ladder(N, dtype)]

    SAMPLE_N = 5
    # smp = [(4,.1),(4,.5),(4,.7),(7,.1),(7,.5),(16,.1),(16,.5),(32,.1),(100,.1)]
    # for N, prob_edge in smp:
    for N in [4,7,16,32,100]:
        for prob_edge in [.1,.5,.7]: 
            dtype = np.bool
            name = f"random_lobster_{prob_edge:.1f}_{str(dtype)[8:-2]}_{N}"
            out_graphs[name] = []
            for i in range(SAMPLE_N):
                ng = nx.generators.random_graphs.random_lobster(N,prob_edge,\
                            prob_edge,rng)
                if ng.number_of_nodes() == 0:
                    continue
                t = from_nx(ng,adj_type=dtype)
                out_graphs[name].append(t)


            dtype = np.int32
            name = f"random_lobster_{prob_edge:.1f}_{str(dtype)[8:-2]}_{N}"
            out_graphs[name] = []
            for i in range(SAMPLE_N):
                edge_weights = rng.randint(1, rng.randint(2, max(N//2, 3)),
                                                    size=rng.randint(1, N//2))
                ng = nx.generators.random_graphs.random_lobster(N,prob_edge,\
                            prob_edge,rng)
                if ng.number_of_nodes() == 0:
                    continue
                t = from_nx(ng,adj_type=dtype)
                for e1, e2 in t.edges():
                    t[e1, e2] = rng.choice(edge_weights)
                out_graphs[name].append(t)


            dtype = np.float64
            name = f"random_lobster_{prob_edge:.1f}_{str(dtype)[8:-2]}_{N}"
            out_graphs[name] = []
            for i in range(SAMPLE_N):
                edge_weights = rng.rand(rng.randint(1, N//2)) + 0.5
                ng = nx.generators.random_graphs.random_lobster(N,prob_edge,\
                            prob_edge,rng)
                if ng.number_of_nodes() == 0:
                    continue
                t = from_nx(ng,adj_type=dtype)
                for e1, e2 in t.edges():
                    t[e1, e2] = rng.choice(edge_weights)
                out_graphs[name].append(t)


    return out_graphs

def get_full_suite():
    basic_suite = create_suite()
    vp_suite = create_suite_vert_prop()
    ep_suite = create_suite_edge_prop()
    gl_suite = create_suite_global_prop()
    nx_suite = create_nx_suite()

    return {**basic_suite, **vp_suite, **ep_suite, **gl_suite, **nx_suite}

# Currently not-thorough testing just to speed validation of the basic library functionality

import numpy as np
import tinygraph as tg

def basic_functionality():
    t = tg.TinyGraph(2, vert_props={'color': np.int32})
    print("Original Adjacency Matrix")
    print(t.adjacency)

    t.add_node({'color': 3})
    print("After node insertion")
    print(t.adjacency)

    t.remove_node(0)
    print("After node removal")
    print(t.adjacency)

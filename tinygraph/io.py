# Functions for interactions between networkx and tinygraph.

import networkx, tinygraph

def tg_from_nx(net_x):
        """
        Initialize a TinyGraph instance from a networkx graph instance.

        Inputs:
            net_x (networkx Graph): graph to translate to TinyGraph.

        Outputs:
            tg (TinyGraph): TinyGraph instance corresponding to networkx graph.
        """

def to_networkx(tg):
    """
    Get a networkx copy of the current graph.

    Inputs:
        tg (TinyGraph): graph to translate to networkx.
    
    Outputs:
        g (networkx Graph): networkx graph of TinyGraph instance.
    """
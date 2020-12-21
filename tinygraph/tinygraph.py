import numpy as np

class TinyGraph:
    """
    tinygraph is centered around our representation of graphs through numpy 
    arrays.  The central feature is the adjacency matrix, which defines the 
    graph stucture under the assumption that we are using undirected, weighted 
    graphs without self-loops. Each graph also has a set of vertex properties 
    and a set of edge properties. We will also use numpy arrays to store the 
    properties at each node or edge. 
    """

    def __init__(node_N, adj_type = np.int32, vert_props = {}, edge_props = {}):
        """
        Initalize a new TinyGraph instance.

        Inputs:
            node_N (int): Number of nodes in the graph. Adding and removing 
                nodes is much slower than adding or removing edges, so setting 
                this value accurately initially can improve efficiency.
            adj_type (numpy type): The type of the edge weights.
            vert_props (string:numpy type): A map from vertex property names to 
                the types of each property.
            edge_props (string:numpy type): A map from edge property names to 
                the types of each property.
        """
        self.node_N = node_N
        self.adj_type = adj_type
        self.vert_props = vert_props
        self.edge_props = edge_props
        self.v = {} # 

    def __init__(net_x):
        """
        Initialize a TinyGraph instance from a networkx graph instance.

        Inputs:
            net_x (networkx Graph): graph to translate to TinyGraph.
        """

    def 
             
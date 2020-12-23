import numpy as np

class TinyGraph:
    """
    tinygraph is centered around our representation of graphs through numpy 
    arrays using the class TinyGraph. The central feature is the adjacency 
    matrix, which defines the graph stucture under the assumption that we are 
    using undirected, weighted graphs without self-loops. Each graph also has a 
    set of vertex properties and a set of edge properties. We will also use 
    numpy arrays to store the properties at each node or edge. 
    """

    def __init__(self,node_N,adj_type=np.int32,vert_props={},edge_props={}):
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

        Outputs:
            tg (TinyGraph): new TinyGraph instance.
        """
        self.node_N = node_N
        self.adj_type = adj_type
        self.adjacency = numpy.array([]) # Adjacency matrix - init to all None?
        self.vert_props = vert_props # Maybe don't need to keep these
        self.edge_props = edge_props
        self.v = {} # Dictionary mapping each property name to array of props
        self.e = {} # Array of props init to None?

    def add_node(self):
        """
        Add a node to a TinyGraph instance. This process can be slow because it 
        requires reshaping the adjancency and property arrays.

        Inputs: 
            None - nodes are indexed numerically 0...node_N - 1.

        Outputs:
            ? node_N (int): new number of nodes.
            
        """    

    def remove_node(self,n):
        """
        Remove a node from a TinyGraph instance. This process can be slow 
        because it requires reshaping the adjancency and property arrays. 

        Inputs:
            n (int): Node to remove. Nodes are indexed numerically 0...node_N-1.

        Outputs:
            ? adj (numpy array): The row of the adjacency matrix corresponding
                to the node removed.
            ? v_props (string:property): A map from vertex property names to 
                the property of the node removed. 
            ? e_props (string:property): A map from edge property names to 
                the list of the property for each edge of the node removed.
            ? node_N (int): new number of nodes
            ? None - modifications are made in place
        """

    def __setitem__(self,key,newValue):
        """
        Create an edge or change the weight of an existing edge. This operation 
        is fast.

        Inputs:
            key (int, int): Endpoint nodes of edge.
            newValue (adj_type): Weight of edge.

        Outputs:
            None - modifications are made in place.
        """

    def __getitem__(self,key):
        """
        Get the weight of an edge. This operation is fast.

        Inputs:
            key (int, int): Endpoint nodes of edge.

        Outputs:
            weight (adj_type): Weight of edge, or None (0?) if no edge exists.
        """

    def copy(self):
        """
        Get a copy of the TinyGraph instance.

        Inputs:
            None

        Outputs:
            tg (TinyGraph): Deep copy of TinyGraph instance.
        """
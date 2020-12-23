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

    def __init__(self, node_N, adj_type=np.int32, vert_props={}, edge_props={}):
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
        self.adjacency = np.zeros((node_N, node_N), dtype = adj_type)
        self.vert_props = vert_props # Maybe don't need to keep these
        self.edge_props = edge_props
        self.v = {} # Dictionary of property arrays (indexed by property name)
        self.e = {} # Same, but 2D arrays

        # Initialize vertex property arrays
        for vkey in vert_props.keys():
            self.v[vkey] = np.zeros(node_N, dtype = vert_props[vkey])

        # Initialize edge property arrays
        for ekey in edge_props.keys():
            self.e[ekey] = np.zeros((node_N, node_N), dtype = edge_props[ekey])

    def add_node(self, props={}):
        """
        Add a node to a TinyGraph instance. This process can be slow because it
        requires reshaping the adjancency and property arrays.
        The new node will have the highest index (node_N - 1).

        Inputs:
            # None - nodes are indexed numerically 0...node_N - 1.
            props - a dictionary for vertex property values
                    If a key is not recognized, it will be ignored.
                    If a key is missing, the corresponding value will be left as 0.

        Outputs:
            ? node_N (int): new number of nodes.

        """
        # # New Adjacency matrix
        # # Currently discards the old adjacency matrix entirely
        # new_adj = np.zeros((self.node_N+1, self.node_N+1), dtype=self.adj_type)
        # new_adj[:self.node_N, :self.node_N] = self.adjacency
        # self.adjacency = new_adj

        self.adjacency = np.insert(self.adjacency, self.node_N, 0, axis=0)
        self.adjacency = np.insert(self.adjacency, self.node_N, 0, axis=1)

        # New vertex property arrays
        for key in self.v.keys():
            # Can resize because it's flat
            self.v[key].resize(self.node_N+1)

            # Grab the argument value
            if key in props.keys():
                self.v[key][self.node_N] = props[key]

        # Update the node count
        self.node_N += 1

    def remove_node(self, n):
        """
        Remove a node from a TinyGraph instance. This process can be slow
        because it requires reshaping the adjancency and property arrays.
        Moves up the nodes after n so that the numbering remains dense.

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
        # First update adjacency matrix
        self.adjacency = np.delete(self.adjacency, n, axis=0)
        self.adjacency = np.delete(self.adjacency, n, axis=1)

        # Trim the property arrays
        for key in self.v.keys():
            np.delete(self.v[key], n)

        # Update the node count
        self.node_N -= 1

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

# Cant get the module to import >:(
# t = TinyGraph(2, vert_props={'color': np.int32})
# print("Original Adjacency Matrix")
# print(t.adjacency)

# t.add_node({'color': 3})
# print("After node insertion")
# print(t.adjacency)

# t.remove_node(0)
# print("After node removal")
# print(t.adjacency)

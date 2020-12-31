import numpy as np

def default_zero(dtype):
    """
    For a given dtype, return the zero value (which
    will indicate the absence of an edge)
    """
    if dtype == np.bool:
        return False
    elif np.issubdtype(dtype, np.number):
        return 0
    else:
        raise ValueError(f"unknown dtype {dtype}")

def default_one(dtype):
    """
    For a given dtype, return the default one value (which
    will indicate the presence of an edge / be the default weight)
    """
    if dtype == np.bool:
        return True
    elif np.issubdtype(dtype, np.number):
        return 1
    else:
        
        raise ValueError(f"unknown dtype {dtype}")


class EdgeProxy:
    """
    EdgeProxy is a container for 2-d numpy arrays representing edge properties.
    EdgeProxy enforces rules onto how and when edge properties are assigned.
    """

    def __init__(self, g, dtype):
        """
        Initialize a new EdgeProxy instance.

        Inputs:
            g (TinyGraph): The graph which EdgeProxy is storing a property for.
                EdgeProxy will not change the graph in any way, but will check
                its adjacency matrix.
            dtype (np.dtype): The datatype of the 2-d numpy matrix to store.
        
        Outputs:
            ep (EdgeProxy): new EdgeProxy object.
        """
        self.__g = g
        self.__props = np.zeros((self.__g.node_N, self.__g.node_N), dtype=dtype)

    @property
    def dtype(self):
        return self.__props.dtype

    def __setitem__(self, key, value):
        """
        Set an edge's property.

        Inputs:
            key ((int, int)): Endpoints of edge to set the property of.
            value (dtype): Value to set edge property to.

        Outputs:
            None
        """
        if len(key) < 2:
            raise IndexError("Must include both endpoints of edge.")
        elif len(key) > 2:
            raise IndexError("Too many endpoints given.")
        else:
            e1, e2 = key
            if self.__g[e1, e2] == default_zero(self.__props.dtype):
                raise Exception("No such edge.")
            else:
                self.__props[e1, e2] = value
                self.__props[e2, e1] = value

    def __getitem__(self, key):
        """
        Get an edge's property.

        Inputs:
            key ((int, int)): Endpoints of edge to get the property of.

        Outputs:
            value (dtype): Value of edge property.
        """
        if len(key) < 2:
            raise IndexError("Must include both endpoints of edge.")
        elif len(key) > 2:
            raise IndexError("Too many endpoints given.")
        else:
            e1, e2 = key
            if self.__g[e1, e2] == default_zero(self.__props.dtype):
                raise Exception("No such edge.")
            else:
                return self.__props[e1, e2]


class TinyGraph:
    """
    tinygraph is centered around our representation of graphs through numpy
    arrays using the class TinyGraph. The central feature is the adjacency
    matrix, which defines the graph stucture under the assumption that we are
    using undirected, weighted graphs without self-loops. Each graph also has a
    set of vertex properties and a set of edge properties. We will also use
    numpy arrays to store the properties at each node or edge.
    """

    def __init__(self, node_N, adj_type=np.int32, vp_types={}, ep_types={}):
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

        self.__node_N = node_N
        self.adjacency = np.zeros((node_N, node_N), dtype = adj_type)

        self.v = {}
        self.e = {}
        
        for k, dt in vp_types.items():
            self.add_vert_prop(k, dt)

        for k, dt in ep_types.items():
            self.add_edge_prop(k, dt)

    @property
    def node_N(self):
        return self.__node_N

    def add_vert_prop(self, name, dtype):
        """
        Add the vertex property named 'name' to the graph. 

        Inputs:
             name : name (string)
             dtype : numpy dtype
        """
        if name in self.v:
            raise KeyError(f"Graph already has vertex property named {name}")
        
        self.v[name] = np.zeros(self.__node_N, dtype=dtype)

    def add_edge_prop(self, name, dtype):
        """
        Add the edge property named 'name' to the graph. 
        
        Inputs: 
             name : name (string)
             dtype : numpy dtype

        """
        
        if name in self.e:
            raise KeyError(f"Graph already has edge property named {name}")
        
        self.e[name] = EdgeProxy(self, dtype)

    def remove_vert_prop(self, name):
        """
        Removes the indicated vertex property from the graph

        Inputs:
             name: the name of the property

        """

        del self.v[name]
        
    def remove_edge_prop(self, name):
        """
        Removes the indicated edge property from the graph

        Inputs:
             name: the name of the property

        """

        del self.e[name]
        


    def add_node(self, props = {}, **kwargs):
        """
        Add a node to a TinyGraph instance. This process can be slow because it
        requires reshaping the adjacency and property arrays.
        The new node will have the highest index (node_N - 1).

        Inputs:
             properties are passed as key=value pairs or as a props dictionary
                If a key is not recognized, it will raise an error
                If a key is missing, the corresponding value will be left as 0
                for whatever the corresponding dtype is

        Outputs:
            None - modifications are made in place.

        """
        # # New Adjacency matrix
        # # Currently discards the old adjacency matrix entirely
        # new_adj = np.zeros((self.node_N+1, self.node_N+1), dtype=self.adj_type)
        # new_adj[:self.node_N, :self.node_N] = self.adjacency
        # self.adjacency = new_adj

        self.adjacency = np.insert(self.adjacency, self.__node_N, 0, axis=0)
        self.adjacency = np.insert(self.adjacency, self.__node_N, 0, axis=1)

        combined_props = {**props, **kwargs}
        # New vertex property arrays
        for key in self.v.keys():
            # Can resize because it's flat
            self.v[key].resize(self.__node_N+1)

            # Grab the argument value
            if key in combined_props.keys():
                self.v[key][self.__node_N] = props[key]

        # Reshape edge property arrays
        for key in self.e.keys():
            self.e[key] = np.insert(self.e[key], self.__node_N, 0, axis=0)
            self.e[key] = np.insert(self.e[key], self.__node_N, 0, axis=1)

        # Update the node count
        self.__node_N += 1

    def remove_node(self, n):
        """
        Remove a node from a TinyGraph instance. This process can be slow
        because it requires reshaping the adjacency and property arrays.
        Moves up the nodes after n so that the numbering remains dense.

        Inputs:
            n (int): Node to remove. Nodes are indexed numerically 0...node_N-1.

        Outputs:
            None - modifications are made in place.
        """
        # First update adjacency matrix
        self.adjacency = np.delete(self.adjacency, n, axis=0)
        self.adjacency = np.delete(self.adjacency, n, axis=1)

        # Trim the vertex property arrays
        for key in self.v.keys():
            self.v[key] = np.delete(self.v[key], n)

        # Trim the edge property arrays
        for key in self.e.keys():
            self.e[key] = np.delete(self.e[key], n, axis = 0)
            self.e[key] = np.delete(self.e[key], n, axis = 1)

        # Update the node count
        self.__node_N -= 1

    def __setitem__(self, key, newValue):
        """
        Create an edge or change the weight of an existing edge. This operation
        is fast. Edges are undirected.

        Inputs:
            key (int, int): Endpoint nodes of edge.
            newValue (adj_type): Weight of edge.

        Outputs:
            None - modifications are made in place.
        """
        if len(key) < 2:
            raise IndexError("Must include both endpoints of edge.")
        elif len(key) > 2:
            raise IndexError("Too many endpoints given.")
        self.adjacency[key[0]][key[1]] = newValue
        self.adjacency[key[1]][key[0]] = newValue

    def __getitem__(self, key):
        """
        Get the weight of an edge. This operation is fast.

        Inputs:
            key (int, int): Endpoint nodes of edge.

        Outputs:
            weight (adj_type): Weight of edge, or None (0?) if no edge exists.
        """
        if len(key) < 2:
            raise IndexError("Must include both endpoints of edge.")
        elif len(key) > 2:
            raise IndexError("Too many endpoints given.")
        return self.adjacency[key[0]][key[1]]

    # def add_edge(self, i, j, weight=None, props={}, **kwargs):
    #     """

    #     ## FIXME clean up this docstring

    #     Convenience function for adding an edge. kw arguments are
    #     turned into properties as well. 

    #     """

    #     if self.adjacency[i, j] != default_zero(self.adjacency.dtype):
    #         raise ValueError(f"Edge ({i, j}) already exists")
        
    #     if weight is None:
    #         weight = default_one(self.adjacency.dtype)

    #     combined_props = {**props, **kwargs}

    #     self.adjacency[i, j] = weight
    #     self.adjacency[j, i] = weight

    #     for k, v in combined_props.items():
    #         self.e[k][i, j] = v
                    

    def copy(self):
        """
        Get a copy of the TinyGraph instance.

        Inputs:
            None

        Outputs:
            newGraph (TinyGraph): Deep copy of TinyGraph instance.
        """
        v_p = {k : v.dtype for k, v in self.v.items()}
        e_p = {k : e.dtype for k, e in self.e.items()}

        newGraph = TinyGraph(self.__node_N, self.adjacency.dtype,
                             v_p, e_p)
        newGraph.adjacency[:] = self.adjacency

        for key, arr in self.v.items():
            newGraph.v[key][:] = arr[i]
            
        # Set edge properties
        for key, arr in self.v.items():
            newGraph.e[key][:] = arr

        return newGraph

    def get_vert_props(self, n):
        """
        Get the properties at a given vertex.

        Inputs:
            n (int): Vertex to get properties of.

        Outputs:
            props (string:prop_type): A dictionary mapping each of the vertex
                property names to the property at the input vertex.
        """
        props = {}
        for key, arr in self.v.items():
            props[key] = arr[n]
        return props

    def get_edge_props(self, n1, n2):
        """
        Get the properties at a given edge.

        Inputs:
            n1 (int): Endpoint node 1 of edge to get properties of.
            n2 (int): Endpoint node 2 of edge to get properties of.

        Outputs:
            props (string:prop_type): A dictionary mapping each of the edge
                property names to the property at the input edge.
        """
        props = {}
        for key, arr in self.e.items():
            props[key] = arr[n1,n2]
        return props

    def __repr__(self):
        """
        Representation of graph for debugging.

        Inputs:
            None

        Outputs:
            rep (str): TinyGraph Representation.
        """
        rep = "Vertices:\n"
        for i in range(self.__node_N):
            rep += str(i) + ": " + str(self.get_vert_props(i)) + "\n"
        rep += "\nEdges:\n"
        for i in range(self.__node_N-1):
            for j in range(i+1, self.__node_N):
                if self.adjacency[i,j]: # Change to not is None?
                    rep += "(" + str(i) + ", " + str(j) + "): " + \
                        str(self.get_edge_props(i,j)) + "\n"
        return rep[:-1] # strip last newline 

    def get_neighbors(self, n):
        """
        Get the neighbors of a node.

        Inputs:
            n (int): The node to get the neighbors of.

        Outputs:
            neighbors ([int]): A list of the neighbor nodes.
        """
        neighbors = np.argwhere(self.adjacency[n] != \
                                default_zero(self.adjacency.dtype)).flatten()
        # for i, w in enumerate(self.adjacency[n]):
        #     if not i == n and not w == 0:
        #         neighbors.append(i)
        return neighbors

    def edges(self, weight = False, edge_props = []):
        """
        Get a list of the edges by endpoint nodes, optionally with their weight 
        and some properties.

        Inputs:
            weight (bool): Whether to return the weight of each edge. By default
                this if false and the weight is not returned.
            edge_props ([string]): A list of edge properties to return, by name.
                By default this is empty and no properties are returned. Must be
                a list of existing properties.

        Outputs:
            edges ([edge]): A list of edges, where each edge is represented by a
                tuple. The first two elements of the tuple are the endpoints of
                the edge. If weights is true, the third element is the weight of
                the edge. If edge_props is not empty, a dictionary mapping the 
                properties provided to the value for the edge is the final 
                element of the tuple.
        """
        edges = []
        for i, j in np.argwhere(self.adjacency != 
                                    default_zero(self.adjacency.dtype)):
            if i < j:
                e = (i, j)
                if weight:
                    e += (self[i,j],)
                if edge_props:
                    d = {}
                    for p in edge_props:
                        d[p] = self.e[p][i,j]
                    e += (d,)
                edges.append(e)
        return edges

    def permute(self, perm):
        """
        Permute the vertices of the graph to create a new TinyGraph instance.

        Inputs:
            perm (map): A mapping from old vertices to new vertices, such that 
                perm[old_vertex] = new_vertex. 

        Outputs:
            g (TinyGraph): A new TinyGraph instance with each vertex, and its
                corresponding vertex and edge properties, permuted.
        """
        g = TinyGraph(self.__node_N, self.adjacency.dtype, 
                        {p:val.dtype for p, val in self.v.items()},
                        {p:val.dtype for p, val in self.e.items()})
        for (e1, e2, w, d) in self.edges(weight=True, edge_props=self.e.keys()):
            g[perm[e1],perm[e2]] = w 
            for prop, val in d.items():
                g.e[prop][perm[e1], perm[e2]] = val
        for ind in range(self.__node_N):
            for prop, val in self.get_vert_props(ind):
                g.v[prop][perm[ind]] = val
        return g
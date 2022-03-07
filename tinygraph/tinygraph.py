import numpy as np
from copy import deepcopy

def default_zero(dtype):
    """
    For a given dtype, return the zero value (which will indicate the absence of
    an edge). Raises an error on unknown datatypes.

    Inputs:
        dtype (class): Datatype of property or array.

    Outputs:
        def_zero (dtype): Default zero value of given dtype.
    """
    if dtype == np.bool_ or dtype == bool:
        return False
    elif np.issubdtype(dtype, np.number):
        return 0
    elif np.issubdtype(dtype, np.str_):
        # Empty string!
        return ""
    else:
        raise ValueError(f"unknown dtype {dtype}")

def default_one(dtype):
    """
    For a given dtype, return the one value (which will indicate the presence of
    an edge). Raises an error on unknown datatypes.

    Inputs:
        dtype (class): Datatype of property or array.

    Outputs:
        def_one (dtype): Default one value of given dtype.
    """
    if dtype == np.bool:
        return True
    elif np.issubdtype(dtype, np.number):
        return 1
    else:
        # Fails on strings
        raise ValueError(f"unknown dtype {dtype}")


class EdgeProxy:
    """
    EdgeProxy is a way of accessing an edge property in a graph safely.
    EdgeProxy enforces rules onto how and when edge properties are assigned.
    """

    def __init__(self, g, prop):
        """
        Initialize a new EdgeProxy instance.

        Inputs:
            g (TinyGraph): The graph which EdgeProxy is accessing a property of.
                EdgeProxy will alter one property in g.e_p.
            property (str): The name of the property to access.
        
        Outputs:
            ep (EdgeProxy): new EdgeProxy object.
        """
        self.__g = g
        self.__prop = prop
        self.__dtype = self.__g.e_p[self.__prop].dtype

    @property
    def dtype(self):
        return self.__dtype

    def __setitem__(self, key, value):
        """
        Set an edge's property.

        Inputs:
            key ((int, int)): Endpoints of edge to set the property of.
            value (dtype): Value to set edge property to.

        Outputs:
            None
        """
        if key.__class__ != tuple:
            raise KeyError("Expecting exactly two endpoints.")
        elif len(key) != 2:
            raise KeyError("Expecting exactly two endpoints.")
        else:
            e1, e2 = key
            if self.__g[e1, e2] == default_zero(self.dtype):
                raise IndexError("No such edge.")
            else:
                self.__g.e_p[self.__prop][e1, e2] = value
                self.__g.e_p[self.__prop][e2, e1] = value

    def __getitem__(self, key):
        """
        Get an edge's property.

        Inputs:
            key ((int, int)): Endpoints of edge to get the property of.

        Outputs:
            value (dtype): Value of edge property.
        """
        if key.__class__ != tuple:
            raise KeyError("Expecting exactly two endpoints.")
        elif len(key) != 2:
            raise KeyError("Expecting exactly two endpoints.")
        else:
            e1, e2 = key
            if self.__g[e1, e2] == default_zero(self.dtype):
                raise IndexError("No such edge.")
            else:
                return self.__g.e_p[self.__prop][e1, e2]        

class EdgeProxyGenerator:
    """
    EdgeProxyGenerator is the go between for TinyGraph and EdgeProxy. TinyGraph
    gives its users EdgeProxyGenerators that then give them access to edges
    through a generator EdgeProxy
    """

    def __init__(self, g):
        """
        Create a new Generator.

        Inputs:
            g (TinyGraph): The graph that this generator is linked to.

        Outputs:
            epg (EdgeProxyGenerator): New generator
        """
        self.__g = g

    def keys(self):
        return self.__g.e_p.keys()

    def items(self):
        return self.__g.e_p.items()

    def __len__(self):
        return len(self.__g.e_p)

    def __contains__(self, key):
        return key in self.__g.e_p

    def __getitem__(self, key):
        """
        Generates an EdgeProxy object for a user to access an edge property.

        Inputs:
            key (str): The property name to access

        Outputs:
            ep (EdgeProxy): An EdgeProxy object with access to the desired 
                property and the current graph.
        """
        return EdgeProxy(self.__g, key)

class TinyGraph:
    """
    TinyGraph is centered around our representation of graphs through numpy
    arrays using the class TinyGraph. The central feature is the adjacency
    matrix, which defines the graph stucture under the assumption that we are
    using undirected, weighted graphs without self-loops. Each graph also has a
    set of vertex properties and a set of edge properties. We will also use
    numpy arrays to store the properties at each vertex or edge.
    """

    def __init__(self, vert_N, adj_type=np.float32, vp_types={}, ep_types={}):
        """
        Initalize a new TinyGraph instance.

        Inputs:
            vert_N (int): Number of vertices in the graph. Adding and removing
                vertices is much slower than adding or removing edges - setting
                this value accurately initially can improve efficiency.
            adj_type (numpy type): The type of the edge weights.
            vp_types (str:numpy type): A map from vertex property names to
                the types of each property.
            ep_types (str:numpy type): A map from edge property names to
                the types of each property.

        Outputs:
            tg (TinyGraph): new TinyGraph instance.
        """

        self.__vert_N = vert_N
        self.adjacency = np.zeros((vert_N, vert_N), dtype = adj_type)

        self.v = {}
        self.e_p = {}
        self.e = EdgeProxyGenerator(self)
        
        for k, dt in vp_types.items():
            self.add_vert_prop(k, dt)

        for k, dt in ep_types.items():
            self.add_edge_prop(k, dt)

        self.props = {}
        
    @property
    def vert_N(self):
        return self.__vert_N
    @property
    def edge_N(self):
        e = np.count_nonzero(self.adjacency)
        if e%2 != 0:
            raise Exception("Adjacency matrix has become asymmetric - number of\
                edges ambiguous")
        else:
            return e//2

    def add_vert_prop(self, name, dtype):
        """
        Add the vertex property named 'name' to the graph. 

        Inputs:
            name (str): property name
            dtype (class): numpy dtype of property

        Outputs:
            None
        """
        if name in self.v:
            raise KeyError(f"Graph already has vertex property named {name}")
        
        self.v[name] = np.zeros(self.__vert_N, dtype=dtype)

    def add_edge_prop(self, name, dtype):
        """
        Add the edge property named 'name' to the graph. 
        
        Inputs:
            name (str): property name
            dtype (class): numpy dtype of property

        Outputs:
            None
        """
        
        if name in self.e_p:
            raise KeyError(f"Graph already has edge property named {name}")
        
        self.e_p[name] = np.zeros((self.__vert_N, self.__vert_N), dtype=dtype)

    def remove_vert_prop(self, name):
        """
        Removes the indicated vertex property from the graph

        Inputs:
            name (str): the name of the property

        Outputs:
            None
        """

        del self.v[name]
        
    def remove_edge_prop(self, name):
        """
        Removes the indicated edge property from the graph

        Inputs:
            name (str): the name of the property

        Outputs:
            None
        """

        del self.e_p[name]
        


    def add_vertex(self, props = {}, **kwargs):
        """
        Add a vertex to a TinyGraph instance. This process can be slow because 
        it requires reshaping the adjacency and property arrays.
        The new vertex will have the highest index (vert_N - 1).

        Inputs:
            properties are passed as key=value pairs or as a props dictionary
                If a key is not recognized, it will raise an error
                If a key is missing, the corresponding value will be left as 0
                for whatever the corresponding dtype is

        Outputs:
            None - modifications are made in place.
        """
        self.adjacency = np.insert(self.adjacency, self.__vert_N, 0, axis=0)
        self.adjacency = np.insert(self.adjacency, self.__vert_N, 0, axis=1)

        combined_props = {**props, **kwargs}
        # New vertex property arrays
        for key in self.v.keys():
            # Can resize because it's flat
            self.v[key].resize(self.__vert_N+1)

            # Grab the argument value
            if key in combined_props.keys():
                self.v[key][self.__vert_N] = props[key]

        # Reshape edge property arrays
        for key in self.e_p.keys():
            self.e_p[key] = np.insert(self.e_p[key], self.__vert_N, 0, axis=0)
            self.e_p[key] = np.insert(self.e_p[key], self.__vert_N, 0, axis=1)

        # Update the vertex count
        self.__vert_N += 1

    def remove_vertex(self, n):
        """
        Remove a vertex from a TinyGraph instance. This process can be slow
        because it requires reshaping the adjacency and property arrays.
        Moves up the vertices after n so that the numbering remains dense.

        Inputs:
            n (int): Vertex to remove. Vertices are indexed numerically 
                (0...vert_N-1).

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
        for key in self.e_p.keys():
            self.e_p[key] = np.delete(self.e_p[key], n, axis = 0)
            self.e_p[key] = np.delete(self.e_p[key], n, axis = 1)

        # Update the vertex count
        self.__vert_N -= 1

    def __setitem__(self, key, newValue):
        """
        Create an edge or change the weight of an existing edge. This operation
        is fast. Edges are undirected. If an existing edge is set to its zero 
        value, it is removed, setting all of its property values to their zeros.

        Inputs:
            key (int, int): Endpoint vertices of edge.
            newValue (adj_type): Weight of edge.

        Outputs:
            None - modifications are made in place.
        """
        if key.__class__ != tuple:
            raise KeyError("Expecting exactly two endpoints.")
        elif len(key) != 2:
            raise KeyError("Expecting exactly two endpoints.")
        e1, e2 = key
        if e1 == e2:
            raise IndexError("Self-loops are not allowed.")
        self.adjacency[e1, e2] = newValue
        self.adjacency[e2, e1] = newValue
        if newValue == default_zero(self.adjacency.dtype):
            for k, prop in self.e_p.items():
                self.e_p[k][e1, e2] = default_zero(prop.dtype)
                self.e_p[k][e2, e1] = default_zero(prop.dtype)

    def __getitem__(self, key):
        """
        Get the weight of an edge. This operation is fast.

        Inputs:
            key (int, int): Endpoint vertices of edge.

        Outputs:
            weight (adj_type): Weight of edge, or None (0?) if no edge exists.
        """
        if key.__class__ != tuple:
            raise KeyError("Expecting exactly two endpoints.")
        elif len(key) != 2:
            raise KeyError("Expecting exactly two endpoints.")
        return self.adjacency[key[0]][key[1]]

    def copy(self):
        """
        Get a copy of the TinyGraph instance.

        Inputs:
            None

        Outputs:
            new_graph (TinyGraph): Deep copy of TinyGraph instance.
        """
        v_p = {k : v.dtype for k, v in self.v.items()}
        e_p = {k : e.dtype for k, e in self.e_p.items()}

        new_graph = TinyGraph(self.__vert_N, self.adjacency.dtype, v_p, e_p)
        new_graph.adjacency[:] = self.adjacency

        # Set vertex properties
        for key, arr in self.v.items():
            new_graph.v[key][:] = self.v[key]

        # Set edge properties
        for key, arr in self.e.items():
            new_graph.e_p[key][:] = self.e_p[key]

        for k, v in self.props.items():
            new_graph.props[k] = deepcopy(v)
            
        return new_graph

    def get_vert_props(self, n, vert_props = None):
        """
        Get the properties at a given vertex.

        Inputs:
            n (int): Vertex to get properties of.
            vert_props ([str]): A list of the vertex properties to return, by
                name.

        Outputs:
            props (str:prop_type): A dictionary mapping each of the vertex
                property names to the property at the input vertex.
        """
        if vert_props is None:
            vert_props = self.v.keys()
        props = {}
        for key in vert_props:
            props[key] = self.v[key][n]
        return props

    def get_edge_props(self, n1, n2, edge_props = None):
        """
        Get the properties at a given edge.

        Inputs:
            n1 (int): Endpoint vertex 1 of edge to get properties of.
            n2 (int): Endpoint vertex 2 of edge to get properties of.
            edge_props ([str]): A list of the edge properties to return, by
                name.

        Outputs:
            props (str:prop_type): A dictionary mapping each of the edge
                property names to the property at the input edge.
        """
        if edge_props is None:
            edge_props = self.e_p.keys()
        props = {}
        for key in edge_props:
            props[key] = self.e_p[key][n1,n2]
        return props

    def __repr__(self):
        """
        Printable representation of a graph.

        Inputs:
            None

        Outputs:
            rep (str): TinyGraph Representation. 
        """

        rep = "TinyGraph dtype=" + str(self.adjacency.dtype) + ", vert_N=" + \
            str(self.vert_N) + ", edge_N=" + str(self.edge_N) + "\n" 
        return rep
    
    def print_full_graph(self):
        """
        Full representation of a graph. Includes all global, vertex and edge
        properties.

        Inputs:
            None

        Outputs:
            None - prints representation.
        """
        rep = "Global Properties:\n"
        for name, prop in self.props.items():
            rep += str(name) + ": " + str(prop) + "\n"
        rep += "\nVertices:\n"
        for i, props in self.vertices(vert_props = self.v.keys()):
            rep += str(i) + ": " + str(props) + "\n"
        rep += "\nEdges:\n"
        for i,j,w,props in self.edges(weight = True,edge_props = self.e.keys()): 
            rep += "(" + str(i) + ", " + str(j) + "): Weight - " + str(w) +\
                ", Props - " + str(props) + "\n"
        print(rep[:-1]) # strip last newline 

    def get_neighbors(self, n):
        """
        Get the neighbors of a vertex.

        Inputs:
            n (int): The vertex to get the neighbors of.

        Outputs:
            neighbors ([int]): A list of the neighbor vertices.
        """
        neighbors = np.argwhere(self.adjacency[n] != \
                                default_zero(self.adjacency.dtype)).flatten()
        # for i, w in enumerate(self.adjacency[n]):
        #     if not i == n and not w == 0:
        #         neighbors.append(i)
        return neighbors

    def edges(self, weight = False, edge_props = None):
        """
        Get a list of the edges by endpoint vertices, optionally with their 
        weight and some properties.

        Inputs:
            weight (bool): Whether to return the weight of each edge. By default
                this if false and the weight is not returned.
            edge_props ([str]): A list of edge properties to return, by name.
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
                if not edge_props is None:
                    d = self.get_edge_props(i,j,edge_props)
                    e += (d,)
                edges.append(e)
        return edges

    def vertices(self, vert_props = []):
        """
        Get a list of the vertices with some of their properties.

        Inputs:
            vert_props ([str]): A list of vertex properties to return, by name.
                By default this is empty and an empty map is returned. Must be
                a list of existing properties.

        Outputs:
            vertices ([vertex]): A list of vertices, where each vertex is 
                represented by a tuple. The first element of the tuple is the 
                vertex index. The second element is a map from the provided 
                vertex properties to the values at the vertex. Even when no 
                properties are provided, a map is returned, since the list of 
                vertices is simply 0...N-1, which can be retrieved more 
                efficiently in other ways.
        """
        vertices = []
        for i in range(self.__vert_N):
            n = (i, self.get_vert_props(i,vert_props),)
            vertices.append(n)
        return vertices

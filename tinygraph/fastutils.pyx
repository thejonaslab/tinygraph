import numpy as np
cimport numpy as np
from cython.view cimport array as cvarray

import tinygraph
from libc.stdlib cimport calloc, free
from cython cimport view
import time

cimport cython

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef _get_all_neighbors(np.uint8_t[:,:] adj, np.int32_t[:, :] neighbors_out):  
    """
    For a TG with N vertices returns a NxN numpy array of
    neighbors, where the ith row lists the vertex IDs of the 
    neighbors (and -1 otherwise)
    """
    
    cdef int N = adj.shape[0]
    cdef int * current_pos = <int *> calloc(N,sizeof(int))
    
    for i in range(N):
        for j in range(N):
            if adj[i, j]:
                neighbors_out[i][current_pos[i]] = j
                current_pos[i] += 1

    free(current_pos)

def get_all_neighbors(tg):  
    """
    For a TG with N vertices returns a NxN numpy array of
    neighbors, where the ith row lists the vertex IDs of the 
    neighbors (and -1 otherwise)
    """

    neighbors_out = np.ones((tg.vert_N, tg.vert_N), dtype=np.int32) * -1
    
    
    _get_all_neighbors(tg.adjacency != tinygraph.default_zero(tg.adjacency.dtype),
                       neighbors_out)

    return neighbors_out

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef _get_connected_components(np.uint8_t[:, :] adj, np.int32_t[:] components_out):


    cdef int N = adj.shape[0]

    # precompute neighbor list
    cdef np.int32_t[:, ::1] neighbors = view.array(shape=(N, N), itemsize=sizeof(int), format="i")
    neighbors[:] = -1
    _get_all_neighbors(adj, neighbors)

    # Track which vertices have not been visited yet, and keep a set with all of 
    # the connected components.    
    cdef np.int32_t[:] unseen = np.ones(N, dtype=np.int32)
    cdef np.int32_t[:] comp = np.zeros(N, dtype=np.int32)
    cdef np.int32_t[:] bfs = np.zeros(N, dtype=np.int32)
    
    cdef int unseen_num = N
    cdef int bfs_num = 0
    cdef int start, current, n_i, n

    cdef int current_comp_num = 0
    
    while unseen_num > 0:
        # While there are still unvisited vertices, start from an unvisited vertex
        # and explore its connected component.
        comp[:] = 0
        bfs[:] = 0
        bfs_num = 0
        start = -1
        for i in range(N):
            if unseen[i]:
                start = i
                break;


        bfs[start] = 1
        bfs_num += 1
        
        while bfs_num > 0:
            # Explore a new vertex in the connected component, adding it to the 
            # connected component set and adding its neighbors to the set to 
            # explore next.
            
            for i in range(N):
                if bfs[i] > 0:
                    current = i
                    bfs[i] = 0
                    bfs_num -= 1
                    break
            unseen[current] = 0
            unseen_num -= 1

            components_out[current] = current_comp_num
            
            for n_i in range(N):
                n = neighbors[current, n_i]
                if n < 0:
                    break
                if unseen[n]:
                    if bfs[n] == 0:
                        bfs_num += 1
                    bfs[n] = 1

        # Add this connected component to the set of connected components
        current_comp_num += 1
        


cpdef get_connected_components(tg):
    """
    Get a list of the connected components in the TinyGraph instance.

    Inputs:
        tg (TinyGraph): graph to find components of.

    Outputs:
        cc ([{int}]): A list of connected components of tg, where each connected
            component is given by a set of the vertices in the component.
    """

    if tg.vert_N == 0:
        return []
    
    comp_array = np.ones(tg.vert_N, dtype=np.int32) * -1
    _get_connected_components(tg.adjacency != tinygraph.default_zero(tg.adjacency.dtype),
                              comp_array)


    #assert np.all(comp_array != -1)

    out_sets = {}
    for ci, c in enumerate(comp_array):
        if c not in out_sets:
            out_sets[c] = set()
        out_sets[c].add(ci)

    out= list(out_sets.values())

    return out

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef np.float64_t[:,:,:] floyd_warshall(np.float64_t[:,:,:] distances, int n):
    cdef double newL = 0
    for k in range(n):
        for j in range(n):
            for i in range(n):
                newL = distances[0][i][k] + distances[0][k][j]
                if distances[0][i][j] > newL:
                    distances[0][i][j] = newL
                    distances[1][i][j] = distances[1][i][k]
    return distances

cpdef _floyd_warshall(d, n):
    return floyd_warshall(d, n)

def get_shortest_paths(tg, weighted, paths=False):
    """
    Get the distance from each vertex to each other vertex on the shortest path. 
    Uses Floyd-Warshall to calculate the distances of the shortest paths.

    Inputs:
        tg (TinyGraph): The graph to find the shortest paths in.
        weighted (bool): Whether to consider the weights of the edges, or to 
            consider only the lengths of the path. If weighted is true, the 
            distance of a path is calculated by the sum of the weights on the 
            path. If false, the distance is calculated by the number of vertices on
            the path.
        paths (bool): Whether to also return the matrix of next steps in the paths,
            which is an NxN matrix describing which node to move to next to take 
            the shortest path from the current node to the target node. This can
            be used to reconstruct the path that is the shortest path between two
            nodes.

    Outputs:
        distances ([[int]]): A list of the distance to each vertex. The lists are
            ordered by vertex number, so distances[0] is a list of the distances 
            from vertex 0 to the other vertices (e.g. distances[0][3] = distance from
            vertex 0 to vertex 3 shortest path from 0 to 3; distances[2][2] = 0 is 
            distance from vertex 2 to itself). If no path exists between the 
            vertices, the result is None.
    """
    return _get_shortest_paths(tg, weighted, paths)

cpdef _get_shortest_paths(tg, weighted, paths):
    next = np.ones_like(tg.adjacency, dtype = np.float64)
    for i in range(tg.vert_N):
        next[i, :] = np.arange(tg.vert_N)
    if not weighted:
        distances = np.ones_like(tg.adjacency, dtype = np.float64)
        distances[tg.adjacency == tinygraph.default_zero(tg.adjacency.dtype)] = np.inf
        next[tg.adjacency == tinygraph.default_zero(tg.adjacency.dtype)] = np.inf
        np.fill_diagonal(distances, 0)
    elif not np.issubdtype(tg.adjacency.dtype, np.number):
        raise TypeError("Graph weights are not numbers.")
    else:
        distances = np.array(tg.adjacency,dtype=np.float64,copy=True)
        distances[tg.adjacency == 0] = np.inf
        next[tg.adjacency == 0] = np.inf
        np.fill_diagonal(distances, 0)
    np.fill_diagonal(next, range(tg.vert_N))
    tracking = np.stack((distances, next))
    tracking = np.array(floyd_warshall(tracking, tg.vert_N))
    for i in range(tg.vert_N):
        if tracking[0][i][i] < 0:
            raise Exception("Graph has a negative cycle.")
    if paths:
        return tracking[0,:,:], tracking[1,:,:]
    else:
        return tracking[0,:,:]

def construct_all_shortest_paths(next):
    """
    Given the next matrix from the Floyd-Warshall shortest paths algorithm,
    construct the sequence of nodes that comprises the shortest path
    between two nodes for all nodes.

    Inputs:
        next (np array): NxN matrix giving the next step to get from node i 
            to node j, as described in the get_shortest_paths algorithm.

    Ouputs:
        paths ([[[int]]]): A numpy array representing the paths between 
            any two nodes, i and j, by the nodes on the path in order,
            including both i and j. After reaching j, all values are
            np.inf. If i and j are not connected, all values are np.inf.
    """
    n = next.shape[0]
    paths = np.full((n,n,n), np.inf)
    paths = np.array(_construct_all_shortest_paths(paths, next, n))
    return paths

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing.
cdef np.float64_t[:,:,:] _construct_all_shortest_paths(np.float64_t[:,:,:] paths, np.float64_t[:,:] next, int N):
    cdef int loc = 0
    for i in range(N):
        for j in range(N):
            if not next[i][j] == np.inf:
                loc = i
                for k in range(N):
                    paths[i][j][k] = loc
                    if loc == j:
                        break
                    else:
                        loc = <int>next[loc][j]
    return paths

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
    For a TG with N nodes returns a NxN numpy array of
    neighbors, where the ith row lists the node IDs of the 
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
    For a TG with N nodes returns a NxN numpy array of
    neighbors, where the ith row lists the node IDs of the 
    neighbors (and -1 otherwise)
    """

    neighbors_out = np.ones((tg.node_N, tg.node_N), dtype=np.int32) * -1
    
    
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

    # Track which nodes have not been visited yet, and keep a set with all of 
    # the connected components.    
    cdef np.int32_t[:] unseen = np.ones(N, dtype=np.int32)
    cdef np.int32_t[:] comp = np.zeros(N, dtype=np.int32)
    cdef np.int32_t[:] bfs = np.zeros(N, dtype=np.int32)
    
    cdef int unseen_num = N
    cdef int bfs_num = 0
    cdef int start, current, n_i, n

    cdef int current_comp_num = 0
    
    while unseen_num > 0:
        # While there are still unvisited nodes, start from an unvisited node
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
            # Explore a new node in the connected component, adding it to the 
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
            component is given by a set of the nodes in the component.
    """

    if tg.node_N == 0:
        return []
    
    comp_array = np.ones(tg.node_N, dtype=np.int32) * -1
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
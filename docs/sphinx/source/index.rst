.. meta::
   :description: A small graph library designed to be fast and easy to extend.

.. title:: TinyGraph: a small graph library for small graphs. 

.. TinyGraph documentation master file, created by
   sphinx-quickstart on Tue Jan 12 11:59:45 2021.
   You can adapt this file completely to your liking, but it should at least
..   contain the root `toctree` directive.

TinyGraph
============================================
A small library for small graphs


version |release|.

.. image:: 	https://img.shields.io/circleci/build/github/thejonaslab/tinygraph
   :target: https://app.circleci.com/pipelines/github/thejonaslab/tinygraph

--------

TinyGraph is a :doc:`open source <license>` Python library for
*small*, *weighted*, *undirected* graphs with no self-loops. TG
supports vertex properties, edge properties, and edge weights by default. Behind the scenes data
is stored as NumPy_ arrays to make it easy to write fast graph algorithms with Numba_ and Cython_.
We interoperate closely with other graph libraries, especially NetworkX_,
to avoid reimplementing the wheel.

TinyGraph is simple to use
----------------------------
.. code-block:: python
                
      import tinygraph as tg

      vertex_n = 10 
      g = tg.TinyGraph(vertex_n)

      g[3, 4] = 1.0
      g[5, 8] = 2.0

Vertex properties and edge properties in TinyGraph have associated NumPy `dtypes`. This
strong typing improves efficiency and serialization/deserialization.

.. code-block:: python
                
      vertex_n = 10 
      g = tg.TinyGraph(vertex_n, vp_types = {'color' : np.int32,
                                             'is_special' : np.bool})

      g[3, 4] = 1.0
      g.v['color'][:] = 10
      g.v['is_special'][5] = False


.. toctree::
   :hidden:

   quickstart
   api
   authors
   license


.. _NumPy: https://numpy.org/
.. _Cython: https://cython.org/
.. _Numba: https://numba.pydata.org/
.. _NetworkX: https://networkx.org/

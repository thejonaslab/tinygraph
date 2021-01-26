# Determine which submodules get loaded

# Avoid typing tg.tinygraph.Tinygraph!
# Just tg.TinyGraph(N)
from .tinygraph import *
from . import io, algorithms, util

from .version import __version__

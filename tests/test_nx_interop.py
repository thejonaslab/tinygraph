# Test the interaction between networkx graphs and tinygraph

import numpy as np
import networkx
import tinygraph as tg

def basic_from_nx():
    "Basic test for main functionality"
    # Should look like methane except the weightings are meaningless
    ng = networkx.Graph()
    ng.add_weighted_edges_from([ \
        ('C1', 'H1', 1),   \
        ('C1', 'H2', 2),   \
        ('C1', 'H3', 0.5), \
        ('C1', 'H4', 1.8)  \
    ])
    ng.nodes['C1']['element'] = 'Carbon'
    ng.nodes['H1']['element'] = 'Hydrogen'
    ng.nodes['H2']['element'] = 'Hydrogen'
    ng.nodes['H3']['element'] = 'Hydrogen'
    # ng.nodes['H4']['element'] = 'Hydrogen' # omitted to test the exception-handling

    ng.nodes['C1']['atomic number'] = 6

    ng.edges['C1', 'H1']['bond'] = True
    ng.edges['C1', 'H2']['bond'] = True
    ng.edges['C1', 'H3']['bond'] = True
    ng.edges['C1', 'H4']['bond'] = True

    t = tg.io.tg_from_nx(ng,
                         adj_type=np.float,
                         weight_prop='weight',
                         vp_types={'element': np.object, 'atomic number': np.int},
                         ep_types={'bond': np.bool},
                         error_mode=False
    )
    ng2 = tg.io.tg_to_nx(t, weight_prop='weight')
    return ng, t, ng2

def tg_nx_tg():
    pass

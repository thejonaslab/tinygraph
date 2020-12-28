import numpy as np
import networkx
import tinygraph as tg
import pytest
import graph_test_suite
import io


suite = graph_test_suite.create_suite()

@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_binary(test_name):
    """

    """

    for g in suite[test_name]:

        outbuf = io.BytesIO()
        tg.io.to_binary(g, outbuf)
        s = outbuf.getvalue()
        inbuf = io.BytesIO(s)

        new_g = tg.io.from_binary(inbuf)
        

        assert tg.util.graph_equality(g, new_g)
        

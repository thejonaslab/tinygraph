import numpy as np
import networkx
import tinygraph as tg
import pytest
import graph_test_suite
import io

suite = graph_test_suite.get_full_suite()

@pytest.mark.parametrize("test_name", [k for k in suite.keys()])
def test_binary(test_name):
    """
    Test the conversion to and from binary.
    """

    for g in suite[test_name]:

        outbuf = io.BytesIO()
        tg.io.to_binary(g, outbuf)
        s = outbuf.getvalue()
        inbuf = io.BytesIO(s)

        new_g = tg.io.from_binary(inbuf)
        
        assert tg.util.graph_equality(g, new_g)


def test_binary_graph_props():
    g1 = tg.TinyGraph(10)
    g1.props['foo'] = 'hello'
    g1.props['bar'] = 100
    g1.props['baz'] = 100.0
    g1.props['quxx'] = [1, 2, 3]
    g1.props['quxxx'] = {'a' : 1, 'b' : 'foo', 'c': [4, 5,6]}


    outbuf = io.BytesIO()
    tg.io.to_binary(g1, outbuf)
    s = outbuf.getvalue()
    inbuf = io.BytesIO(s)

    new_g = tg.io.from_binary(inbuf)
    
    assert tg.util.graph_equality(g1, new_g)

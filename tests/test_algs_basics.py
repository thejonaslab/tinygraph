import tinygraph as tg

def test_cc_empty():
    g1 = tg.TinyGraph(0)

    assert tg.algorithms.get_connected_components(g1) == set()

def test_cc_one_comp():
    assert True

def test_cc_multi_comp():
    assert True

def test_cycles_empty():
    g4 = tg.TinyGraph(0)

    assert tg.algorithms.get_min_cyle(g4) == [] 

def test_cycles_small():
    assert True

def test_cycles_medium():
    assert True
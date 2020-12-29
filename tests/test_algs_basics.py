import tinygraph as tg

def test_cc_empty():
    g1 = tg.TinyGraph(0)

    assert tg.algorithms.get_connected_components(g1) == set()

def test_cc_one_comp():
    g2 = tg.TinyGraph(5)
    g2[0,1] = 1
    g2[0,2] = 1
    g2[2,3] = 1
    g2[3,4] = 1

    assert tg.algorithms.get_connected_components(g2) == {set(range(5)),}

def test_cc_multi_comp():
    g3 = tg.TinyGraph(6)
    g3[0,1] = 1
    g3[0,2] = 1
    g3[1,2] = 1
    g3[3,4] = 1
    g3[4,5] = 1

    assert tg.algorithms.get_connected_components(g3) == {set(range(3)),\
                                                            set(range(3,6))}

def test_cycles_empty():
    g4 = tg.TinyGraph(0)

    assert tg.algorithms.get_min_cycles(g4) == [] 

def test_cycles_small():
    g5 = tg.TinyGraph(6)
    g5[0,1] = 1
    g5[0,2] = 1
    g5[1,2] = 1
    g5[0,3] = 1
    g5[0,5] = 1
    g5[3,4] = 1
    g5[4,5] = 1

    assert tg.algorithms.get_min_cycles(g5) == [{0, 1, 2}, {0, 1, 2}, {0, 1, 2},\
                                                {0, 3, 4, 5},{0, 3, 4, 5},\
                                                {0, 3, 4, 5}]

def test_cycles_medium():
    g6 = tg.TinyGraph(9)
    g6[0,8] = 1
    g6[7,8] = 1
    g6[6,8] = 1
    g6[3,7] = 1
    g6[3,6] = 1
    g6[2,3] = 1
    g6[5,6] = 1
    g6[1,2] = 1
    g6[1,4] = 1
    g6[4,5] = 1

    assert tg.algorithms.get_min_cycles(g6) == [] 
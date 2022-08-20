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


broken_binary = b'PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00!\x00(\xfe\xbbbd\x00\x00\x00\x80\t\x00\x00\r\x00\x14\x00adjacency.npy\x01\x00\x10\x00\x80\t\x00\x00\x00\x00\x00\x00d\x00\x00\x00\x00\x00\x00\x00\x9b\xec\x17\xea\x1b\x10\xc9\xc8P\xc6P\xad\x9e\x92Z\x9c\\\xa4n\xa5\xa0n\x93f\xa2\xae\xa3\xa0\x9e\x96_TR\x94\x98\x17\x9f_\x94\x92\n\x12wK\xcc)N\x05\x8a\x17g$\x16\xa4\x02\xf9\x1aF&:\nF&\x9a:\n\xb5\nd\x02.\x060h\xb0\xa7-\x1e\xb5c\xd4\x8eQ;F\xed\x18\xb5c\xd4\x8eQ;F\xed\x18<v\x00\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00!\x00K\xb4\x8d\xc2I\x00\x00\x00\x98\x00\x00\x00\x15\x00\x14\x00vp_shift_observed.npy\x01\x00\x10\x00\x98\x00\x00\x00\x00\x00\x00\x00I\x00\x00\x00\x00\x00\x00\x00\x9b\xec\x17\xea\x1b\x10\xc9\xc8P\xc6P\xad\x9e\x92Z\x9c\\\xa4n\xa5\xa0^\x93d\xa8\xae\xa3\xa0\x9e\x96_TR\x94\x98\x17\x9f_\x94\x92\n\x12wK\xcc)N\x05\x8a\x17g$\x16\xa4\x02\xf9\x1aF&:\x9a:\n\xb5\n\xe4\x03.\x06F\xec\x00\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xe7:\x92\xc3\x99\x00\x00\x00\xe0\x00\x00\x00\x12\x00\x14\x00vp_shift_value.npy\x01\x00\x10\x00\xe0\x00\x00\x00\x00\x00\x00\x00\x99\x00\x00\x00\x00\x00\x00\x00\x9b\xec\x17\xea\x1b\x10\xc9\xc8P\xc6P\xad\x9e\x92Z\x9c\\\xa4n\xa5\xa0n\x93f\xa2\xae\xa3\xa0\x9e\x96_TR\x94\x98\x17\x9f_\x94\x92\n\x12wK\xcc)N\x05\x8a\x17g$\x16\xa4\x02\xf9\x1aF&:\x9a:\n\xb5\n\xe4\x03.\x06 8\xec\xfb\xd61\xe1\xbf\x84S\xe1j+\xa75\x16\x02\xce\\\xe9,\xce\xa9Y\xae\xce\xb3]V9\xc6\xb408\x7f\xb7\xfb\xe7\xd4n\xc6\xea\xdc\xbe\xe7\x8fSD\xa4\xaa\x83\xf9fm0\xb6^\xaa\x04\xc6\x17\xd4j\xeda8\xb6\xff\x99\x83\xfbU\x06\xc7M\x9b^;\xf0>z\xe1\x00\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xec\xa5\xff\xa9\x98\x00\x00\x00\xe0\x00\x00\x00\x18\x00\x14\x00vp_shift_uncertainty.npy\x01\x00\x10\x00\xe0\x00\x00\x00\x00\x00\x00\x00\x98\x00\x00\x00\x00\x00\x00\x00\x9b\xec\x17\xea\x1b\x10\xc9\xc8P\xc6P\xad\x9e\x92Z\x9c\\\xa4n\xa5\xa0n\x93f\xa2\xae\xa3\xa0\x9e\x96_TR\x94\x98\x17\x9f_\x94\x92\n\x12wK\xcc)N\x05\x8a\x17g$\x16\xa4\x02\xf9\x1aF&:\x9a:\n\xb5\n\xe4\x03.\x06 \xb8\xce\x93n\xff\xbfB\xce\xfe#\xd3=\xbb\xc0\x12\t{\x19\xb9v\xbb\x99\xdf4\xed3&\xcd\xb1\xab\x9b\x96m\xb7\xe0V\xbb\xdd\xf4\x87)vZ\xaa\xa2v\x13\xcf\xfe\xb2\xab\xfa2\x17\x8c9\xb6\xf3\x81\xb1\xdcD\x198\x9e%ln\xc7\xe5\xf5\xca\xf6\xbf\xbc\x82\xddt\xcd\x1f\xb6\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xa4\x0b\x05\xc4V\x00\x00\x00\x00\x02\x00\x00\x10\x00\x14\x00vp_shift_nuc.npy\x01\x00\x10\x00\x00\x02\x00\x00\x00\x00\x00\x00V\x00\x00\x00\x00\x00\x00\x00\x9b\xec\x17\xea\x1b\x10\xc9\xc8P\xc6P\xad\x9e\x92Z\x9c\\\xa4n\xa5\xa0n\x13j\xa2\xae\xa3\xa0\x9e\x96_TR\x94\x98\x17\x9f_\x94\x92\n\x12wK\xcc)N\x05\x8a\x17g$\x16\xa4\x02\xf9\x1aF&:\x9a:\n\xb5\n\xe4\x03.\x064`\x08\xc4\xc6@\xec<\x84\xf8\x1eh\xee\x1fJ|\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xb5\xd5HkR\x00\x00\x00\xc0\x02\x00\x00\x18\x00\x14\x00ep_coupling_observed.npy\x01\x00\x10\x00\xc0\x02\x00\x00\x00\x00\x00\x00R\x00\x00\x00\x00\x00\x00\x00\x9b\xec\x17\xea\x1b\x10\xc9\xc8P\xc6P\xad\x9e\x92Z\x9c\\\xa4n\xa5\xa0^\x93d\xa8\xae\xa3\xa0\x9e\x96_TR\x94\x98\x17\x9f_\x94\x92\n\x12wK\xcc)N\x05\x8a\x17g$\x16\xa4\x02\xf9\x1aF&:\nF&\x9a:\n\xb5\nd\x02.\x06F\x1c`TbT\x82\x08\t\x00PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00!\x00\x8fW/\r\xb5\x06\x00\x00\x80\t\x00\x00\x15\x00\x14\x00ep_coupling_value.npy\x01\x00\x10\x00\x80\t\x00\x00\x00\x00\x00\x00\xb5\x06\x00\x00\x00\x00\x00\x00\x9d\x96\xffW\xd4u\x16\xc6\xf1\x04K\xe0\x89\xce\xba\x0b\xa4k\x81yd$p\xa9Dq\x81\xf9\xdc;3\xa5\xa6\x8b"\x99\x98E\n#B&\x91\x83\xe0Y\xb5\xf8\xe2\x17\x14\xc4\xf5\x88\xa8h~\x9d\xc50\xd7\x03I\x82:0\x1fX\xdbp\xf5xd\xd9\\\xcc\xb2t\xc5X\x8fZ\x16\x9btt\xd3\xe55\x7f\xc2\xceo3?\xdc{\xcf\xf3~=\xcf3\xd53^II}u\x88_\x91\xdfJ\xcb\xc2\xec\x02\xa7\xcb\x92\x18iI^\x14o\x89\x8d\xb4,\xcaw-se\xbe=?\xdf\xb50\x9b\xdf\'g.)\xc8\x1e\xfc\xbd 7\xf3\x9d\xec\xc1\xefc\x9f\x8f\x8f\x8d|>>:6\xf2\xdd\xc8\xff\xf3\x13\xec7\xf8i\xe8\xbdo\xed\xc9x(\x9e\xc0\xc7u\xd9\x92:\tO\xef\xd2\xba\xa2s\xf6y/\\\x94{z\xdc\xa8\xee<\xa1\x81\xdef\x9d\xb3e\x83\xd1\x9f\xf3\x88vM3\xf4\xd8\xa5\x17ue\xfd(\xfdbX\x86\xae\xb8\xdeg\x1c\x0e\xcd\x17\x8d(\x90#\xc9\x97t\xb7\xe7#\x91\x9f\xe3m\xa15\xd5\x06\xb3\xd9\xe19;\xda\xfeB\xf1(\xfb\xed\x91E\xe6\xf97\x17\xca\xcb]\xa3\xcc\xc5/F\xdb\xefe.U\xcf\xb6\xc5\xe2\xc9\xeb6f.\x8d\x12\xc7\xc7\x8f:\x02\xac\x1f\x98\xd2\x14\xd8\xfe\xaf\xce\x1b\xe6\x9919\xe6\x8a\xfan\xb3kU\x93\xe9lm2\xf36\xb7\xea\xd05I\xb6\x0f#z\xe4aX\x8b\xf8\xee\x1e\x9c\xcd\x8e/\xc6\xbd\xd9^~\xe6w\xf6\t\xb9\x8dm\xb3\xceN\xd2g\\W\xbd\x05;\xfa\x8d\xec9QjM\xcbS\xb7\xb5X\x823\x93\x8d[a\xbfp\x14\\}\xd4\x91U\x13\xa2U\xc3\xfe\xa9=\xddK\xd591K[\xd2n\xe8\xf8\x9aR\x9d\xf0e\xba,\xff\xd5[\xf2\xfd\xf0`E\x13\xeef6;&Mi5\xfa^\x8b\xb6\x8duN\xb1\'L4\xcc\x99\x07\xaad\xe8\x1f2\xe4\xd8\x81\x14\xe9\x9eq\xddx\xf2\xdd\x14\xc3\xed\xff7\x95\xdcg4\xe3\xc7\x00\xc7\xb9o\x82\x1d\r\xcb\xa3\xf5d\xdc>\r]\x9b\xa0\xd5\xb5\xb3lk\x17\xf4\xea\xc0o-b\x1a\xf1\x82\xdeh\xc2\xdd\xcc\xf6\xed\xf0n\xb7\x7f\x17\x15\xa2]\xd3w\xaaY\xec\xb67\x8d\x9a\xe1\xed/\xccj\xf3\x8ei\xd0\x86S\xb7\xa5\xef\xa0\xbd\xfd\xafw7\xb6\xff0\xec\x8a\xf8/Yc\xee\x99z@\x8a?-\x1c\xd4\xfc\xaeQ\x1eR-\xe19\xcdz\xf1\xc6\x05\xcd\xf9\xfbt\xdf[\xa27\x9ap7\xb3\xd9\x91v\xfc\x1d\xfb@B\x99TV\x0fo\xbb\xf6\xdc^\xbb\xff\xb4=z\xb6h\xb6\xd5\xee*i\x9b\xb2I5\xf8\xe3[\x12\x16}\xd0\x98\xe2\x1d\xa3\xc9\x0f\xe3\xa5\xe8H\x80\xac\x7f\xe9\x81qfH\xb3F\x9d\xb4\xc8\xb3\xa9!\xf2r\x9e\xc7\xc7\to\x89\xdeh\xc2\xdd\xccf\xc7\xde\x1f\xfe\xac7\x8d|\xcd\xed4\xcd\x11!\x97\xe4\x83\x8eL\x9d\xf9I\x9d\xac\xfbp\xb3T5_\x96\xac\xa8\xe2\xf6\x80\xc7v\xb7G\x1d\xaa\x95J\xd7!Y\xff\xfd&y\xe3/\xa7e o\x96>RZ\xa2\xbb\x1a\xf7\x08\x0c\xc2\to\x89\xdeh\xc2\xdd\xccfG\xf8\xba\n\x99:\xabT\xd6\xc4l\x95\xec\xf4r\x89\xb8\xbc\xc1L\xa9\x8b\xd1\xfe\xf2`}\xfd\xdb_j\x8b\xe7Y-?\xfe\xc0~a\xb6\x9f\xc3\xff\xf7C\x1c\xae\x94?\xd9\xe6\xfe\xe3\x8f\xf2V\xf8j){\x7f\xaf\x8fo\x18\x84\x13\xde\x12\xbd\xd1\x84\xbb\x99\xcd\x8e\xc9_o\xd2\xf8\xa4z{\xc6\xd3-\xde\xbc\xb8\x15\xde\xc4\xc9\xefi\xf9\xa48\x1d\x97\x9f\xa8\xa9\xbd[\xf47\xc1n\xd9~\xf43\xe9\x0f\xba&1\xf3\x83\x1c\xbb\xc2>\x93\xb0\xed\xa7\xa4r\xc3Y\xc5;\xf0\r\x83p\xc2[\xa27\x9ap7\xb3\xd9\x91\xe3\x1fh\xbaZ\x0f\xd9\xb7~\x97`\x9c[_+?/\n\x93\xad\xa9\x07\xe4\xda\xd1\x0br\xfdp\xa5D$\xad\x97\xfe\x1d[d\xc2\xf9\x9br\xb8.\xc4Q1\xfb\xb4:*n\x08\xbe\xc4;\xf0\r\x83p\xc2[\xa27\x9ap7\xb3\xd9\xf1\x9f\x02\xb7\xbd\xfb\xd5:\xe3\x89\x1f\x9d\xc6\xca\xa0H\xa9\xdf\x9f\'};\x9bd\xff\xaf=\xd2\x1e\xfe\x9eX?Y-}\xab6\x8bc\xc1WZy3\xc8a\x8b\xa9\x15<\x8f/\xf1\x0e|\xc3 \x9c\xf0\x96\xe8\x8d&\xdc\xcdlv\xacHH0\xa6\x97\xe5\xda\xde\xae\x0f\xd5\xd4\xb2\x05\xe2\xdd\xe8\x16\xbf$\xb7\x04\x9c\x9b$#\xceO\x15\x8b\xb3GO\xe5\x7f$\xd9cketk\x90\x83<\xc1\xf3\xf8\x12\xef\xc07\x0c\xc2\to\x89\xdeh\xc2\xdd\xccf\xc7\x85\x814-_\x1co\x9b7\xdca\xbb\xe2\x9e\xab\xd5\xb9w\xf5|\xebQ\xad\xf9\xf4\xa8\xfe\xbbs\x83\xb50\xf4\x81\x11P\x18)\xd7\x1b\x9f\x12\xb2\x8a<\xc1\xf3\xf8\x12\xef\xc07\x0c\xc2\to\x89\xdeh\xc2\xdd\xccf\xc7%wq\xc7\xf8\xc4\xf2\xd6+\xcb\x87h\x91\xf3i\xef\x91\xcfG&\xa7\xaf\xab06\x8d\x8c0cnGYG\x1f<a\xf5\xac~B\xc8A\xb2\x8a<\xc1\xf3\xf8\x12\xef\xc07\x0c\xc2\to\x89\xdeh\xc2\xdd\xccf\xc7s\x13c\x8d\xcd{/[O\x05O\xf5\x0e\xec~\xc3;\xa7ih[\xf5\xf1\x0630b\x9aqg\xbf\x9f\x1ci\xb9g\x90\xb1\xe4 YE\x9e\xe0y|\x89w\xe0\x1b\x06\xe1\x84\xb7Do4\xe1nf\xb3\xa3w\xce\xb6\x8e\x83?\xed\xf1^<|\xac\xad\xf1\xfd\x13\xde\'K\xc2d\xdf@\x85\xb5i\xdf*i|j\xa6\x90\xdfd,9HV\x91\'x\x1e_\xe2\x1d\xf8\x86A8\xe1-\xd1\x1bM\xb8\x9b\xd9\xec\xd0\xd2\xd7\xbd\xce\xd9\xfd\xad9\xe3\xbfN\n\xb8/r\xb2\xb0\xc7\x9a\xb9\xb8T^\xa9zM\xe8\x06\xf2\x9b\x8c%\x07\xc9*\xf2\x04\xcf\xe3K\xbc\x03\xdf0\x08\'\xbc%z\xa3\tw3\x9b\x1d\x91\xffuv\xec\xbe\x9f\xd5\xf1\xd2\xd5\x112\xb7k\x9b\xa4\xd9+\xa4\xb3\xb7D\xe8\x1d_7\x0c\xe67\x19K\x0e\x92U\xe4\t\x9e\xc7\x97x\x07\xbea\x10NxK\xf4F\x13\xeef6;v~\x93\xdbq:%V\x92\xa4BJ\xaa\xca\xe4\xf1\x1d._\xa7\xd1;t\x03\xf9M\xc6\x92\x83d\x15y\x82\xe7\xf1%\xde\x81o\x18\x84\x13\xde\x12\xbd\xd1\x84\xbb\x99\xcd\x0ewz\x9c\xa4\x86\xef\x92\x84\xe6\x8d\xb2,n\x8d\xaf/\xe94z\x87n \xbf\xc9Xr\x90\xac"O\xf0<\xbe\xc4;\xf0\r\x83p\xc2[\xa27\x9ap7\xb3\xd9\xb1v\xbe\xc5\x18\x97xG\xeb\xbf]\'t1}I\xa7\xd1;t\x03\xf9M\xc6\x92\x83d\x15y\x82\xe7\xf1%\xde\x81o\x18\x84\x13\xde\x12\xbd\xd1\x84\xbb\x99\xed\xeb\xda\x8d52\xef\xa7;J\xcf\xd3\xc5\xf4%\x9dF\xef\xd0\r\xe47\x19K\x0e\x92U\xe4\t\x9e\xc7\x97x\x07\xbea\x10NxK\xf4F\x13\xeef6;\xb6$\xdcR\xfeC\xd0\xf3t1}I\xa7\xd1;t\x03\xf9M\xc6\x92\x83d\x15y\x82\xe7\xf1%\xde\x81o\x18\x84\x13\xde\x12\xbd\xd1\x84\xbb\x99\xcd\x8e\xff\x01PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xb8\x90U\xa1\x88\x06\x00\x00\x80\t\x00\x00\x1b\x00\x14\x00ep_coupling_uncertainty.npy\x01\x00\x10\x00\x80\t\x00\x00\x00\x00\x00\x00\x88\x06\x00\x00\x00\x00\x00\x00\x9d\x96\xe9S\x15d\x18\xc5E\x14\x10Hi\x08\xd3\xc1\xe5\xba\x14\x12\x90@\xa2\xe2\xf8\x9e\x1734\x13QS\xd4\xa4\x04\xc2\xabH\x85\x89\xe5\x92\x88((\x86\xb9\x00\x92[n#\x86\x83@\xa4Raji\xcb(Xji\x8b\x98[\x19ci(J\x96\xdb\xc4\xcf?\xa1\xfb\xed\xde\x0f\xcf\xf3\xccy\x7f\xe7\x9c[\x18\x1b7b\xd4\x0b.-f\xb5\x98\x170\xd9939=`\x80#`\xe0\x94>\x01\xc1\x8e\x80)\xd3\xd3\xdfHOJK\x98\x9e>\xd9\xc9\xefC\x92^\x9d\xe9l\xfe}fJ\xd2\xeb\xce\xe6\xef\xbd\xc2\xfb\x04;\xc2\xfb\x04\x06;\xe6;\xfe\xe7\xc7\xb3E\xf3\xe7y\x8f\x156h\xc2\x00\xfb\xf8\x95&%,\x99c\x83\x12\xe3\xec\x1a\xf7\x1b\xf6\xfc0_\xdb5\xc6\xd7\x1e\x8bK\xb5\x9f\x87&\xd9\xc9U\xbevp\xe9\xefj\xf4*\xb0\xe3z\xcf\xb5;\xdcV\xd8\xec\xa7{\xdb\xca\xc7\x16\xd8\xca\xb29\xb6\xfd\xcd4;8\xe6=[4\xba\x9d\xbd\x91Wf\xbf\x9d\xefb\x99\xcd\x8e\x82\xb0\xbf\xcck\xcf\xce\xd1\xa6\xc4\x85\xca\xcc\x8cT\xd4\xf1Uz\xe2`\x9aL\xfe<\xed\xde\x92\xa8\xe5i\xd7M\xfd\xba%\xa6\xc0\xc7O\x85\xb7\xcb\x95{\xc0\xa9\x01%\xa3T\xec\x1a\xa1\xd2\x03\x15&\xed\xfeU\x13\xba\xaf\xb5\xf6\xfe\xb8\xcc\xde|\xa7\xc1^\xdc\x7fZW\xce\x9f\x14w3\x9b\x1d+S\'\xea\xa1#a\xeaV\x9e\xa0\x1f\x1c\xdd\xed\xc3\x89SU\xe3\xee\xa6/\xfd\xd7\xea\xd8sgLf^\x96\x06^\x98\xab\x11\xab\x8d\xca\x83\x9fR\xf4\'\x9fiG\xf2\xa36\xa5v\x85\x8e\xde\x1a\xaf\xd9\xa3\x83m\xcf\xdc\t\xfa(\xc5\xa9\x1bi\x1b5\xa8\xc1\xfd\x81&\xdc\xcdlv\xcc\xaa]\xa0\x19\x13\xbb\xda]s\x93\xf5k\x8fmj\xfaw\x9fnn~J\xc5a\x83t\xf8Zg\x15T\xacQS\xdf,\xd9\xa9\xb2c}34f}\xa1\xfeL\xba\xacT\xafL[\xb7\xca\xdbn\x18z\xd6\xc6O\xab\xb0\xdb\xed\x19\x1dL\xcby\xa07\x9ap7\xb3\xd9\xb1\xe7R\x85\xe9\xee\xb9Z}\xf2V*\xe6\xe3=&09\xdf\xf4}\xab\xd8\x94\xc4\xe7\x9b\xe8\xc5\xdf\xeb\xcf\xa2\xe1\x9a1<K\x15%5\xba\xbf\xb4sT\xee\xdbwuq\xd7q\xf9\x94\x17\xea\xeb\x8eu\xe6\xee\xd6y\xe6RH\x8e\xd9P\xf9\x89xK\xf4F\x13\xeef6;\xf2\xce,\xd2\x84\xa9KT\x1c\xfd\x93i\x13y\xc8\xfcq\xb0\xd2\xfc\xbb\xc1\x9a_2\x17it\x88\x9b\x1dS\x13k\x7fx8\xda\xfa\xd5v\xb0-<n)0\xea\xb2j\x86\\W\xfb0_\xad\x89>a\x06\'\x8eW\xd7\xc6u\x06NxK\xf4F\x13\xeef6;\x02V\xadWN\xe7\xb7\xb4~FW\x95\x9d:\xa2\x8f\xf7<\xab8\xff\xd3\x8a+\xf1\xb4\xa1\x1bv\xc8\xf3\x91\xab\xea\xb4e\xb3f\\\r\xb7\x8e#\xad\xed\xe0\xbd\xde\xb6\xaf3_C\x97]5q\xc9k\xec\xf9\xaaX\xc1 \x9c\xf0\x96\xe8\x8d&\xdc\xcdlv\x1c\xfbq\xa4\x1a\xde\x0fS\xf4\xc9`yx?\xa3\xd4\xc0ij\n\xaf\xd3X7\xa7.\xa4\xdcS\xab\xc8\xce\xb6`x\xbd9\x94\xec\xa5\xd0;~\xaa\xafm\x1d\xf5\xd5\x96\x18\x85.\x0c\xd7 \x05\t\xbea\x10NxK\xf4F\x13\xeef6;\xc2\xd3W\x99~\xd3\xb6\x98S\xdb\xe3\xcd\xd9\x97\xbePjd\xf3\r\x9f\xee\xd4\xf2jo\xfb\xc1\x8eB{y\xd0q\xf5\xf3kkk/\xb5\xb3\xb9\x17\xba\xcb\xff\xfdj97{\x99.\x1d\xc6\x19\xbc\x03\xdf0\x08\'\xbc%z\xa3\tw3\x9b\x1d[O<oz\xaf\xab2\'B\xfeRMV\xbbf&\xbb\xd8\xb8\xfan\xb6l\xfe\xdf\xaa\xa9>\xac\xfe>\xfb\xf5\xfa\x8b\xbb\x95\xdd\xb8T\xfd\x8f\xb8h\xd6\x88qfD\xf1Z\x83/\xf1\x0e|\xc3 \x9c\xf0\x96\xe8\x8d&\xdc\xcdlv\x04\xf7/5\x87\x97=j\xff\xa9\xeea\x8b\x8e\xbb\xda\'\x97\xfd\xa4\xaa\xe2C*-_\xaa\x0e\x1fe\xa8\xba [\x9b\xfc2L\xcf\xa8\xb7\xcd+ug\xcd\xeaV\x93\x0c\x9e\xc7\x97x\x07\xbea\x10NxK\xf4F\x13\xeef6;\xea\xbfKW\xfcb\xd7\xa8\xb2\x88H\xbb\xa2[\x8eb\xcf\xe5h\\\xe36e\xd4\x17\xcb\xc3\xf5\x03U\xa6N4\xf9\xef\xba\x99\x8e\xc3\xee\x0c\xfc5\xaf\xd4\x90\'x\x1e_\xe2\x1d\xf8\x86A8\xe1-\xd1\x1bM\xb8\x9b\xd9\xecx\xf7\xdcP\xbdv\xc7\xd5\x9eH\xf7\xb1\xe7\xd6\x8e\xd5\xd96\xd3m\x97s;U~\xf4\x94\xa6\xb9\x1e4\r\xad\xeb\xcc\xec%\xb7\xcd\xed\xc6\xa0\x07YE\x9e\xe0y|\x89w\xe0\x1b\x06\xe1\x84\xb7Do4\xe1nf\xb3#\xc3t\xd2]\xcfL\xe5\xa6$)\xe7\xe7X3\xb4\xe7CJ\xb0\tr\xd9\x1b\xaf\xfc)\xb7\xcc\xd1\xe9\x9f\x9b\xde\xff\xfcf\xc8A\xb2\x8a<\xc1\xf3\xf8\x12\xef\xc07\x0c\xc2\to\x89\xdeh\xc2\xdd\xccf\xc7\xfd\xc0\xed\xaa9\x90\xa5\xb6\xb3Fi\xee7\'M\xfb]\x81\xca\r\xf6\xd7\xcb\x9fy\xebb\xe5#Z\xd9\xd2Ed,9HV\x91\'x\x1e_\xe2\x1d\xf8\x86A8\xe1-\xd1\x1bM\xb8\x9b\xd9\x0frwJ\x90\x9e\x8c\x1c"\xff\x8d\xcb\xb5\xdc\xf3\x8a\xf9\xe2\xca7f{H\x83\xc9\xfe\xb2\x9f\xaazt\x14\xf9M\xc6\x92\x83d\x15y\x82\xe7\xf1%\xde\x81o\x18\x84\x13\xde\x12\xbd\xd1\x84\xbb\x99\xcd\x0e\x0f\x9f\xb5fd\xc5d\x15\xb9\xa7\xab\xe4z+uJ\xa80\xb3\xc7\x0fSED\x84\xe8\x06\xf2\x9b\x8c%\x07\xc9*\xf2\x04\xcf\xe3K\xbc\x03\xdf0\x08\'\xbc%z\xa3\tw3\x9b\x1d##\x16\x9a\xe8\x96\xdbL\xd3\xd4@\xb9\xc4D)$\xfe\xa8\xd9\xba\xc8[\xf4\x0e\xdd@~\x93\xb1\xe4 YE\x9e\xe0y|\x89w\xe0\x1b\x06\xe1\x84\xb7Do4\xe1nf\xb3#%\xb4\x8dNWf\xeb\xd3\xfd1J\xfc\xcdK\xe7\xcb\x9f\x10\x9dF\xef\xd0\r\xe47\x19K\x0e\x92U\xe4\t\x9e\xc7\x97x\x07\xbea\x10NxK\xf4F\x13\xeef6;>\x0c(R\xd0\xee7\xd4\xb1W?9nN\x12}I\xa7\xd1;t\x03\xf9M\xc6\x92\x83d\x15y\x82\xe7\xf1%\xde\x81o\x18\x84\x13\xde\x12\xbd\xd1\x84\xbb\x99\xcd\x8e\xef\xde\\i\x0e\xb8\x87\x1a\x87\x9f\xab\xa1\x8b\xe9K:\x8d\xde\xa1\x1b\xc8o2\x96\x1c$\xab\xc8\x13<\x8f/\xf1\x0e|\xc3 \x9c\xf0\x96\xe8\x8d&\xdc\xcdlv\\\xeb~m\xe0\xbd\xcaE\x86\x9e\xa7\x8b\xe9K:\x8d\xde\xa1\x1b\xc8o2\x96\x1c$\xab\xc8\x13<\x8f/\xf1\x0e|\xc3 \x9c\xf0\x96\xe8\x8d&\xdc\xcdlvx\x0e\xd8h\xf8\x0fA\xcf\xd3\xc5\xf4%\x9dF\xef\xd0\r\xe47\x19K\x0e\x92U\xe4\t\x9e\xc7\x97x\x07\xbea\x10NxK\xf4F\x13\xeef6;\xfe\x03PK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\x00\x00!\x00(\xfe\xbbbd\x00\x00\x00\x80\t\x00\x00\r\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x00\x00\x00\x00adjacency.npyPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\x00\x00!\x00K\xb4\x8d\xc2I\x00\x00\x00\x98\x00\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\xa3\x00\x00\x00vp_shift_observed.npyPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xe7:\x92\xc3\x99\x00\x00\x00\xe0\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x013\x01\x00\x00vp_shift_value.npyPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xec\xa5\xff\xa9\x98\x00\x00\x00\xe0\x00\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x10\x02\x00\x00vp_shift_uncertainty.npyPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xa4\x0b\x05\xc4V\x00\x00\x00\x00\x02\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\xf2\x02\x00\x00vp_shift_nuc.npyPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xb5\xd5HkR\x00\x00\x00\xc0\x02\x00\x00\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01\x8a\x03\x00\x00ep_coupling_observed.npyPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\x00\x00!\x00\x8fW/\r\xb5\x06\x00\x00\x80\t\x00\x00\x15\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01&\x04\x00\x00ep_coupling_value.npyPK\x01\x02\x14\x03\x14\x00\x00\x00\x08\x00\x00\x00!\x00\xb8\x90U\xa1\x88\x06\x00\x00\x80\t\x00\x00\x1b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x01"\x0b\x00\x00ep_coupling_uncertainty.npyPK\x05\x06\x00\x00\x00\x00\x08\x00\x08\x00\x14\x02\x00\x00\xf7\x11\x00\x00\x00\x00'    


def test_read_broken_bin():
    # deserializing this graph was broken, leaving
    # here to make sure it works
    g = tg.io.from_binary(io.BytesIO(broken_binary))


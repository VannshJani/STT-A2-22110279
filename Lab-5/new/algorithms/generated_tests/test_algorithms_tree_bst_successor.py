# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.tree.bst.successor as module_0


@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = "\nIn graph theory, a component, sometimes called a connected component,\nof an undirected graph is a subgraph in which any\ntwo vertices are connected to each other by paths.\n\nExample:\n\n\n    1                3------------7\n    |\n    |\n    2--------4\n    |        |\n    |        |              output = 2\n    6--------5\n\n"
    module_0.successor(str_0, str_0)


def test_case_1():
    bool_0 = False
    var_0 = module_0.successor(bool_0, bool_0)

# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.tree.traversal.inorder as module_0


def test_case_0():
    float_0 = 3535.82
    node_0 = module_0.Node(float_0, right=float_0)


@pytest.mark.xfail(strict=True)
def test_case_1():
    bytes_0 = b"\xec\n\t\xa7\xa2"
    module_0.inorder(bytes_0)


def test_case_2():
    none_type_0 = None
    list_0 = module_0.inorder(none_type_0)


def test_case_3():
    none_type_0 = None
    list_0 = module_0.inorder_rec(none_type_0)


@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = "__main__"
    module_0.inorder_rec(str_0)


@pytest.mark.xfail(strict=True)
def test_case_5():
    bytes_0 = b"\x03"
    module_0.inorder_rec(bytes_0, bytes_0)


@pytest.mark.xfail(strict=True)
def test_case_6():
    bytes_0 = b"\x9e\x95Is\x7f\xa2\xa4q$o\xa1\x19vVp\x9b4\xbf"
    node_0 = module_0.Node(bytes_0, bytes_0)
    module_0.inorder(node_0)


def test_case_7():
    int_0 = 6
    node_0 = module_0.Node(int_0)
    list_0 = module_0.inorder(node_0)


@pytest.mark.xfail(strict=True)
def test_case_8():
    bool_0 = True
    node_0 = module_0.Node(bool_0)
    list_0 = module_0.inorder_rec(node_0)
    list_1 = module_0.inorder(node_0)
    none_type_0 = None
    list_2 = module_0.inorder_rec(none_type_0)
    list_3 = module_0.inorder_rec(none_type_0)
    none_type_1 = None
    node_1 = module_0.Node(bool_0, list_3)
    list_4 = module_0.inorder(node_0)
    list_5 = module_0.inorder_rec(none_type_0)
    list_6 = module_0.inorder_rec(none_type_0, list_1)
    list_7 = module_0.inorder(none_type_1)
    node_2 = module_0.Node(bool_0, node_0, node_0)
    list_8 = module_0.inorder(node_1)
    node_3 = module_0.Node(none_type_0, right=node_2)
    list_9 = module_0.inorder(node_1)
    bool_1 = True
    list_10 = module_0.inorder(node_0)
    list_11 = module_0.inorder(none_type_1)
    list_12 = module_0.inorder_rec(none_type_1, none_type_1)
    node_4 = module_0.Node(list_6, none_type_0)
    bool_2 = True
    node_5 = module_0.Node(bool_2, right=node_2)
    list_13 = module_0.inorder_rec(node_3)
    list_14 = module_0.inorder(node_3)
    module_0.inorder(bool_1)

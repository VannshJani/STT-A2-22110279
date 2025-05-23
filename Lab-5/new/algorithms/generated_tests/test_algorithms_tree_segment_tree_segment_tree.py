# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.tree.segment_tree.segment_tree as module_0


@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = "2Z"
    module_0.SegmentTree(str_0, str_0)


def test_case_1():
    bool_0 = False
    list_0 = [bool_0]
    segment_tree_0 = module_0.SegmentTree(list_0, bool_0)
    assert (
        f"{type(segment_tree_0).__module__}.{type(segment_tree_0).__qualname__}"
        == "algorithms.tree.segment_tree.segment_tree.SegmentTree"
    )
    assert segment_tree_0.segment == [False, 0, 0, 0, 0, 0]
    assert segment_tree_0.arr == [False]
    assert segment_tree_0.fn is False
    var_0 = segment_tree_0.query(bool_0, bool_0)
    assert var_0 is False


@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    set_0 = set()
    segment_tree_0 = module_0.SegmentTree(set_0, none_type_0)
    assert (
        f"{type(segment_tree_0).__module__}.{type(segment_tree_0).__qualname__}"
        == "algorithms.tree.segment_tree.segment_tree.SegmentTree"
    )
    assert segment_tree_0.segment == [0, 0, 0]
    assert segment_tree_0.arr == {*()}
    assert segment_tree_0.fn is None
    segment_tree_0.query(none_type_0, none_type_0)


@pytest.mark.xfail(strict=True)
def test_case_3():
    bool_0 = True
    list_0 = [bool_0]
    int_0 = -2617
    segment_tree_0 = module_0.SegmentTree(list_0, int_0)
    assert (
        f"{type(segment_tree_0).__module__}.{type(segment_tree_0).__qualname__}"
        == "algorithms.tree.segment_tree.segment_tree.SegmentTree"
    )
    assert segment_tree_0.segment == [True, 0, 0, 0, 0, 0]
    assert segment_tree_0.arr == [True]
    assert segment_tree_0.fn == -2617
    var_0 = segment_tree_0.query(int_0, int_0)
    var_0.query(int_0, int_0)


@pytest.mark.xfail(strict=True)
def test_case_4():
    bool_0 = False
    bool_1 = True
    bool_2 = False
    list_0 = [bool_2]
    segment_tree_0 = module_0.SegmentTree(list_0, list_0)
    assert (
        f"{type(segment_tree_0).__module__}.{type(segment_tree_0).__qualname__}"
        == "algorithms.tree.segment_tree.segment_tree.SegmentTree"
    )
    assert segment_tree_0.segment == [False, 0, 0, 0, 0, 0]
    assert segment_tree_0.arr == [False]
    assert segment_tree_0.fn == [False]
    var_0 = segment_tree_0.query(bool_1, bool_1)
    var_0.make_tree(bool_0, bool_0, bool_0)


@pytest.mark.xfail(strict=True)
def test_case_5():
    bool_0 = True
    list_0 = [bool_0]
    int_0 = -2617
    dict_0 = {}
    segment_tree_0 = module_0.SegmentTree(dict_0, int_0)
    assert (
        f"{type(segment_tree_0).__module__}.{type(segment_tree_0).__qualname__}"
        == "algorithms.tree.segment_tree.segment_tree.SegmentTree"
    )
    assert segment_tree_0.segment == [0, 0, 0]
    assert segment_tree_0.arr == {}
    assert segment_tree_0.fn == -2617
    var_0 = segment_tree_0.query(int_0, bool_0)
    var_0.query(list_0, int_0)

# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.dfs.pacific_atlantic as module_0


@pytest.mark.xfail(strict=True)
def test_case_0():
    bytes_0 = b"\xf4\x13\xed\x95>T\xd3"
    module_0.pacific_atlantic(bytes_0)


def test_case_1():
    tuple_0 = ()
    var_0 = module_0.pacific_atlantic(tuple_0)


@pytest.mark.xfail(strict=True)
def test_case_2():
    str_0 = "\n    Returns the Identity matrix of size n x n\n    Time Complexity: O(n^2)\n    "
    module_0.pacific_atlantic(str_0)


@pytest.mark.xfail(strict=True)
def test_case_3():
    bytes_0 = b"F\xd1\xfeXf\xbf\x88\xad\xafd"
    module_0.dfs(bytes_0, bytes_0, bytes_0, bytes_0, bytes_0)


def test_case_4():
    bytes_0 = b"0"
    list_0 = [bytes_0]
    var_0 = module_0.pacific_atlantic(list_0)


def test_case_5():
    bytes_0 = b"L\x8d"
    list_0 = [bytes_0, bytes_0]
    var_0 = module_0.pacific_atlantic(list_0)


@pytest.mark.xfail(strict=True)
def test_case_6():
    tuple_0 = ()
    list_0 = [tuple_0]
    var_0 = module_0.pacific_atlantic(list_0)
    str_0 = "l`*nA"
    tuple_1 = (str_0, str_0)
    module_0.pacific_atlantic(tuple_1)


def test_case_7():
    bytes_0 = b"\xa3\xac"
    bytes_1 = b"sjf\xd0\xd0\x01Oi\xa2\x11\r"
    tuple_0 = (bytes_0, bytes_1)
    var_0 = module_0.pacific_atlantic(tuple_0)


def test_case_8():
    bytes_0 = b"X\xac"
    bytes_1 = b"sjf\xd0\xd0\x01Oi\xa2\x11\r"
    tuple_0 = (bytes_0, bytes_1)
    var_0 = module_0.pacific_atlantic(tuple_0)

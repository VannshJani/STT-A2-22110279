# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.strings.add_binary as module_0


def test_case_0():
    str_0 = "7iM;m'3+O\x0c"
    var_0 = module_0.add_binary(str_0, str_0)
    assert var_0 == "1011011100"
    var_1 = module_0.add_binary(str_0, var_0)
    assert var_1 == "1001001010"
    var_2 = module_0.add_binary(var_0, var_1)
    assert var_2 == "10100100110"


def test_case_1():
    tuple_0 = ()
    var_0 = module_0.add_binary(tuple_0, tuple_0)
    assert var_0 == ""


@pytest.mark.xfail(strict=True)
def test_case_2():
    none_type_0 = None
    module_0.add_binary(none_type_0, none_type_0)


@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = "7iM;m'3+O\x0c"
    var_0 = module_0.add_binary(str_0, str_0)
    assert var_0 == "1011011100"
    var_1 = module_0.add_binary(var_0, var_0)
    assert var_1 == "10110111000"
    var_2 = module_0.add_binary(str_0, var_1)
    assert var_2 == "10100100110"
    tuple_0 = (var_1,)
    module_0.add_binary(tuple_0, var_2)


@pytest.mark.xfail(strict=True)
def test_case_4():
    set_0 = set()
    list_0 = [set_0, set_0, set_0]
    module_0.add_binary(set_0, list_0)

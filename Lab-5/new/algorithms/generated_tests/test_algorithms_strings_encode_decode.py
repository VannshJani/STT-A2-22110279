# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.strings.encode_decode as module_0


@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = "Na+yMHw'0>d&5"
    var_0 = module_0.encode(str_0)
    assert var_0 == "13:Na+yMHw'0>d&5"
    var_1 = module_0.encode(str_0)
    assert var_1 == "13:Na+yMHw'0>d&5"
    var_2 = module_0.decode(var_0)
    module_0.decode(str_0)


@pytest.mark.xfail(strict=True)
def test_case_1():
    str_0 = "y)D\\l80u(<$:<8D"
    module_0.decode(str_0)


@pytest.mark.xfail(strict=True)
def test_case_2():
    list_0 = []
    var_0 = module_0.decode(list_0)
    var_1 = module_0.decode(var_0)
    module_0.encode(list_0)


@pytest.mark.xfail(strict=True)
def test_case_3():
    none_type_0 = None
    module_0.decode(none_type_0)


@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = " Calculates the factorial of a given number n "
    var_0 = module_0.encode(str_0)
    assert var_0 == "10:Calculates3:the9:factorial2:of1:a5:given6:number1:n"
    str_1 = "|#X2"
    var_1 = module_0.decode(var_0)
    complex_0 = 2j
    dict_0 = {str_1: str_1, complex_0: complex_0, str_1: str_1}
    module_0.decode(dict_0)

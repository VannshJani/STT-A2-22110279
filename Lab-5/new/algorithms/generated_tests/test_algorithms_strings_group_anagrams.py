# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.strings.group_anagrams as module_0
import builtins as module_1


@pytest.mark.xfail(strict=True)
def test_case_0():
    bool_0 = False
    list_0 = []
    list_1 = [bool_0, bool_0, bool_0, list_0]
    module_0.group_anagrams(list_1)


def test_case_1():
    set_0 = set()
    var_0 = module_0.group_anagrams(set_0)
    var_1 = module_0.group_anagrams(var_0)
    var_2 = module_0.group_anagrams(set_0)
    var_3 = module_0.group_anagrams(set_0)
    var_4 = module_0.group_anagrams(set_0)
    var_5 = module_0.group_anagrams(var_3)
    var_6 = module_0.group_anagrams(var_0)
    var_7 = module_0.group_anagrams(var_3)
    var_8 = module_0.group_anagrams(set_0)
    var_9 = module_0.group_anagrams(var_8)
    var_10 = module_0.group_anagrams(var_9)


@pytest.mark.xfail(strict=True)
def test_case_2():
    bool_0 = True
    module_0.group_anagrams(bool_0)


@pytest.mark.xfail(strict=True)
def test_case_3():
    str_0 = 'n&";'
    var_0 = module_0.group_anagrams(str_0)
    object_0 = module_1.object()
    set_0 = set()
    var_1 = module_0.group_anagrams(set_0)
    module_0.group_anagrams(object_0)


@pytest.mark.xfail(strict=True)
def test_case_4():
    list_0 = []
    str_0 = "?!_@0B_i`cOi[k#>]"
    var_0 = module_0.group_anagrams(str_0)
    str_1 = "E!bE7XaJ&7["
    var_1 = module_0.group_anagrams(var_0)
    var_2 = module_0.group_anagrams(str_1)
    str_2 = "1\nPcv\rkD"
    var_3 = module_0.group_anagrams(list_0)
    str_3 = "0[skcg,8;b$RGQ@Q"
    dict_0 = {str_0: list_0, str_1: list_0, str_2: str_1, str_1: str_3}
    module_1.object(*list_0, **dict_0)

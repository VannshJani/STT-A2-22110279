# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import algorithms.strings.merge_string_checker as module_0


def test_case_0():
    bytes_0 = b"v|\xdf%\x906"
    var_0 = module_0.is_merge_recursive(bytes_0, bytes_0, bytes_0)
    assert var_0 is False


def test_case_1():
    none_type_0 = None
    var_0 = module_0.is_merge_recursive(none_type_0, none_type_0, none_type_0)
    assert var_0 is True


def test_case_2():
    bytes_0 = b"v|\xdf%\x906\xd1"
    var_0 = module_0.is_merge_iterative(bytes_0, bytes_0, bytes_0)
    assert var_0 is False


def test_case_3():
    str_0 = "//"
    var_0 = module_0.is_merge_recursive(str_0, str_0, str_0)
    assert var_0 is False


def test_case_4():
    dict_0 = {}
    list_0 = [dict_0]
    list_1 = [list_0, list_0]
    var_0 = module_0.is_merge_iterative(list_1, dict_0, dict_0)
    assert var_0 is False


def test_case_5():
    dict_0 = {}
    var_0 = module_0.is_merge_iterative(dict_0, dict_0, dict_0)
    assert var_0 is True

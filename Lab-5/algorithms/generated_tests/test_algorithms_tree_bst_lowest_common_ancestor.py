# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.tree.bst.lowest_common_ancestor as module_0


@pytest.mark.xfail(strict=True)
def test_case_0():
    none_type_0 = None
    bytes_0 = b"-c\x8b %\xd3$\x7f\x80X\xca\xed$\xda?\x03\xea\xc5\x14;"
    var_0 = module_0.lowest_common_ancestor(none_type_0, none_type_0, none_type_0)
    module_0.lowest_common_ancestor(bytes_0, bytes_0, bytes_0)

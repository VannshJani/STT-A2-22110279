# Test cases automatically generated by Pynguin (https://www.pynguin.eu).
# Please check them before you use them.
import pytest
import algorithms.tree.trie.add_and_search as module_0
import collections as module_1


@pytest.mark.xfail(strict=True)
def test_case_0():
    str_0 = "5O@E*D}pP#tXI~6 y"
    word_dictionary_0 = module_0.WordDictionary()
    var_0 = word_dictionary_0.search(str_0)
    assert var_0 is False
    var_1 = word_dictionary_0.add_word(str_0)
    var_1.add_word(var_0)


def test_case_1():
    str_0 = "5O@E*D}pP#tXI~6 y"
    word_dictionary_0 = module_0.WordDictionary()
    var_0 = word_dictionary_0.search(str_0)
    assert var_0 is False


@pytest.mark.xfail(strict=True)
def test_case_2():
    word_dictionary2_0 = module_0.WordDictionary2()
    word_dictionary2_0.add_word(word_dictionary2_0)


@pytest.mark.xfail(strict=True)
def test_case_3():
    word_dictionary2_0 = module_0.WordDictionary2()
    none_type_0 = None
    var_0 = word_dictionary2_0.add_word(none_type_0)
    word_dictionary_0 = module_0.WordDictionary()
    word_dictionary_0.search(var_0)


@pytest.mark.xfail(strict=True)
def test_case_4():
    word_dictionary2_0 = module_0.WordDictionary2()
    word_dictionary2_0.search(word_dictionary2_0)


@pytest.mark.xfail(strict=True)
def test_case_5():
    word_dictionary2_0 = module_0.WordDictionary2()
    str_0 = '4~ExR\nQky"ThI('
    trie_node_0 = module_0.TrieNode(str_0, str_0)
    none_type_0 = None
    var_0 = word_dictionary2_0.search(none_type_0)
    assert var_0 is False
    var_1 = word_dictionary2_0.search(str_0)
    assert var_1 is False
    word_dictionary2_0.add_word(word_dictionary2_0)


def test_case_6():
    word_dictionary_0 = module_0.WordDictionary()


def test_case_7():
    word_dictionary2_0 = module_0.WordDictionary2()


@pytest.mark.xfail(strict=True)
def test_case_8():
    word_dictionary_0 = module_0.WordDictionary()
    word_dictionary_1 = module_0.WordDictionary()
    word_dictionary_1.search(word_dictionary_1, word_dictionary_1)


def test_case_9():
    word_dictionary2_0 = module_0.WordDictionary2()
    str_0 = "@LV=j67jzn. k~JJPJ"
    var_0 = word_dictionary2_0.add_word(str_0)
    assert len(word_dictionary2_0.word_dict) == 1
    var_1 = word_dictionary2_0.search(str_0)
    assert var_1 is True


@pytest.mark.xfail(strict=True)
def test_case_10():
    word_dictionary2_0 = module_0.WordDictionary2()
    str_0 = "@LV=j67jzn. k~JJPJ"
    var_0 = word_dictionary2_0.search(str_0)
    assert len(word_dictionary2_0.word_dict) == 1
    var_0.search(str_0)


@pytest.mark.xfail(strict=True)
def test_case_11():
    word_dictionary2_0 = module_0.WordDictionary2()
    str_0 = "@LV=j67jzn. k~JJPJ"
    var_0 = word_dictionary2_0.search(str_0)
    assert len(word_dictionary2_0.word_dict) == 1
    word_dictionary_0 = module_0.WordDictionary()
    var_1 = word_dictionary_0.search(str_0)
    assert var_1 is False
    var_2 = word_dictionary_0.add_word(str_0)
    var_3 = word_dictionary_0.add_word(str_0)
    var_1.__contains__(var_0)


@pytest.mark.xfail(strict=True)
def test_case_12():
    word_dictionary2_0 = module_0.WordDictionary2()
    ordered_dict_0 = module_1.OrderedDict()
    none_type_0 = None
    var_0 = word_dictionary2_0.add_word(none_type_0)
    word_dictionary_0 = module_0.WordDictionary()
    var_1 = word_dictionary_0.search(ordered_dict_0)
    assert var_1 is False
    var_1.__setitem__(word_dictionary_0, ordered_dict_0)


@pytest.mark.xfail(strict=True)
def test_case_13():
    str_0 = "'@=&j).k"
    word_dictionary_0 = module_0.WordDictionary()
    var_0 = word_dictionary_0.add_word(str_0)
    word_dictionary_0.search(str_0)


@pytest.mark.xfail(strict=True)
def test_case_14():
    str_0 = "'@=&j)."
    word_dictionary_0 = module_0.WordDictionary()
    var_0 = word_dictionary_0.add_word(str_0)
    word_dictionary_0.search(str_0)

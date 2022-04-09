# Custom imports
from notion_word_data import utils


def test_prettify_normal():
    assert utils.prettify("test") == "Test"


def test_prettify_special():
    assert utils.prettify("‘test’") == "‘test’"


def test_dict_get_element_by_index():
    assert utils.dict_get_element_by_index({"Test": ""}, 0) == "Test"

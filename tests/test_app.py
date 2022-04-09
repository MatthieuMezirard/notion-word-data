# Third party imports
import pytest

# Custom imports
from notion_word_data import app
from notion_word_data import errors


def test_get_word_to_find_success():
    assert ["Example", "en"] in app.get_words_to_find("WORDS.md", 4)


def test_get_word_to_find_failure_InvalidDeclarations():
    with pytest.raises(errors.InvalidDeclarations):
        app.get_words_to_find("WORDS.md", 1)

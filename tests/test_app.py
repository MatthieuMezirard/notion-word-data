# Third party imports
import pytest

# Custom imports
from notion_word_data import app
from notion_word_data import errors


def test_get_word_to_find():
    assert ["Example", "en"] in app.get_words_to_find("WORDS.md", 4)

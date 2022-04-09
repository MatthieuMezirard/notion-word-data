# Third party imports
import pytest
import requests

# Custom imports
from notion_word_data import notion
from notion_word_data import errors

HEADERS = {
    "Authorization": f"Bearer {notion.TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-02-22",
}
PAYLOAD = {
    "filter": {
        "and": [
            {"property": "Word", "title": {"is_not_empty": True}},
            {"property": "Word", "title": {"starts_with": "Test"}},
        ],
        "start_cursor": "string",
        "page_size": 250,
    }
}


def test_query_database_success():
    response = notion.NotionSync.query_database(HEADERS, PAYLOAD, requests.Session())
    assert isinstance(response, dict)


def test_query_database_failure_InvalidDatabaseID():
    notion.DATABASE_ID = "invalid"
    with pytest.raises(errors.InvalidDatabaseID):
        notion.NotionSync.query_database(HEADERS, PAYLOAD, requests.Session())


def test_query_database_failure_InvalidToken():
    with pytest.raises(errors.InvalidToken):
        notion.NotionSync.query_database("", PAYLOAD, requests.Session())

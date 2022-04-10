"""A custom module to update a Notion database with the given data."""

# System imports
import json
import os

# Third party imports
import dotenv
import requests

# Custom imports
from notion_word_data import errors, logs, utils

general_logger = logs.setup_logging_general(f"{__name__}.general")

dotenv.load_dotenv()
DATABASE_ID = os.environ.get("DATABASE_ID")
TOKEN = os.environ.get("TOKEN")
NOTION_ENDPOINT_DATABASE = "https://api.notion.com/v1/databases/"
NOTION_ENDPOINT_PAGE = "https://api.notion.com/v1/pages/"
NOTION_ENDPOINT_BLOCKS = "https://api.notion.com/v1/blocks/"


class NotionSync:
    """A class to update a Notion database from a database ID with the given data."""

    def __init__(self, data: dict, session: requests.sessions.Session) -> None:
        """The initialization function of NotionSync.

        Args:
            data (dict): The dictionary containing all the data to be added.
            session (requests.sessions.Session): The session used to fetch data.
        """
        self.data = data
        self.name = utils.dict_get_element_by_index(self.data, 0)
        general_logger.debug('Initializing Notion class for "%s".', self.name)
        self.identifier = ""
        self.json_data = {"parent": {"database_id": DATABASE_ID}, "properties": {}}

        self.headers = {
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-02-22",
        }
        self.payload = {
            "filter": {
                "and": [
                    {"property": "Word", "title": {"is_not_empty": True}},
                    {"property": "Word", "title": {"starts_with": self.name}},
                ],
                "start_cursor": "string",
                "page_size": 250,
            }
        }
        self.session = session

        def update_notion():
            """Update a Notion database with the given data."""
            id_list = self.get_database_id(self.headers, self.payload, self.session)
            for page_id in id_list:
                self.delete_page(page_id, self.headers, self.session)
            self.set_new_page()

        update_notion()

    @classmethod
    def query_database(
        cls, headers: dict, payload: dict, session: requests.sessions.Session
    ) -> dict:
        """Get the content of a database.

        Args:
            headers (dict): The headers used to process the request.
            payload (dict): The payload used to process the request.
            session (requests.sessions.Session): The session used to process the request.

        Raises:
            errors.InvalidDatabaseID: An exception to indicate that the given database ID is invalid.
            errors.InvalidToken: An exception to indicate that the given token is invalid.

        Returns:
            dict: A dictionary of the existing data.
        """
        general_logger.debug("Querying the database.")
        database_url = f"{NOTION_ENDPOINT_DATABASE}{DATABASE_ID}/query"
        response = session.post(url=database_url, headers=headers, json=payload)
        if response.status_code == 400 and response.reason == "Bad Request":
            raise errors.InvalidDatabaseID(DATABASE_ID)
        if response.status_code == 401 and response.reason == "Unauthorized":
            raise errors.InvalidToken(TOKEN)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_database_id(
        cls, headers: dict, payload: dict, session: requests.sessions.Session
    ) -> list[str]:
        """Get the ID of the pages matching the word name.

        Args:
            headers (dict): The headers used to process the request.
            payload (dict): The payload used to process the request.
            session (requests.sessions.Session): The session used to process the request.

        Returns:
            list[str]: A list of all the pages ID matching the word name.
        """
        general_logger.debug(
            'Getting the database ID for "%s".',
            payload["filter"]["and"][1]["title"]["starts_with"],
        )
        existing_data = cls.query_database(headers, payload, session)
        id_list = [page["id"] for page in existing_data["results"]]
        return id_list

    @classmethod
    def create_page(
        cls, data_to_send: dict, headers: dict, session: requests.sessions.Session
    ) -> None:
        """Create a new database entry.

        Args:
            data_to_send (dict): The dictionary containing the data you want to add to a database entry.
            headers (dict): The headers used to process the request.
            session (requests.sessions.Session): The payload used to process the request.
        """
        general_logger.debug("Creating a page.")
        data_to_send = json.dumps(data_to_send)
        response = session.post(
            url=NOTION_ENDPOINT_PAGE, data=data_to_send, headers=headers
        )
        response.raise_for_status()

    @classmethod
    def update_page(
        cls,
        page_id: str,
        data_to_send: dict,
        headers: dict,
        session: requests.sessions.Session,
    ) -> None:
        """Update a database entry.

        Args:
            page_id (str): The ID of the database entry to be updated.
            data_to_send (dict): The dictionary containing the data you want to add to the database entry.
            headers (dict): The headers used to process the request.
            session (requests.sessions.Session): The session used to process the request.
        """
        general_logger.debug("Updating a page.")
        data_to_send = json.dumps(data_to_send)
        page_url = f"{NOTION_ENDPOINT_PAGE}{page_id}"
        response = session.patch(url=page_url, data=data_to_send, headers=headers)
        response.raise_for_status()

    @classmethod
    def delete_page(
        cls, page_id: str, headers: dict, session: requests.sessions.Session
    ) -> None:
        """Delete a database entry.

        Args:
            page_id (str): The ID of the database entry to be deleted.
            headers (dict): The headers used to process the request.
            session (requests.sessions.Session): The payload used to process the request.
        """
        general_logger.debug("Deleting a page.")
        page_url = f"{NOTION_ENDPOINT_BLOCKS}{page_id}"
        response = session.delete(url=page_url, headers=headers)
        response.raise_for_status()

    def set_new_page(self) -> None:
        """Create a new page with the given data."""
        general_logger.debug('Setting new page for "%s".', self.name)

        def set_word_block() -> dict:
            """Set the JSON block for the 'Word' property.

            Returns:
                dict: A dictionary containing the 'Word' property.
            """
            general_logger.debug('Setting word block for "%s".', self.name)
            word_property = {"title": [{"text": {"content": self.name}}]}
            return word_property

        word_block = set_word_block()
        self.json_data["properties"]["Word"] = word_block

        def set_pos_block() -> dict:
            """Set the JSON block for the 'Part Of Speech' property.

            Returns:
                dict: A dictionary containing the 'Part Of Speech' property.
            """
            general_logger.debug('Setting pos block for "%s".', self.name)
            pos_list = list(self.data[utils.dict_get_element_by_index(self.data, 0)])
            pos_property = {"multi_select": [{"name": pos} for pos in pos_list]}
            return pos_property

        pos_block = set_pos_block()
        self.json_data["properties"]["Part Of Speech"] = pos_block

        self.create_page(self.json_data, self.headers, self.session)
        self.identifier = self.get_database_id(
            self.headers, self.payload, self.session
        )[0]

        def set_infos_block() -> None:
            """Set the JSON block for the 'Informations' property.

            Returns:
                dict: A dictionary containing the 'Informations' property.
            """
            general_logger.debug('Setting infos block for "%s".', self.name)

            def get_pos_color() -> dict:
                """Get the Notion color for the parts of speechs.

                Returns:
                    dict: A dictionary containing the parts of speechs and their corresponding colors.
                """
                general_logger.debug('Getting pos color for "%s".', self.name)
                existing_data = self.query_database(
                    self.headers, self.payload, self.session
                )
                pos_color_dict = {
                    pos["name"]: pos["color"]
                    for pos in existing_data["results"][0]["properties"][
                        "Part Of Speech"
                    ]["multi_select"]
                }
                return pos_color_dict

            color_dict = get_pos_color()
            infos_property = {"rich_text": []}
            for pos in self.data[utils.dict_get_element_by_index(self.data, 0)]:
                color = color_dict[pos]
                number = 1
                for definition in self.data[
                    utils.dict_get_element_by_index(self.data, 0)
                ][pos]:
                    infos_property["rich_text"].append(
                        {
                            "text": {"content": str(number) + ". " + definition + "\n"},
                            "annotations": {"bold": True, "color": color},
                        }
                    )
                    number += 1
                    example_str = ""
                    for example in self.data[
                        utils.dict_get_element_by_index(self.data, 0)
                    ][pos][definition][0]:
                        example_str += f"{example}, "
                    if example_str != "":
                        infos_property["rich_text"].append(
                            {"text": {"content": example_str[:-2] + "\n"}}
                        )
                    synonym_str = ""
                    for synonym in self.data[
                        utils.dict_get_element_by_index(self.data, 0)
                    ][pos][definition][1]:
                        synonym_str += f"{synonym}, "
                    if synonym_str != "":
                        infos_property["rich_text"].append(
                            {
                                "text": {"content": synonym_str[:-2] + "\n"},
                                "annotations": {"italic": True, "color": "gray"},
                            }
                        )
                infos_property["rich_text"].append({"text": {"content": "\n"}})
            infos_property["rich_text"][-1]["text"]["content"] = infos_property[
                "rich_text"
            ][-1]["text"]["content"][:-2]
            return infos_property

        infos_block = set_infos_block()
        self.json_data["properties"]["Informations"] = infos_block
        self.update_page(self.identifier, self.json_data, self.headers, self.session)

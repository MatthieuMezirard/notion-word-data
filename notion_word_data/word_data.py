"""A custom module to fetch Google Dictionary's data for a given word."""

# System imports
import random
import types

# Third party imports
import bs4
import requests

# Custom imports
from notion_word_data import errors, logs, utils

general_logger = logs.setup_logging_general(f"{__name__}.general")


class WordData:
    """A class to fetch Google Dictionary's data for a given word, in a given language."""

    def __init__(
        self, word: str, lang: str, session: requests.sessions.Session
    ) -> None:
        """The initialization function of WordData.

        Args:
            word (str): The word you want to fetch data for.
            lang (str): The language you want to fetch data in.
            session (requests.sessions.Session): The session used to fetch data.
        """

        self.check_language(lang)

        self.search_word = word.lower()
        self.queried_language = lang.lower()
        general_logger.debug(
            'Initializing WordData class for "%s" in language "%s".',
            self.search_word,
            self.queried_language,
        )
        self.url = f"https://www.google.com/search?hl={self.queried_language}&q=define+{self.search_word}&num=1"
        self.data = {}

        self.consent_cookie = (
            f"YES+cb.20220219-22-p0.en-US+FX+{random.randint(100, 900)}"
        )
        self.headers = {
            "cookie": f"CONSENT={self.consent_cookie};",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
        }
        self.session = session

        def fetch_word_data() -> None:
            """Fetch Google Dictionary's data for a given word."""
            response = self.get_web_data(self.url, self.headers, self.session)
            soup = self.parse_web_data(response)
            self.set_word_data(soup)

        fetch_word_data()

    @classmethod
    def check_language(cls, lang: str) -> None:
        """Check if a given language is valid.

        Args:
            lang (str): The language you want to verify.

        Raises:
            errors.InvalidLanguage: An exception to indicate that the given language cannot be found in SUPPORTED_LANGUAGES.md.
        """
        general_logger.debug('Checking the validity of "%s".', lang)
        with open("SUPPORTED_LANGUAGES.md", "r", encoding="utf-8") as file:
            if ("```" + lang.lower() + "```") not in file.read():
                raise errors.InvalidLanguage(lang)

    @classmethod
    def get_web_data(
        cls, url: str, headers: dict, session: requests.sessions.Session
    ) -> requests.models.Response:
        """Get the web results for a given word

        Args:
            url (str): The URL you want to get data from.
            headers (dict): The headers used to process the request.
            session (requests.sessions.Session): The session used to process the request.

        Returns:
            requests.models.Response: The raw request result.
        """
        general_logger.debug('Fetching web data for "%s".', url)
        response = session.get(url=url, headers=headers)
        response.raise_for_status()
        return response

    @classmethod
    def parse_web_data(cls, response: requests.models.Response) -> bs4.BeautifulSoup:
        """Get the parsed data from a request result.

        Args:
            response (requests.models.Response): The raw request result.

        Returns:
            bs4.BeautifulSoup: The parsed data from the request result.
        """
        general_logger.debug("Parsing web data.")
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        return soup

    def set_word_data(self, soup: bs4.BeautifulSoup) -> dict:
        """Set the word name, parts of speech, definitions, examples and synonyms.

        Args:
            soup (bs4.BeautifulSoup): The parsed data from the request result.

        Raises:
            errors.InvalidWord: An exception to indicate that the given word cannot be found on Google Search.
        """
        general_logger.debug(
            'Setting word data for "%s" in "%s".',
            self.search_word,
            self.queried_language,
        )

        def set_word_name() -> None:
            """Set the word name.

            Raises:
                errors.InvalidWord: An exception to indicate that the given word cannot be found on Google Search.
            """
            general_logger.debug(
                'Setting word name for "%s" in "%s".',
                self.search_word,
                self.queried_language,
            )
            name = soup.find(attrs={"data-dobid": "hdw"})
            if not isinstance(name, types.NoneType):
                self.data[utils.prettify(name.text)] = {}
            else:
                raise errors.InvalidWord(self.search_word)

        set_word_name()

        def set_word_pos() -> None:
            """Set the word parts of speech."""
            general_logger.debug(
                'Setting word pos for "%s" in "%s".',
                self.search_word,
                self.queried_language,
            )
            pos_wrapper = soup.find_all("div", "lW8rQd")
            for index, _ in enumerate(pos_wrapper, 0):
                pos = pos_wrapper[index].find("span", "YrbPuc")
                self.data[utils.dict_get_element_by_index(self.data, 0)][
                    utils.prettify(pos.text)
                ] = {}

        set_word_pos()

        def set_word_info() -> None:
            """Set the word informations (definitions, examples and synonyms)"""
            general_logger.debug(
                'Setting word infos for "%s" in "%s".',
                self.search_word,
                self.queried_language,
            )
            info_wrapper = soup.find_all("ol", "eQJLDd")
            for index_wrapper, _ in enumerate(info_wrapper, 0):
                info_number = info_wrapper[index_wrapper].find_all(
                    "div", class_="thODed"
                )
                for index_number, _ in enumerate(info_number, 0):
                    # Definitions
                    definition = info_number[index_number].find(
                        attrs={"data-dobid": "dfn"}
                    )
                    self.data[utils.dict_get_element_by_index(self.data, 0)][
                        utils.dict_get_element_by_index(
                            self.data[utils.dict_get_element_by_index(self.data, 0)],
                            index_wrapper,
                        )
                    ][utils.prettify(definition.text)] = [[], []]
                    # Examples
                    examples = info_number[index_number].find_all(
                        "div", class_="ubHt5c"
                    )
                    for example in examples:
                        self.data[utils.dict_get_element_by_index(self.data, 0)][
                            utils.dict_get_element_by_index(
                                self.data[
                                    utils.dict_get_element_by_index(self.data, 0)
                                ],
                                index_wrapper,
                            )
                        ][utils.prettify(definition.text)][0].append(
                            "”" + utils.prettify((example.text).replace('"', "")) + "”"
                        )
                    # Synonyms
                    synonyms = info_number[index_number].find_all(
                        "div",
                        class_="EmSASc gWUzU MR2UAc F5z5N jEdCLc LsYFnd p9F8Cd I6a0ee rjpYgb gjoUyf",
                    )
                    for synonym in synonyms:
                        self.data[utils.dict_get_element_by_index(self.data, 0)][
                            utils.dict_get_element_by_index(
                                self.data[
                                    utils.dict_get_element_by_index(self.data, 0)
                                ],
                                index_wrapper,
                            )
                        ][utils.prettify(definition.text)][1].append(
                            utils.prettify(synonym.text)
                        )

        set_word_info()

# System imports
import types
import random

# Third party imports
import requests
import bs4

# Custom imports
from notion_word_data import utils
from notion_word_data import errors


class WordData:
    def __init__(
        self, word: str, lang: str, session: requests.sessions.Session
    ) -> None:

        self.check_language(lang)

        self.search_word = word.lower()
        self.queried_language = lang.lower()
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
            response = self.get_web_data(self.url, self.headers, self.session)
            soup = self.parse_web_data(response)
            self.set_word_data(soup)

        fetch_word_data()

    @classmethod
    def check_language(cls, lang: str) -> None:
        with open("SUPPORTED_LANGUAGES.md", "r", encoding="utf-8") as file:
            if ("```" + lang.lower() + "```") not in file.read():
                raise errors.InvalidLanguage(lang)

    @classmethod
    def get_web_data(
        cls, url: str, headers: dict, session: requests.sessions.Session
    ) -> requests.models.Response:
        response = session.get(url=url, headers=headers)
        response.raise_for_status()
        return response

    @classmethod
    def parse_web_data(cls, response: requests.models.Response) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(response.content, "html.parser")
        return soup

    def set_word_data(self, soup: bs4.BeautifulSoup) -> dict:
        def set_word_name() -> None:
            name = soup.find(attrs={"data-dobid": "hdw"})
            if not isinstance(name, types.NoneType):
                self.data[utils.prettify(name.text)] = {}
            else:
                raise errors.InvalidWord(self.search_word)

        set_word_name()

        def set_word_pos() -> None:
            pos_wrapper = soup.find_all("div", "lW8rQd")
            for index, _ in enumerate(pos_wrapper, 0):
                pos = pos_wrapper[index].find("span", "YrbPuc")
                self.data[utils.dict_get_element_by_index(self.data, 0)][
                    utils.prettify(pos.text)
                ] = {}

        set_word_pos()

        def set_word_info() -> None:
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

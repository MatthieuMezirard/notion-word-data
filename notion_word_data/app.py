# System imports
import multiprocessing
import itertools

# Third party imports
import requests


# Custom imports
from notion_word_data import word_data
from notion_word_data import notion
from notion_word_data import utils
from notion_word_data import errors


def main() -> None:
    words = get_words_to_find("WORDS.md", 4)
    session = requests.Session()
    with multiprocessing.Pool(processes=4) as pool:
        return_words = pool.starmap(
            worker_process, zip(words, itertools.repeat(session))
        )
    words_to_delete = [word[0] for word in return_words if word]
    delete_word(words_to_delete, "WORDS.md", 4)


def get_words_to_find(file_name: str, index: int, default_lang="en") -> list[str]:
    words_list = []
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()[index:]
        for line in lines:
            data = line.split(",")
            if len(data) < 2:
                data.append(default_lang)
            elif len(data) > 2:
                raise errors.InvalidDeclarations(data, line)
            words_list.append(
                [
                    utils.prettify(data[0].replace("\n", "")),
                    utils.prettify(data[1].replace("\n", "")).lower(),
                ]
            )
        return words_list


def delete_word(words: list[str], file_name: str, index: int) -> None:
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        first_lines = lines[:index]
        other_lines = lines[index:]
    with open(file_name, "w", encoding="utf-8") as file:
        for first_line in first_lines:
            file.write(first_line)
        for other_line in other_lines:
            if not any(word in other_line.replace("\n", "") for word in words):
                file.write(other_line)


def worker_process(word: str, session: requests.sessions.Session):
    word_name = word[0]
    word_lang = word[1]
    try:
        notion.NotionSync(
            word_data.WordData(word_name, word_lang, session).data, session
        )
        return word
    except errors.CustomException:
        print(
            f'An error has been encountered trying to add {word_name} for the language "{word_lang}".'
        )
        return None


if __name__ == "__main__":
    main()

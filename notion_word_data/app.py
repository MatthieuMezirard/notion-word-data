"""The main module, the only one you should run."""

# System imports
import itertools
import multiprocessing

# Third party imports
import alive_progress
import requests

# Custom imports
from notion_word_data import errors, logs, notion, utils, word_data

general_logger = logs.setup_logging_general(f"{__name__}.general")
exception_logger = logs.setup_logging_exception(f"{__name__}.exception")


PROCESSES = 4


def main() -> None:
    """The main function, which gets called at runtime."""
    general_logger.debug("Start main process.")
    words = get_words_to_find("WORDS.md", 4)
    session = requests.Session()
    success_words = []
    with multiprocessing.Pool(processes=PROCESSES) as pool:
        general_logger.debug("Starting multiprocessing with %i processes.", PROCESSES)
        with alive_progress.alive_bar(
            total=len(words), title="Progress", dual_line=True
        ) as progress_bar:
            progress_bar.text = "Processing... Please wait."
            return_words = pool.starmap(
                worker_process, zip(words, itertools.repeat(session))
            )
            for word in return_words:
                if "success" == word[2]:
                    general_logger.info(
                        'The word "%s" has successfully been added for the language "%s".',
                        word[0],
                        word[1],
                    )
                    success_words.append(word[0])
                elif "failure" == word[2]:
                    general_logger.warning(
                        'An error has been encountered trying to add the word "%s" for the language "%s". Error type: %s. Message: %s',
                        word[0],
                        word[1],
                        word[3].__class__.__name__,
                        word[3],
                    )
                else:
                    general_logger.critical(
                        'An unexpected error occurred trying to add the word "%s" for the language "%s". Error type : %s. Message: %s',
                        word[0],
                        word[1],
                        word[3].__class__.__name__,
                        word[3],
                    )

                progress_bar()

    delete_word(success_words, "WORDS.md", 4)
    general_logger.info("Done!")


def get_words_to_find(file_name: str, index: int, default_lang="en") -> list[str]:
    """Get the list of words you want to fetch data for, and their corresponding languages.

    Args:
        file_name (str): The file name containing the words.
        index (int): The number of lines that should be ignored at the beginning of the file.
        default_lang (str, optional): The default word language. Defaults to "en".

    Raises:
        errors.InvalidDeclaration: An exception to indicate that a declaration in WORDS.md is invalid.

    Returns:
        list[str]: A list containing each word to find, and its language.
    """
    general_logger.debug("Searching for words.")
    words_list = []
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()[index:]
        for line in lines:
            try:
                data = line.split(",")
                data[-1] = data[-1].strip().replace("\n", "")
                if data[-1] == "":
                    data.pop()
                if len(data) > 2 or not data:
                    line_index = lines.index(line) + index + 1
                    raise errors.InvalidDeclaration(data, line_index)
                if len(data) < 2:
                    data.append(default_lang)
            except errors.InvalidDeclaration as error:
                general_logger.warning(
                    "An error has been encountered trying to get the words in WORDS.md. Error type: %s. Message: %s",
                    error.__class__.__name__,
                    error,
                )
                exception_logger.exception("Caught an expected error.", exc_info=True)
            else:
                general_logger.debug("OK %s", data)
                words_list.append(
                    [
                        utils.prettify(data[0].replace("\n", "")),
                        utils.prettify(data[1].replace("\n", "")).lower(),
                    ]
                )
    general_logger.debug("Found %i word(s).", len(words_list))
    return words_list


def delete_word(words: list[str], file_name: str, index: int) -> None:
    """Delete the words in a file from a given list.

    Args:
        words (list[str]): The words to be deleted.
        file_name (str): The file name containing the words.
        index (int): The number of lines that should be ignored at the beginning of the file.
    """
    general_logger.debug("Deleting %i word(s).", len(words))
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
    general_logger.debug("Deleted %s.", words)


def worker_process(
    word: list[str],
    session: requests.sessions.Session,
) -> list[str]:
    """The process that will be repeated by the multiprocessing's workers.

    Args:
        word (list[str]): A list containing the word and the language to be processed.
        session (requests.sessions.Session): The session used to process the request.

    Returns:
        list[str]: A list containing the word name, its language and the result of the process.
    """
    word_name = word[0]
    word_lang = word[1]
    try:
        notion.NotionSync(
            word_data.WordData(word_name, word_lang, session).data, session
        )
    except errors.CustomException as error:
        exception_logger.exception("Caught an expected error.", exc_info=True)
        return [word_name, word_lang, "failure", error]
    except Exception as error:
        exception_logger.exception("Caught an unexpected error.", exc_info=True)
        return [word_name, word_lang, error]
    else:
        exception_logger.debug("No error caught.")
        return [word_name, word_lang, "success"]


if __name__ == "__main__":
    main()

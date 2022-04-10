"""A custom module to manage logging."""

# System imports
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

LOG_FILE = "./notion_word_data/logs.log"


@staticmethod
def get_file_handler() -> logging.Handler:
    """Get the file handler.

    Returns:
        logging.Handler: The handler managing file output.
    """
    file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
    file_format = logging.Formatter(
        "%(asctime)s, %(levelname)-8s [%(filename)s:%(module)s:%(funcName)s:%(lineno)d] %(message)s"
    )
    file_handler.setFormatter(file_format)
    file_handler.setLevel(logging.DEBUG)
    return file_handler


@staticmethod
def get_console_handler() -> logging.Handler:
    """Get the console handler.

    Returns:
        logging.Handler: The handler managing console output.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_format = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_format)
    console_handler.setLevel(logging.INFO)
    return console_handler


@staticmethod
def setup_logging_general(logger_name: str) -> logging.Logger:
    """Setup a logger for general informations.

    Args:
        logger_name (str): The name of the logger you want to create.

    Returns:
        logging.Logger: The created logger.
    """
    logger = logging.getLogger(logger_name)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    logger.setLevel(logging.DEBUG)
    logger.debug("Creating logger %s.", logger_name)
    return logger


@staticmethod
def setup_logging_exception(logger_name: str) -> logging.Logger:
    """Setup a logger for exceptions.

    Args:
        logger_name (str): The name of the logger you want to create.

    Returns:
        logging.Logger: The created logger.
    """
    logger = logging.getLogger(logger_name)
    logger.addHandler(get_file_handler())
    logger.setLevel(logging.ERROR)
    logger.debug("Creating logger %s.", logger_name)
    return logger

"""A custom module for custom exceptions."""


class CustomException(Exception):
    """A custom class for exceptions."""


class InvalidWord(CustomException):
    """An exception to indicate that the given word cannot be found on Google Search."""

    def __init__(self, word: str) -> None:
        """The initialization function of InvalidWord.

        Args:
            word (str): The invalid word that raised this exception.
        """
        self.word = word
        super().__init__(self.word)

    def __str__(self) -> str:
        """The error text of InvalidWord.

        Returns:
            str: The text that will be printed if InvalidWord is raised.
        """
        return f'The word "{self.word}" is invalid. Check for misspelling or for language compatibility with Google Search.'


class InvalidLanguage(CustomException):
    """An exception to indicate that the given language cannot be found in SUPPORTED_LANGUAGES.md."""

    def __init__(self, lang: str) -> None:
        """The initialization function of InvalidLanguage.

        Args:
            lang (str): The invalid language that raised this exception.
        """
        self.lang = lang
        super().__init__(self.lang)

    def __str__(self) -> str:
        """The error text of InvalidLanguage.

        Returns:
            str: The text that will be printed if InvalidLanguage is raised.
        """
        return f'The language "{self.lang}" is invalid. Verify that it can be found in SUPPORTED_LANGUAGES.md.'


class InvalidDatabaseID(CustomException):
    """An exception to indicate that the given database ID is invalid."""

    def __init__(self, database_id: str) -> None:
        """The initialization function of InvalidDatabaseID.

        Args:
            database_id (str): The invalid database ID that raised this exception.
        """
        self.database_id = database_id
        super().__init__(self.database_id)

    def __str__(self) -> str:
        """The error text of InvalidDatabaseID.

        Returns:
            str: The text that will be printed if InvalidDatabaseID is raised.
        """
        return f'The database id "{self.database_id}" is invalid. Verify that it has correctly been added to .env.'


class InvalidToken(CustomException):
    """An exception to indicate that the given token is invalid."""

    def __init__(self, token: str) -> None:
        """The initialization function of InvalidToken.

        Args:
            token (str): The invalid token that raised this exception.
        """
        self.token = token
        super().__init__(self.token)

    def __str__(self) -> str:
        """The error text of InvalidToken.

        Returns:
            str: The text that will be printed if InvalidToken is raised.
        """
        return f'The token "{self.token}" is invalid. Verify that it has correctly been added to .env.'


class InvalidDeclaration(CustomException):
    """An exception to indicate that a declaration in WORDS.md is invalid."""

    def __init__(self, string: str, line: int) -> None:
        """The initialization function of InvalidDeclaration.

        Args:
            string (str): The invalid declaration that raised this exception.
            line (int): The line of the invalid declaration that raised this exception.
        """
        self.string = string
        self.line = line
        super().__init__(self.string, self.line)

    def __str__(self) -> str:
        """The error text of InvalidDeclaration.

        Returns:
            str: The text that will be printed if InvalidDeclaration is raised.
        """
        return f'The declaration "{self.string}" line {self.line} is invalid. It contains too much ",".'

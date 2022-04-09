class CustomException(Exception):
    pass


class InvalidWord(CustomException):
    def __init__(self, word: str) -> None:
        self.message = f"The word {word} is invalid. Check for misspelling or for language compatibility with Google Search."
        super().__init__(self.message)


class InvalidLanguage(CustomException):
    def __init__(self, lang: str) -> None:
        self.message = f"The language {lang} is invalid. Verify that it can be found in SUPPORTED_LANGUAGES.md."
        super().__init__(self.message)


class InvalidDatabaseID(CustomException):
    def __init__(self, database_id: str) -> None:
        self.message = f"The database id {database_id} is invalid."
        super().__init__(self.message)


class InvalidToken(CustomException):
    def __init__(self, token: str) -> None:
        self.message = f"The token {token} is invalid."
        super().__init__(self.message)


class InvalidDeclarations(CustomException):
    def __init__(self, string: str, line: int) -> None:
        self.message = f"The declaration {string} line {line} is invalid."
        super().__init__(self.message)

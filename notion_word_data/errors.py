class CustomException(Exception):
    pass


class InvalidWord(CustomException):
    def __init__(self, word: str) -> None:
        self.word = word
        super().__init__(self.word)

    def __str__(self) -> str:
        return f'The word "{self.word}" is invalid. Check for misspelling or for language compatibility with Google Search.'


class InvalidLanguage(CustomException):
    def __init__(self, lang: str) -> None:
        self.lang = lang
        super().__init__(self.lang)

    def __str__(self) -> str:
        return f'The language "{self.lang}" is invalid. Verify that it can be found in SUPPORTED_LANGUAGES.md.'


class InvalidDatabaseID(CustomException):
    def __init__(self, database_id: str) -> None:
        self.database_id = database_id
        super().__init__(self.database_id)

    def __str__(self) -> str:
        return f'The database id "{self.database_id}" is invalid. Verify that it has correctly been added to .env.'


class InvalidToken(CustomException):
    def __init__(self, token: str) -> None:
        self.token = token
        super().__init__(self.token)

    def __str__(self) -> str:
        return f'The token "{self.token}" is invalid. Verify that it has correctly been added to .env.'


class InvalidDeclaration(CustomException):
    def __init__(self, string: str, line: int) -> None:
        self.string = string
        self.line = line
        super().__init__(self.string, self.line)

    def __str__(self) -> str:
        return f'The declaration "{self.string}" line {self.line} is invalid. It contains too much ",".'

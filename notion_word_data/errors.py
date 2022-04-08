class InvalidWord(Exception):
    def __init__(self, word: str) -> None:
        self.message = f"The word {word} is invalid. Check for misspelling or for language compatibility with Google Search."
        super().__init__(self.message)


class InvalidLanguage(Exception):
    def __init__(self, lang: str) -> None:
        self.message = f"The language {lang} is invalid. Verify that it can be found in SUPPORTED_LANGUAGES.md"
        super().__init__(self.message)

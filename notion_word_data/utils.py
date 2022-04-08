@staticmethod
def prettify(something: str) -> str:
    return (
        something.strip().capitalize()
        if "‘" and "’" not in something
        else something.strip()
    )


@staticmethod
def dict_get_element_by_index(dictionary: dict, index: int) -> str:
    return list(dictionary.keys())[index]

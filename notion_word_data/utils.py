"""A custom module for utility functions."""


@staticmethod
def prettify(something: str) -> str:
    """Get the prettified version of an expression.

    Args:
        something (str): The expression you want to prettify.

    Returns:
        str: The prettified expression.
    """
    return (
        something.strip().capitalize()
        if "‘" and "’" not in something
        else something.strip()
    )


@staticmethod
def dict_get_element_by_index(dictionary: dict, index: int) -> str:
    """Get the key of a dictionary from an index.

    Args:
        dictionary (dict): The dictionary you want to find a key from.
        index (int): The key index you want to find.

    Returns:
        str: The value corresponding to the key index given.
    """
    return list(dictionary.keys())[index]

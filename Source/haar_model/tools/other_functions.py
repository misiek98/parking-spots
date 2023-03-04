import json


def load_config(path: str) -> dict:
    """
    Function load_config takes a JSON file, loads it  
    and returns the object as dictionary.

    path: path to JSON file.visu.
    """
    with open(path, encoding='utf8') as cfg:
        config = json.load(cfg)
    return config

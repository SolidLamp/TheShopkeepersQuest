"""Handles most TOML operations in the SHM Engine.

Uses tomllib, and read-only. Requires Python 3.11+

Typical usage example:

toml_dict = toml_reader.read_toml("config.toml")
gamedata = toml_reader.read_gamedata("game.toml")
"""

import os
import tomllib
from itertools import chain
from pathlib import Path
from typing import Any, TypeVar, overload

from src.typing import FormatDict, Room


def read_toml(file: str = "game.toml", abs_path: bool = False) -> dict[Any, Any]:
    """Reads a TOML file.

    Args:
        file (str, optional):
        The path to the TOML file which will be read.
        Defaults to "game.toml".

        abs_path (bool, optional):
        If true, the path to the file will be interpreted as absolute.
        Otherwise, the path will be interpreted as relative to this directory.
        Defaults to False.

    Returns:
        dict[Any, Any]:
        A dictionary representation of the TOML file.
    """
    if not abs_path:
        file: str = os.path.join(os.path.dirname(__file__), file)
    if not os.path.exists(file):
        return {}
    else:
        with open(file, "rb") as f:
            gamedata = tomllib.load(f).copy()
        return gamedata


@overload
def replace_text(text: str) -> str: ...


@overload
def replace_text(text: list[str]) -> list[str]: ...


T = TypeVar("T")


def replace_text(text: T) -> T:
    r"""Converts escaped ANSI escape codes to non-escaped variants.

    Accepts both strings and lists of strings as input - invalid inputs,
    including that of lists with types other than strings, will result in
    TypeError being raised. It is guaranteed that the output type will be
    identical to that of the input type.

    Supported ANSI escape codes:
        - "\a"
        - "\b"
        - "\f"
        - "\n"
        - "\r"
        - "\t"
        - "\v"
        - "\033"
        - "\x1b"
        - "\x1B"
        - "\X1b"
        - "\X1B"

    Args:
        text (str | list[str]):
            The input text - either a string or a list of strings - containing
            escaped (or 'cooked') ANSI escape codes.

    Returns:
        str | list[str]:
            The text converted to raw ANSI escape codes. If the input is
            invalid, simply returns the input.

    Raises:
        TypeError: The input was of incorrect type.
    """
    ESCAPE_CHARS: dict[str, str] = {
        "\\a": "\a",
        "\\b": "\b",
        "\\f": "\f",
        "\\n": "\n",
        "\\r": "\r",
        "\\t": "\t",
        "\\v": "\v",
        "\\033": "\033",
        "\\x1b": "\033",
        "\\x1B": "\033",
        "\\X1b": "\033",
        "\\X1B": "\033",
    }

    if not (isinstance(text, str) or isinstance(text, list)):
        raise TypeError(
            f"Invalid type ({type(text).__name__}) provided as str.\n"
            + f"Provided Input: {text}"
        )
    if isinstance(text, str):
        text = _replace_text_str(text, ESCAPE_CHARS)
    if isinstance(text, list):
        text = _replace_text_list(text, ESCAPE_CHARS)
    return text


def _replace_text_str(text: str, mapping_table: dict[str, str]) -> str:
    """Replaces text within a single string via a mapping table.

    Internal use only

    Args:
        text (str): The string to map onto
        mapping_table (dict[str, str]): A table of substrings to map to.

    Returns:
        str: The input string mapped via the table.

    Raises:
        TypeError: Raised if text is not a str value.
    """

    if not isinstance(text, str):
        raise TypeError(
            f"Invalid type ({type(text).__name__}) provided as str.\n"
            + f"Provided Input: {text}"
        )
    for k, v in mapping_table.items():
        text: str = text.replace(k, v)
    return text


def _replace_text_list(strings: list[str], mapping_table: dict[str, str]) -> list[str]:
    """Replaces text within a list of strings via a mapping table.

    Internal use only

    Args:
        strings (list[str]): A list of strings to convert.
        mapping_table (dict[str, str]): A table of substrings to map to.

    Returns:
        list[str]: A list of strings, with each string mapped via the table.

    Raises:
        TypeError: Raised if strings contains a non-str value.
    """
    for k, v, i in chain.from_iterable(
        ((k, v, i) for k, v in mapping_table.items()) for i in range(len(strings))
    ):
        if not isinstance(strings[i], str):
            raise TypeError(
                f"Invalid type ({type(strings[i]).__name__}) provided as str.\n"
                + f"Provided Input: {strings[i]}"
            )
        strings[i] = strings[i].replace(k, v)
    return strings


def ansi_replace(gamedata: dict[int | str, Room]) -> dict[int | str, Room]:
    """Goes through all strings and un-escapes their ANSI codes.

    Keys affected:
        - Text
        - AlternateText
        - Desc
        - ItemText
        - KeyItemText
        - ShopEntrance
        - ShopExit
        - BattleText
        - Options

    Args:
        gamedata (dict[int | str, Room]): A dict of rooms as defined for SHM
        1.2, containing escaped ANSI codes in strings.

    Returns:
        (dict[int | str, Room]): A dict of rooms as defined for SHM 1.2,
        containing unescaped ANSI codes in strings.
    """
    str_keys: list[str] = [
        "Text",
        "AlternateText",
        "Desc",
        "ItemText",
        "KeyItemText",
        "ShopEntrance",
        "ShopExit",
        "BattleText",
        "Options",
    ]

    for key, room_id in chain.from_iterable(
        ((key, room_id) for key in str_keys) for room_id in gamedata
    ):
        room: Room = gamedata[room_id]
        if key in room:
            room[key] = replace_text(room[key])
    return gamedata


def strtoint_key(gamedata: dict[int | str, Room]) -> dict[int, Room]:
    """Converts all string keys to integer keys, and all non-int keys are dropped.

    Args:
        gamedata (dict[int, Room]): SHM 1.2-compatible dict of Rooms
        containing str or int keys.

    Returns:
        dict[int, Room]: SHM 1.2-compatible dict of Rooms containing only int
        keys.
    """
    new_gamedata = {}
    for key in gamedata.keys():
        try:
            new_key = int(key)
            new_gamedata.update({new_key: gamedata[key]})
        except ValueError:
            continue
    return new_gamedata


def read_gamedata(file: str = "game.toml", abs_path: bool = False) -> dict[Any, Any]:
    """Reads gamedata from a TOML file.

    Args:
        file (str, optional):
        The path to the gamedata TOML file which will be read.
        Defaults to "game.toml".

        abs_path (bool, optional):
        If true, the path to the file will be interpreted as absolute.
        Otherwise, the path will be interpreted as relative to this directory.
        Defaults to False.

    Returns:
        dict: The parsed game data as a Python dictionary.
    """
    if not abs_path:
        file: str = os.path.join(os.path.dirname(__file__), file)
        file: str = os.path.abspath(file)
    if not os.path.exists(file):
        return {}
    else:
        gamedata = read_toml(file, abs_path=True)
        ansi_replace(gamedata)
        gamedata = strtoint_key(gamedata)
        return gamedata


def get_engine_info(
    infoString: str = "{Name} {MajorVersion}{PatchConnector}{Patch}",
) -> str:
    """Provides information about the engine, as from engine_info.toml

    Args:
        infoString (str, optional):
        The string to format with engine_info, using replaceable keys.
        Defaults to "{Name} {MajorVersion}{PatchConnector}{Patch}".

    Returns:
        str: The string after all keys have been replaced.
    """
    engineInfo = read_toml("engine_info.toml")
    engineInfo = FormatDict(engineInfo)
    if not engineInfo["Patch"] or engineInfo["Patch"][0] == "-":
        engineInfo["PatchConnector"] = ""
    else:
        engineInfo["PatchConnector"] = " "
    infoString = infoString.format_map(engineInfo)
    return infoString

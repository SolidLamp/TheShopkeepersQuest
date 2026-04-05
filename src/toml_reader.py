"""Handles most TOML operations in the SHM Engine.

Uses tomllib, and read-only. Requires Python 3.11+

Typical usage example:

toml_dict = toml_reader.read_toml("config.toml")
gamedata = toml_reader.read_gamedata("game.toml")
"""

import os
import tomllib
from pathlib import Path
from typing import Any

from src.typing import FormatDict

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


def replace_text(text: str) -> str:
    r"""Converts escaped ANSI escape codes to non-escaped variants.

    Supported ANSI escape codes:
        * "\a"
        * "\b"
        * "\f"
        * "\n"
        * "\r"
        * "\t"
        * "\v"
        * "\033"
        * "\x1b"
        * "\x1B"
        * "\X1b"
        * "\X1B"


    Args:
        text (str): A string containing escaped ANSI escape codes.

    Returns:
        str: The same string with non-escaped ANSI escape codes.
    """
    escape_chars: dict[str, str] = {
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
    for k, v in escape_chars.items():
        text: str = text.replace(k, v)
    return text


def ansi_replace(gamedata: dict) -> dict:
    """
    Goes through all strings and un-escapes their ANSI codes.

    Args:
        gamedata (dict): SHM 1.2 gamedata containing escaped ANSI codes.

    Returns:
        dict: SHM 1.2 gamedata containing unescaped ANSI codes.
    """
    for i in gamedata:
        if "Text" in gamedata[i]:
            gamedata[i]["Text"] = replace_text(gamedata[i]["Text"])

        if "AlternateText" in gamedata[i]:
            gamedata[i]["AlternateText"] = replace_text(gamedata[i]["AlternateText"])

        if "ItemText" in gamedata[i]:
            gamedata[i]["ItemText"] = replace_text(gamedata[i]["ItemText"])

        if "KeyItemText" in gamedata[i]:
            gamedata[i]["KeyItemText"] = replace_text(gamedata[i]["KeyItemText"])

        if "Desc" in gamedata[i]:
            gamedata[i]["Desc"] = replace_text(gamedata[i]["Desc"])

        if "Options" in gamedata[i]:
            for option in gamedata[i]["Options"]:
                option = replace_text(option)
    return gamedata


def strtoint_key(gamedata: dict) -> dict:
    """
    Converts all string keys to integer keys, and all non-int keys are dropped.

    Args:
        gamedata (dict): SHM 1.2-compatible gamedata containing str | int keys.

    Returns:
        dict: SHM 1.2-compatible gamedata containing only int keys.
    """
    new_gamedata = {}
    for key in gamedata.keys():
        if key.isdigit():
            new_key = int(key)
            new_gamedata.update({new_key: gamedata[key]})
    return new_gamedata


def read_gamedata(file: str = "game.toml", abs_path: bool = False) -> dict[Any, Any]:
    """
    Reads gamedata from a TOML file.

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
    """_summary_

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

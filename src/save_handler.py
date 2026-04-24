import json
import os.path
import shutil
import unicodedata
import uuid
from datetime import datetime
from typing import Any

from src.typing import GameInfo, Save


def save_validifier(saveFile: Save) -> bool:
    if not isinstance(saveFile, dict):
        return False
    if "Game" not in saveFile or not isinstance(saveFile["Game"], str):
        return False
    if "game_state" not in saveFile or not isinstance(saveFile["game_state"], dict):
        return False
    if "RoomID" not in saveFile or not isinstance(saveFile["RoomID"], int):
        return False
    if "History" not in saveFile or not isinstance(saveFile["History"], list):
        return False
    return True


def remove_extension(file_name: str) -> str:
    file_name.removesuffix(".json")
    file_name.removesuffix(".save")
    file_name.removesuffix(".sav")
    return file_name


def read_json(file_name: str = "file.json") -> dict[Any, Any]:
    """Reads json from a the file `file_name`"""
    if not os.path.exists(file_name):
        return {}
    else:
        with open(file_name, "rt") as f:
            gamedata = json.load(f).copy()
        return gamedata


def read_save(file_name: str = "game") -> Save:
    """
    Reads the save from {game}.sav.
    file_name should not include the .sav file extension
    """
    file_name = remove_extension(file_name)
    file_name += ".sav"
    gamedata: dict[Any, Any] = read_json(file_name)
    casted_gamedata: Save = Save(**gamedata)
    return casted_gamedata


def normalise_type(value: Any) -> int | float | str | bool | list | dict | None:
    NORMALISED_TYPES = (int, float, str, bool, list, dict)
    if isinstance(value, NORMALISED_TYPES):
        return value
    if hasattr(value, "__int__"):
        return int(value)
    if hasattr(value, "__float__"):
        return float(value)
    if hasattr(value, "__str__"):
        return str(value)
    if hasattr(value, "__bool__"):
        return bool(value)
    if hasattr(value, "__iter__"):
        return list(value)
    if hasattr(value, "__dict__"):
        return dict(value)
    else:
        return None


def filename_compat(file_name: str) -> str:
    illegal_chars = str.maketrans(r'\/?%*:|"<>,;= ', "..._._.___.._.")
    file_name = file_name.translate(illegal_chars)
    file_name = "".join(ch for ch in file_name if unicodedata.category(ch)[0] != "C")
    file_name = file_name.encode(encoding="ascii", errors="ignore").decode()
    return file_name


def write_json(saveFile: str, file_name: str = "game.sav") -> None:
    """file_name should include the file extension"""
    file_name = os.path.normpath(file_name)
    file_name = filename_compat(file_name)
    with open(file_name, "wt") as f:
        f.write(saveFile)


def write_save(
    game_state,
    gameInfo: GameInfo,
    room: int,
    history: list[int],
    file_name: str = "game",
    save_version: int = 0,
    game_id: str | uuid.UUID | None = None,
    save_id: str | uuid.UUID | None = None,
    shop_exit: int = -1,
) -> None:
    """file_name should not include the .sav file extension"""
    file_name = remove_extension(file_name)
    existing_save = read_save(file_name)
    if existing_save and existing_save.get("save_id", "2") != save_id:
        new_suffix: str = existing_save.get("Saved", "copy")
        copy_save(file_name, new_suffix)
    file_name += ".sav"

    json_game_state = {
        k: normalise_type(v) for k, v in game_state.__dict__.copy().items()
    }

    dictionary = {
        "Game": gameInfo["title"],
        "Saved": datetime.now().isoformat(),
        "save_version": save_version,
        "RoomID": room,
        "History": history,
        "shop_exit": shop_exit,
        "game_state": json_game_state,
    }
    if "inventory" in json_game_state:
        json_game_state.pop("inventory")
        dictionary.update({"inventory": game_state.__dict__["inventory"].__dict__})
    if game_id:
        dictionary.update({"game_id": game_id})
    if save_id:
        dictionary.update({"save_id": save_id})
    else:
        dictionary.update({"save_id": str(uuid.uuid4())})
    output = json.dumps(dictionary, indent=4)
    write_json(output, file_name)


def copy_save(file_name: str, new_suffix: str) -> None:
    """
    Copies an existing

    Args:
        file_name (str): The file name of the existing file to copy.
        new_suffix (str): A suffix to be appended to the end of the file name.
    """
    file_name: str = remove_extension(file_name)
    old_save: str = os.path.abspath(file_name + ".sav")
    old_copy: str = os.path.abspath(file_name) + "-" + new_suffix + ".sav"
    old_copy = filename_compat(old_copy)
    shutil.copyfile(old_save, old_copy)

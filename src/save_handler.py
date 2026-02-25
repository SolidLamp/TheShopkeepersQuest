from datetime import datetime
import json
import os.path
import shutil
import uuid


def save_validifier(saveFile: dict) -> bool:
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


def read_json(file_name: str = "file.json") -> dict:
    """Reads json from a the file `file_name`"""
    if not os.path.exists(fileName):
        return {}
    else:
        with open(fileName, "rt") as f:
            gamedata = json.load(f).copy()
        return gamedata


def read_save(file_name: str = "game") -> dict:
    """
    Reads the save from {game}.sav.
    fileName should not include the .sav file extension
    """
    file_name = remove_extension(file_name)
    file_name += ".sav"
    gamedata = read_json(file_name)
    return gamedata


def write_json(saveFile: str, fileName: str = "game.sav") -> None:
    """fileName should include the file extension"""
    with open(fileName, "wt") as f:
        f.write(saveFile)


def write_save(
    game_state,
    gameInfo: dict,
    room: int,
    history: list[int],
    file_name: str = "game",
    save_version: int = 0,
    game_id: str | uuid.UUID | None = None,
    save_id: str | uuid.UUID | None = None,
) -> None:
    """file_name should not include the .sav file extension"""
    file_name = remove_extension(file_name)
    existing_save = read_save(file_name)
    if existing_save and existing_save.get("save_id", "2") != save_id:
        copy_save(file_name, existing_save)
    file_name += ".sav"
    dictionary = {
        "Game": gameInfo["title"],
        "Saved": datetime.now().isoformat(),
        "save_version": save_version,
        "RoomID": room,
        "History": history,
        "game_state": game_state.__dict__.copy(),
    }
    if "inventory" in dictionary["game_state"]:
        dictionary["game_state"].pop("inventory")
        dictionary.update({"inventory": game_state.__dict__["inventory"].__dict__})
    if game_id:
        dictionary.update({"game_id": game_id})
    if save_id:
        dictionary.update({"save_id": save_id})
    else:
        dictionary.update({"save_id": str(uuid.uuid4())})
    output = json.dumps(dictionary, indent=4)
    write_json(output, fileName)


def copy_save(file_name: str, existing_save: dict) -> None:
    file_name = remove_extension(file_name)
    old_save = os.path.abspath(file_name + ".sav")
    old_copy = (
        os.path.abspath(file_name) + "-" + existing_save.get("Saved", "copy") + ".sav"
    )
    shutil.copyfile(old_save, old_copy)

from datetime import datetime
import json
import os.path
import shutil
import uuid


def write_save(
    game_state,
    gameInfo: dict,
    room: int,
    history: list[int],
    fileName: str = "game",
    save_version: int = 0,
    game_id: str | uuid.UUID | uuid.SafeUUID | None = None,
    save_id: str | uuid.UUID | uuid.SafeUUID | None = None,
) -> None:
    """fileName should not include the .sav file extension"""
    existing_save = read_save(fileName)
    if existing_save and existing_save.get("save_id", "2") != save_id:
        copy_save(fileName, existing_save)
    fileName = fileName + ".sav"
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
        # e.g. 164237f8-d3ce-46b2-95b1-b30d39ce4472
    output = json.dumps(dictionary, indent=4)
    write_json(output, fileName)


def write_json(saveFile: str, fileName: str = "game.sav") -> None:
    """fileName should include the file extension"""
    with open(fileName, "wt") as f:
        f.write(saveFile)


def read_save(gameName: str = "game") -> dict:
    """fileName should not include the .sav file extension"""
    fileName = gameName + ".sav"
    if not os.path.exists(fileName):
        return {}
    else:
        with open(fileName, "rt") as f:
            gamedata = json.load(f).copy()
        return gamedata


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


def copy_save(file_name: str, existing_save: dict) -> None:
    old_save = os.path.abspath(file_name + ".sav")
    old_copy = (
        os.path.abspath(file_name) + existing_save.get("Saved", " - Copy") + ".sav"
    )
    shutil.copyfile(old_save, old_copy)

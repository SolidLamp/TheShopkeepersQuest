from datetime import datetime
import json
import os.path


def write_save(
    game_state, gameInfo: dict, room: int, history: list[int], fileName: str = "game"
) -> None:
    dictionary = {
        "Game": gameInfo["title"],
        "Saved": datetime.now().isoformat(),
        "game_state": game_state.__dict__.copy(),
        "RoomID": room,
        "History": history,
    }
    if "inventory" in dictionary["game_state"]:
        dictionary["game_state"].pop("inventory")
        dictionary.update({"inventory": game_state.__dict__["inventory"].__dict__})
    output = json.dumps(dictionary, indent=4)
    fileName = fileName + ".sav"
    write_json(output, fileName)


def write_json(saveFile: str, fileName: str = "game.sav") -> None:
    with open(fileName, "wt") as f:
        f.write(saveFile)


def read_save(gameName: str = "game") -> dict:
    fileName = gameName + ".sav"
    if not os.path.exists(fileName):
        return {}
    else:
        with open(fileName, "rt") as f:
            gamedata = json.load(f).copy()
        return gamedata


def save_validifier(saveFile: dict) -> bool:
    return (
        "Game" in saveFile
        and "game_state" in saveFile
        and "RoomID" in saveFile
        and "History" in saveFile
    )

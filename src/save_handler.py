import json
import os.path


def write_save(game_state, gameInfo: dict, room: int, gameName: str = "game") -> None:
    dictionary = {"Game": gameInfo["title"]}
    dictionary.update({"game_state": game_state.__dict__.copy()})
    if "inventory" in dictionary["game_state"]:
        dictionary["game_state"].pop("inventory")
        dictionary.update({"inventory": game_state.__dict__["inventory"].__dict__})
        dictionary.update({"RoomID": room})
    output = json.dumps(dictionary, indent=4)
    fileName = gameName + ".sav"
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


def saveValidifier(saveFile: str) -> bool:
    "Game" in saveFile
    "game_state" in saveFile
    "RoomID" in saveFile

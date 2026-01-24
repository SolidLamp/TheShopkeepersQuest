import json
import os
import game


def write_save(game_state: game.gameState, gameInfo: dict, room: int) -> None:
    dictionary = {"Game": gameInfo["title"]}
    dictionary.update({"game_state": game_state.__dict__.copy()})
    if "inventory" in dictionary["game_state"]:
        dictionary["game_state"].pop("inventory")
        dictionary.update(
            {"inventory": game_state.__dict__["inventory"].__dict__}
            )
        dictionary.update(
            {"RoomID": room}
            )
    output = json.dumps(dictionary, indent=4)
    write_json(output)


def write_json(output: str) -> None:
    with open("game.sav", "wt") as f:
        f.write(output)


def read_save() -> dict:
    if not os.path.exists("game.sav"):
        return {}
    else:
        with open("game.sav", "rt") as f:
            gamedata = json.load(f).copy()
        return gamedata

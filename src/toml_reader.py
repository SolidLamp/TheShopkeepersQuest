import os
import tomllib


def replace_text(text: str) -> str:
    text = text.replace("\\n", "\n")
    text = text.replace("\\033", "\033")
    return text


def ansi_replace(gamedata: dict) -> dict:
    for i in gamedata:
        if "Text" in gamedata[i]:
            gamedata[i]["Text"] = replace_text(gamedata[i]["Text"])
        if "Options" in gamedata[i]:
            for option in gamedata[i]["Options"]:
                option = replace_text(option)
    return gamedata


def strtoint_key(gamedata: dict) -> dict:
    new_gamedata = {}
    for key in gamedata.keys():
        if key.isdigit():
            new_key = int(key)
            new_gamedata.update({new_key: gamedata[key]})
            del new_key
    return new_gamedata


def read_toml(file: str = "game.toml") -> dict:
    if not os.path.exists(file):
        return {}
    else:
        with open(file, "rb") as f:
            gamedata = tomllib.load(f).copy()
        return gamedata

def read_gamedata(file: str = "game.toml") -> dict:
    if not os.path.exists(file):
        return {}
    else:
        gamedata = read_toml(file)
        ansi_replace(gamedata)
        gamedata = strtoint_key(gamedata)
        return gamedata
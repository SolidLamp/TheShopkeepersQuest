import os
import tomllib

# \[\]\[\]\[\033[01;34m\]\w\[\033[00m\]$ \[\]


def replace_text(text: str):
    text = text.replace("\\n", "\n")
    text = text.replace("\\033", "\033")
    return text


def ansi_replace(gamedata: dict):
    for i in gamedata:
        if "Text" in gamedata[i]:
            gamedata[i]["Text"] = replace_text(gamedata[i]["Text"])
        if "Options" in gamedata[i]:
            for option in gamedata[i]["Options"]:
                option = replace_text(option)
    return gamedata


def strtoint_key(gamedata: dict):
    new_gamedata = {}
    for key in gamedata.keys():
        if key.isdigit():
            new_key = int(key)
            new_gamedata.update({new_key: gamedata[key]})
            del new_key
    return new_gamedata


def read_toml():
    if not os.path.exists("game.toml"):
        return {}
    else:
        with open("game.toml", "rb") as f:
            gamedata = tomllib.load(f).copy()
            ansi_replace(gamedata)
            gamedata = strtoint_key(gamedata)
        return gamedata

import os
import tomllib


class formatDict(dict):
    def __missing__(self, key: str) -> str:
        string = "{" + key + "}"
        return string


def read_toml(file: str = "game.toml") -> dict:
    if not os.path.exists(file):
        return {}
    else:
        with open(file, "rb") as f:
            gamedata = tomllib.load(f).copy()
        return gamedata


def replace_text(text: str) -> str:
    text = text.replace("\\n", "\n")
    text = text.replace("\\033", "\033")
    return text


def ansi_replace(gamedata: dict) -> dict:
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
    new_gamedata = {}
    for key in gamedata.keys():
        if key.isdigit():
            new_key = int(key)
            new_gamedata.update({new_key: gamedata[key]})
            del new_key
    return new_gamedata


def read_gamedata(file: str = "game.toml") -> dict:
    if not os.path.exists(file):
        return {}
    else:
        gamedata = read_toml(file)
        ansi_replace(gamedata)
        gamedata = strtoint_key(gamedata)
        return gamedata


def get_engine_info(
    infoString: str = "{Name} {MajorVersion}{PatchConnector}{Patch}",
) -> str:
    engineInfo = read_toml("engine_info.toml")
    engineInfo = formatDict(engineInfo)
    if not engineInfo["Patch"] or engineInfo["Patch"][0] == "-":
        engineInfo["PatchConnector"] = ""
    else:
        engineInfo["PatchConnector"] = " "
    infoString = infoString.format_map(engineInfo)
    return infoString

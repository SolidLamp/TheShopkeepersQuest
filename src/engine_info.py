import toml_reader


class formatDict(dict):
    def __missing__(self, key: str) -> str:
        string = "{" + key + "}"
        return string


def get(infoString: str = "{Name} {MajorVersion}{PatchConnector}{Patch}") -> str:
    engineInfo = toml_reader.read_toml("engine_info.toml")
    engineInfo = formatDict(engineInfo)
    if not engineInfo["Patch"] or engineInfo["Patch"][0] == "-":
        engineInfo["PatchConnector"] = ""
    else:
        engineInfo["PatchConnector"] = " "
    infoString = infoString.format_map(engineInfo)
    return infoString

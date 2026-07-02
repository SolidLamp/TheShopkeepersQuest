#!/usr/bin/env python3
"""The entry point for the program.

This should never be used outside of being entry point for the module.
"""

import os
import platform
import sys
from importlib.resources import files

from shm import toml_reader  # title
from shm.typing import FormatDict


def display_help_menu() -> None:
    module_path: str = str(files(__spec__.parent))
    toml_path: str = os.path.join(module_path, "engine_info.toml")

    gameInfo = toml_reader.read_toml(toml_path)
    gameInfo = FormatDict(gameInfo)

    if not gameInfo["Patch"] or gameInfo["Patch"][0] == "-":
        gameInfo["PatchConnector"] = ""
    else:
        gameInfo["PatchConnector"] = " "

    infoString = (
        "{Name}{PatchConnector} {MajorVersion}{Patch}\n{ReleaseDate}"
        "\n{Licence}\nCreated by {Creator}\n{Link}"
    )
    infoString = infoString.format_map(gameInfo)
    print(infoString)
    print("\n-h | --help | --about  --  opens this menu")


def main() -> None:
    """The main function to be loaded. Handles arguments. Loads title screen."""
    if platform.system() != "Windows" and os.getuid() == 0:
        print("\033[31mCritical Error: root should not be running user processes")
        sys.exit(1)

    if len(sys.argv) > 1:
        for arg in sys.argv:
            match arg:
                case "--about" | "--help" | "-h":
                    display_help_menu()
        sys.exit(0)
    else:
        display_help_menu()
        sys.exit(0)


if __name__ == "__main__":
    main()

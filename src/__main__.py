#!/usr/bin/env python3
"""The entry point for the program.

This should never be used outside of being entry point for the module.
"""

import os
import platform
import sys

from src import title, toml_reader
from src.typing import FormatDict


def main() -> None:
    """The main function to be loaded. Handles arguments. Loads title screen."""
    if platform.system() != "Windows" and os.getuid() == 0:
        print("\033[31mCritical Error: root should not be running user processes")
        sys.exit(1)

    if len(sys.argv) > 1:
        for arg in sys.argv:
            match arg:
                case "--about" | "--help" | "-h":
                    gameInfo = toml_reader.read_toml("cli_info.toml")
                    gameInfo = FormatDict(gameInfo)
                    if not gameInfo["Patch"] or gameInfo["Patch"][0] == "-":
                        gameInfo["PatchConnector"] = ""
                    else:
                        gameInfo["PatchConnector"] = " "
                    infoString = (
                        "{Name}{PatchConnector}{Version}\n{ReleaseDate}"
                        "\n{Licence}\nCreated by {Creator}\n{Link}"
                    )
                    infoString = infoString.format_map(gameInfo)
                    print(infoString)
                    print(
                        "\n-h | --help | --about  --  opens this menu\n[no args]  --  runs the game"
                    )
        sys.exit(0)
    else:
        title.title()


if __name__ == "__main__":
    main()

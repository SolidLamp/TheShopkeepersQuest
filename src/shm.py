"""The main SHM Engine.

After loading the SHM Engine, all execution will be offloaded to it.
Does not return, but will terminate the program with sys.exit().
Most usage should be shm.run(), which handles setting up MainHandler
automatically.

Typical usage example:

shm.run(win, starting_room=1, gameFile_name="game", gameFile_path="./")
"""

import curses
import os.path
import platform
import re
from src.typing.box import Box
from src.typing.box import Box
from src.typing.box import Box
import sys
import time
from collections.abc import Callable
from datetime import datetime
from importlib.machinery import ModuleSpec
from importlib.util import module_from_spec, spec_from_file_location
from itertools import chain
from random import randrange as rand
from types import ModuleType
from typing import Any

from src import save_handler, toml_reader, tui
from src.battle import BattleHandler
from src.tui import print3
from src.typing import (
    BattleHooks,
    BattleItem,
    Box,
    Enemy,
    EngineInfo,
    FormatDict,
    Save,
)

HISTORY_MAX_LEN: int = 10
AUTOMOVE_DELAY: float = 1.0
ENDING_DELAY: float = 0.5


class MainHandler:
    """The main heart of the SHM Engine."""

    def __init__(
        self,
        win: curses.window,
        starting_room: int | None = None,
        saveFile: Save | None = None,
        gameFile_name: str = "game",
        gameFile_path: str = "./game.py",
        saveFileName: str = "game",
    ) -> None:
        """Set up an instance of the SHM Engine with a given gamefile.

        Args:
            win (curses.window):
            A curses window instance.

            starting_room (int | None, optional):
            When specified, the engine starts within that room ID.
            If None, uses the starting_room within the gamefile.
            Defaults to None.

            saveFile (Save | None, optional):
            The save file.
            Defaults to None.

            gameFile_name (str, optional):
            The name of the module name which corresponds to the gamefile to
            be loaded.
            Defaults to "game".

            gameFile_path (str, optional):
            The file path of the gamefile to be loaded.
            Accepts both relative and absolute paths.
            If the file extension is not specified, defaults to ".py"
            Defaults to "./game.py".

            saveFileName (str, optional):
            The name of the save file to write to when the game is saved.
            Defaults to "game".
        """
        self.COMPATIBLE_COMPLEVELS: list[int] = [1, 2]
        self.current_saveid: int | str | None = None
        self.engineInfo: FormatDict = FormatDict(
            toml_reader.read_toml("engine_info.toml")
        )
        self.game: ModuleType = self.setup_gameFile(gameFile_name, gameFile_path)
        self.gameFile_name: str = gameFile_name
        self.gameInfo: dict[str, Any] = self.game.gameInfo
        self.game_state: Any = self.game.game_state
        self.globaldebug: bool = False
        self.history: list[int] = self.game.history
        self.room: dict[str, Any] = {}
        self.saveFileName: str = saveFileName
        self.SHMversion: str = toml_reader.get_engine_info()
        self.shop_exit: int = -1
        self.starting_room: int = self.gameInfo.get("starting_room", 1)
        self.stdscr: curses.window = win
        self.text_speed: float = self.gameInfo.get("default_textspeed", 0.01)
        self.win: curses.window = win
        self.setup_stdscr()

        if starting_room:
            self.roomID: int = starting_room
        else:
            self.roomID: int = self.starting_room

        if saveFile:
            self.setup_loadSave(saveFile)

        if hasattr(self.game, "battle_hooks"):
            self.battle_hooks: BattleHooks = self.game.battle_hooks
        else:
            self.battle_hooks: dict[None, None] = {}

    def setup_gameFile(self, module_name: str, file_path: str) -> ModuleType:
        """The method which handles importing the .py gamefile.

        Uses importlib.util to dynamically load a Python module, which should
        correspond to the desired gamefile to load.
        The imported module is then returned, so that it can be available
        outside of this method and publicly available within the class.

        Args:
            module_name (str): The name of the module to import.
            file_path (str): The path of the module to import.

        Returns:
            ModuleType: The module which has just been imported.

        Raises:
            ImportError: The specified module could not be imported.
        """
        file_path = os.path.abspath(file_path)
        if file_path[-3:] != ".py":
            file_path = os.path.join(file_path, module_name)
            file_path = file_path + ".py"
        spec: ModuleSpec | None = spec_from_file_location(
            name=module_name,
            location=file_path,
            submodule_search_locations=[os.path.dirname(file_path)],
        )
        try:
            module: ModuleType = module_from_spec(spec)  # pyright: ignore
        except:
            raise ImportError("Failed to import game file")
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # pyright: ignore
        return module

    def setup_loadSave(self, saveFile: Save | None) -> bool:
        """Sets up the current game state based on the save file provided.

        The save file is a dictionary in the Save format (see typing), and
        should already be loaded from a file. This function only handles
        interpreting the save file. The save file should correspond to the
        current game_state,  which should already be set up. However, the
        UUID and title of the game, as stored in the save file, are both
        checked so that they match the current loaded gamefile. A save file
        with the UUID and title of a game that does not correspond to the
        gamefile with the same identifiers will cause unexpected behaviour.
        Automatically handles if an attribute is Box[int] or Box[float],
        although

        Args:
            saveFile (Save | None): A dictionary in the Save format.

        Returns:
            bool: Indicates if loading the save file was successful.
        """

        if not isinstance(saveFile, dict):
            return False

        game_id = self.gameInfo.get("game_id")
        if (
            saveFile.get("game_id", game_id) != game_id
            or saveFile["Game"] != self.gameInfo["title"]
        ):
            self.err_log_error(
                error_type="Error",
                error_msg="The save file does not correspond to the current game. "
                + "Continuing without save file...",
            )
            self.roomID = self.starting_room
            return False

        self.history.extend(saveFile["History"])
        self.shop_exit = saveFile.get("shop_exit", -1)

        # Test for if the given attribute is a box.

        for item in saveFile["game_state"]:
            if not hasattr(self.game_state, item):
                continue
            if type(getattr(self.game_state, item)) != Box:
                setattr(self.game_state, item, saveFile["game_state"][item])
            elif type(saveFile["game_state"][item]) == int:
                boxed_item = getattr(self.game_state, item)
                boxed_item -= boxed_item
                boxed_item += saveFile["game_state"][item]
            elif type(saveFile["game_state"][item]) == float:
                boxed_item = getattr(self.game_state, item)
                boxed_item -= boxed_item
                boxed_item += saveFile["game_state"][item]

        if hasattr(self.game_state, "inventory") and "inventory" in saveFile:
            for item in saveFile["inventory"]["items"]:
                self.game_state.inventory.items.append(item)
            for item in saveFile["inventory"]["keyItems"]:
                self.game_state.inventory.keyItems.append(item)

        self.current_saveid = saveFile.get("save_id", None)

        return True

    def setup_stdscr(self) -> None:
        """Sets up the main activity window, inside the border."""
        padding = 1
        padx1 = 0
        padx2 = 0
        pady1 = 0
        pady2 = 1
        self.win = tui.create_newwin(self.stdscr, padding, padx1, padx2, pady1, pady2)

    def db_debug(self) -> None:
        """Creates the debug menu and displays it to the player."""
        if "disable_debug" in self.gameInfo and self.gameInfo["disable_debug"]:
            return
        debug_options = ["Test room IDs", "Enable debug mode", "Test room attributes"]
        query = tui.option(self.win, "SHM Engine Debug Menu", debug_options)
        match query:
            case 0:
                self.db_test_roomIDs()
            case 1:
                self.globaldebug = not (self.globaldebug)
            case 2:
                self.db_test_attributes()

    def db_test_roomIDs(self) -> None:
        """Debug menu - tests room IDs and check for validity.

        Tests each room ID inside "Move" and "Automove" attributes, to check
        if they all correspond to a valid room ID within the gamefile, or if
        they correspond to the negative IDs, where they should not correspond
        to a room ID. Also notes when (history, -x)-style (complevel 1)
        negative ID references when a complevel 2 file is loaded.
        """
        text = ""
        rooms = self.game.get_rooms(self.win)
        idnos = []
        for roomno, room in rooms.items():
            if "Move" in room:
                idnos.extend((idno, roomno) for idno in room["Move"])
            if "Automove" in room:
                idnos.append((room["Automove"], roomno))
        for idno, roomno in idnos:
            if isinstance(idno, int) and idno in rooms:
                continue
            negIDv1: bool = (
                isinstance(idno, tuple) and idno[0] == "history" and idno[1] < 0
            )
            negIDv2_support: bool = not (self.game.gameInfo["complevel"] == 1)
            if negIDv1 and not negIDv2_support:
                continue
            if negIDv1 and negIDv2_support:
                text += f"\033[36mNote: Room {roomno} uses complevel 1-style"
                text += f" history ID references: {idno}\n\033[0m"
                continue
            if isinstance(idno, int) and idno < 0 and negIDv2_support:
                continue
            text += f"\033[33mWarning: Invalid ID {idno} in {roomno}!\n\033[0m"
        self.win.clear()
        if text:
            print3(self.win, text, 33, 0)
        else:
            print3(self.win, "Success! No errors found.", 32, 0)
        print3(self.win, "\nPress any key to exit Debug Menu...", 0, 0)
        self.win.getch()

    def db_test_attributes(self) -> None:
        """Debug menu - validates the types of all room attributes.

        In the current loaded gamefile, checks every attribute in every room,
        and compares the type to the correct type the attribute should have,
        and reports a notice for incorrect types.
        """
        attribute_types = {
            "Text": str,
            "Requirements": Callable,
            "AlternateText": str,
            "TextSpeed": float,
            "Desc": str,
            "titlebarCentre": str,
            "titlebarLeft": str,
            "titlebarRight": str,
            "Script": Callable,
            "Item": str,
            "ItemRequirements": Callable,
            "ItemText": str,
            "KeyItem": str,
            "KeyItemRequirements": Callable,
            "KeyItemText": str,
            "BattleText": str,
            "Enemies": list,
            "EnemyChances": list,
            "Options": list,
            "Inventory": bool | int,
            "Move": list,
            "Automove": int | tuple[str, int],
            "InstantAutomove": bool | int,
            "Lose": str,
            "Ending": str,
        }
        text = ""
        rooms = self.game.get_rooms(self.win)
        for attribute, value, roomno, room in chain.from_iterable(
            ((attribute, value, roomno, room) for attribute, value in room.items())
            for roomno, room in rooms.items()
        ):
            if attribute in attribute_types and not isinstance(
                room[attribute], attribute_types[attribute]
            ):
                text += f"\033[33mWarning: Attribute '{attribute}' in room {roomno} "
                text += f"is {type(room[attribute])}!\n\033[0m"
            if re.fullmatch(r"Option\d+Requirements", attribute):
                continue
            if attribute not in attribute_types:
                text += f"\033[33mWarning: Invalid attribute '{attribute}' in room "
                text += f"{roomno}!\n\033[0m"
        self.win.clear()
        if text:
            print3(self.win, text, 33, 0)
        else:
            print3(self.win, "Success! No errors found.", 32, 0)
        print3(self.win, "\nPress any key to exit Debug Menu...", 0, 0)
        self.win.getch()

    def err_log_error(
        self,
        error_type: str,
        error_msg: str,
    ) -> None:
        """Logs an error - displays to the user and writes to error.log.

        Args:
            error_type (str):
            The type of error to display.
            Valid values: "Alert", "Critical Error", "Error", "Warning"
            If the current gamefile has hide_warnings as True, then an error
            with the type "Warning" will only be written to error.log, and
            not visually displayed to the user.

            error_msg (str):
            The message to display to the user and write to file, explaining
            the error encountered. Should not include an error prefix (which
            should instead be provided by the error_type).
        """
        colours: dict[str, str] = {
            "Alert": "\033[36m",
            "Critical Error": "\033[31;1m",
            "Error": "\033[31m",
            "Warning": "\033[33m",
        }
        timestamp: str = datetime.now().isoformat()
        error_txt = f"{error_type}: {error_msg}\n"
        with open("error.log", "a") as log:
            log.write(f"[{timestamp}] {error_txt}")

        if self.gameInfo.get("hide_warnings", False) and error_type == "Warning":
            return

        self.win.refresh()
        self.ui_drawtitlebar(
            centreOverride=error_type, leftOverride="", rightOverride=""
        )
        print3(self.win, text=error_msg, delay=0)
        error_txt: str = colours.get(error_type, "") + error_txt
        if error_type == "Critical Error":
            tui.option(self.win, text=error_txt, options=["Exit"])
            sys.exit(1)
        else:
            tui.option(self.win, text=error_txt, options=["Dismiss"])

    def err_roomIDerror(self) -> None:
        """Handle an error when an invalid room is attempted to be loaded

        Displays an error to the user, using err_log_error(), and changes
        the current roomID to the starting_room, which should always be a
        valid room in a correct gamefile.
        """
        self.err_log_error(
            error_type="Error", error_msg=f"Invalid RoomID: {self.roomID}"
        )
        self.roomID = self.starting_room

    def ui_drawtitlebar(
        self,
        centreOverride: str | None = None,
        leftOverride: str | None = None,
        rightOverride: str | None = None,
    ) -> None:
        """Draws the titlebar and border around the main screen.

        Handles the titlebar and set up the strings to be displayed.
        The strings will be chosen by the following priority:
        1. The 'centreOverride', 'leftOverride' and 'rightOverride' arguments.
        2. The 'titlebarCentre', 'titlebarLeft' and 'titlebarRight'
        attributes within a room.
        3. The default titlebar string set within the gamefile info.
        4. Default string values if not defined.
        This method also handles the border style defined within game_info,
        which is passed to tui.draw_titlebar().

        Args:
            centreOverride (str | None, optional):
            Overrides the text displayed in the centre of the titlebar.
            Defaults to None.

            leftOverride (str | None, optional):
            Overrides the text displayed in the right corner of the titlebar.
            Defaults to None.

            rightOverride (str | None, optional):
            Overrides the text displayed in the left corner of the titlebar.
            Defaults to None.
        """
        leftString = " D - Debug Menu "
        rightString = " Q - Quit "
        if self.room and "Desc" in self.room:
            title_string = " {abbr} | {desc} "
        else:
            title_string = self.gameInfo["title"]
        if "titlebarCentre" in self.room:
            title_string = self.room["titlebarCentre"]
        elif "default_titlebar_centre" in self.gameInfo:
            title_string = self.gameInfo["default_titlebar_centre"]
        if "titlebarLeft" in self.room:
            leftString = self.room["titlebarLeft"]
        elif "default_titlebar_left" in self.gameInfo:
            leftString = self.gameInfo["default_titlebar_left"]
        if "titlebarRight" in self.room:
            rightString = self.room["titlebarRight"]
        elif "default_titlebar_right" in self.gameInfo:
            rightString = self.gameInfo["default_titlebar_right"]
        if centreOverride is not None:
            title_string = centreOverride
        if leftOverride is not None:
            leftString = leftOverride
        if rightOverride is not None:
            rightString = rightOverride
        title_string = self.ui_format_string(title_string)
        leftString = self.ui_format_string(leftString)
        rightString = self.ui_format_string(rightString)
        default_border = self.engineInfo.get("DefaultBorderStyle", 0)
        tui.draw_titlebar(
            self.stdscr,
            title=title_string,
            leftString=leftString,
            rightString=rightString,
            style=self.gameInfo.get("border_style", default_border),
        )

    def ui_ending(self, end: str) -> None:
        """Handles endings in a game, including autosaving.

        Displays the defined ending text for the specific ending, and the
        generic ending text, and saves the current game state to file.

        Args:
            end (str):
            The ending which the user has received.
            Can correspond to the endings in the endingText attribute within
            the gamefile.
        """
        titlebar_centre = "{title}"
        titlebar_left = ""
        titlebar_right = ""
        self.ui_drawtitlebar(titlebar_centre, titlebar_left, titlebar_right)
        self.roomID = self.starting_room
        self.fn_save_handler()
        if hasattr(self.game, "endingText") and end in self.game.endingText:
            print3(
                self.win,
                "\n" + self.game.endingText[end].replace("|", end),
                0,
                0.015,
                0.65,
            )
        time.sleep(1.5)
        self.win.clear()
        print3(self.win, self.game.defaultEnding.replace("|", end), 0, 0.015, 0.65)
        time.sleep(3.5)

    def ui_format_string(self, string: str) -> str:
        """Formats a string with predefined keys.

        Formats the string with the various available keys;
        used to format the titlebar and the text of rooms.
        Keys are in the format '{key}' embedded within a string.

        Supported keys:
            - 'abbr' - the abbreviation set by the gamefile, if present.
            - 'arch' - displays the architecure of the machine. Uses
            platform.machine().
            - 'date' - displays the current date in Y-M-D format.
            - 'engine_info' - displays the current version of the SHM Engine.
            - 'game_state' - the entire current game_state;
                - call child attributes of game_state; do not use it bare.
            - 'health' - displays player health (requires battle support)
            - 'iso_date' - displays the current date in iso-format.
            - 'level' - displays player level (requires battle support)
            - 'money' - displays player money
            - 'python_implementation' - displays the current Python
            implementation, e.g. CPython, PyPy. Uses
            platform.python_implementation()
            - 'python_version' - displays the current Python version
            - 'self' - displays the entire self object;
                - call child attributes of self; do not use it bare.
            - 'system' - displays the current OS, using platform.system().
            - 'time' - displays the current time in H:M.
            - 'title' - displays the game title.
            - 'utime' - displays the current time in Unix timestamp.
            - 'xp' - displays player experience (requires battle support)


        Args:
            string (str): The string to be formatted by the function.

        Returns:
            str: The output string that has been formatted.
        """
        key_dict = {
            "abbr": self.gameInfo.get("abbr", "{abbr}"),
            "arch": platform.machine(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "engine_info": self.SHMversion,
            "game_state": self.game_state,
            "iso_date": datetime.now().isoformat(),
            "money": str(getattr(self.game, "money_hook", "{money}")),
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "self": self,
            "system": platform.system(),
            "time": datetime.now().strftime("%H:%M"),
            "title": self.gameInfo.get("title", "{title}"),
            "utime": datetime.now().timestamp(),
        }
        battle_keys = {
            "health": self.battle_hooks.get("health_hook", "{health}"),
            "level": self.battle_hooks.get("level_hook", "{level}"),
            "xp": self.battle_hooks.get("exp_hook", "{xp}"),
        }
        if self.battle_hooks:
            key_dict.update(battle_keys)

        key_dict = FormatDict(key_dict)
        if self.room and "Desc" in self.room:
            key_dict["desc"] = self.room["Desc"]
        string = string.format_map(key_dict)
        return string

    def ui_lose(self, lose: str) -> None:
        """Handles losing the game.

        Displays the defined losing text for the specific loss, and the
        generic losing text.

        Args:
            lose (str):
            The loss which the user has received.
            Can correspond to the loss text is set within the gamefile,
            under the loseText attribute.
        """
        time.sleep(0.25)
        if hasattr(self.game, "loseText") and lose in self.game.loseText:
            printText = "\n" + self.game.loseText[lose].replace("|", lose)
        else:
            printText = self.game.defaultLose.replace("|", lose)
        print3(self.win, printText, 0, 0.015, 0.65)
        self.win.clear()
        time.sleep(0.5)
        query = tui.option(self.win, printText + "Try again?", ["Yes", "No"])
        if query == 1 or query == "q":
            sys.exit(0)
        else:
            self.roomID = self.starting_room

    def ui_text_handler(self) -> str:
        """Handles getting the text within a room.

        Handles the text of a room, between Text, AlternateText, etc.
        Prints the text and returns the text.

        Returns:
            str: The appropriate text of the room to be used.
        """
        text: str = ""

        # Detect if this room is a shop
        is_shop: bool = (
            "ShopItems" in self.room
            and isinstance(self.room["ShopItems"], list)
            and "ShopItemCosts" in self.room
            and isinstance(self.room["ShopItemCosts"], list)
            and "ShopEntrance" in self.room
        )

        # Decide whether the user just entered the shop
        if is_shop and self.shop_exit == self.history[-2]:
            if isinstance(self.room["ShopEntrance"], str):
                text: str = self.room["ShopEntrance"]
            elif isinstance(self.room["ShopEntrance"], list):
                random_index: int = rand(len(self.room["ShopEntrance"]))
                random_string = self.room["ShopEntrance"][random_index]
                text: str = str(random_string)

        # Check for requirements if user is not within a shop
        elif "Requirements" in self.room and not self.room["Requirements"]():
            text: str = str(self.room["AlternateText"])
        elif "Text" in self.room:
            text: str = str(self.room["Text"])

        # Get money hook to display user money if they are within a shop
        if hasattr(self.game, "money_hook") and isinstance(
            getattr(self.game, "money_hook"), Box
        ):
            money_hook: Box[int] = getattr(self.game, "money_hook")
        else:
            money_hook: Box[int] = Box(0)

        currency_name: str = str(self.gameInfo.get("currency_name", "Money"))

        if is_shop:
            text += f"\nCurrent {currency_name}: {money_hook}"

        tui.newline(self.win)
        if "\n" not in text:
            tui.centre_text(self.win, text)
        self.win.scrollok(True)
        text = self.ui_format_string(text)
        print3(self.win, text, delay=self.room.get("TextSpeed", self.text_speed))
        return text

    def ui_option(self, text: str, options: list[str], Inventory: bool = True) -> int:
        """Handle options for the SHM Engine, as a wrapper for tui.option();

        Should be used for most operations, for user interaction. Adds the
        additional features:
        - (pressing q) Handles quit option
        - (pressing i and additonal choice) Handles inventory option
        - Always returns an integer.

        Args:
            text (str):
            The text to display to the user.

            options (list[str]):
            The list of options to display to the user.

            Inventory (bool, optional):
            Whether inventory is enabled or disabled.
            Defaults to True.

        Returns:
            int: The user's chosen option, as corresponds to the place within
            the options list.
        """
        choices = options.copy()
        if not hasattr(self.game_state, "inventory"):
            Inventory = False
        query = 0
        if Inventory and hasattr(self.game_state, "inventory"):
            choices = choices + ["Inventory"]
        for i in range(len(choices)):
            choices[i] = self.ui_format_string(choices[i])
        text = self.ui_format_string(text)
        query = tui.option(self.win, text, choices)
        if query == "q":
            max_y, max_x = self.win.getmaxyx()
            padding = 0
            padx1 = max_x // 2 - 20
            padx2 = max_x // 2 - 20
            pady1 = max_y // 2 - 5
            pady2 = max_y // 2 - 5
            quitborder = tui.create_newwin(
                self.win, padding, padx1, padx2, pady1, pady2
            )
            padding = 1
            pady2 += 1
            quitwin = tui.create_newwin(self.win, padding, padx1, padx2, pady1, pady2)
            default_border = self.engineInfo.get("DefaultBorderStyle", 0)
            border_style = self.gameInfo.get("border_style", default_border)
            tui.draw_titlebar(quitborder, "", "", "", border_style)
            query = tui.option(
                quitwin,
                "Are you sure you want to quit?",
                ["Save and Quit", "Quit without Saving", "Return to Game"],
            )
            if query == 0:
                self.win.clear()
                self.fn_save_handler()
                sys.exit(0)
            if query == 1:
                sys.exit(0)
            else:
                query = self.ui_option(text, options, Inventory)
        elif query == "d":
            self.db_debug()
            query = self.ui_option(text, options, Inventory)
        elif Inventory and (query == choices.index("Inventory") or query == "i"):
            self.win.clear()
            self.ui_drawtitlebar(centreOverride="Inventory")
            print3(self.win, str(self.game_state.inventory))
            print3(self.win, "\nPress any key to exit inventory.")
            self.win.getch()
            self.ui_drawtitlebar()
            query = self.ui_option(text, options, Inventory)
        if not isinstance(query, int):
            query = self.ui_option(text, options, Inventory)
        return query

    def fn_battle_handler(self) -> None:
        """Handles battles in the SHM Engine.

        The attribute battle_hooks should be set up before calling this.
        The gamefile should also have the attributes 'enemies' and
        'battle_hooks'.
        """
        DEFAULT_LOSS_TEXT: str = "You have fallen in battle..."
        TIME_BATTLETEXT_DISPLAYED: float = 0.5

        if not self.battle_hooks:
            return

        if not hasattr(self.game, "enemies"):
            return

        if not hasattr(self.game, "battle_hooks"):
            return

        enemy: Enemy | None = self.fn_battle_get_enemy()

        if enemy is None:
            return

        if "BattleText" in self.room and isinstance(self.room["BattleText"], str):
            print3(self.win, self.room["BattleText"])
            time.sleep(TIME_BATTLETEXT_DISPLAYED)

        if hasattr(self.game, "battle_items") and isinstance(
            self.game.battle_items, dict
        ):
            battle_items: dict[str, BattleItem] | None = self.game.battle_items
        else:
            battle_items: dict[str, BattleItem] | None = None

        try:
            items: list[str] = self.game_state.inventory.items
        except:
            items: list[str] = []

        if not isinstance(items, list):
            self.err_log_error(error_type="Error", error_msg="Unable to get items.")
            return

        if "variable_damage" in self.gameInfo:
            variable_damage: bool = self.gameInfo["variable_damage"]
        else:
            variable_damage: bool = False

        battle: BattleHandler = BattleHandler(
            stdscr=self.win,
            hook_dict=self.battle_hooks,
            enemy=enemy,
            variable_damage=variable_damage,
            battle_items=battle_items,
            items=items,
        )
        if battle.battle_handler():
            self.ui_drawtitlebar()
            return
        elif "loss_text" in self.battle_hooks:
            loss_text: str = self.battle_hooks.get("loss_text")
        else:
            loss_text: str = DEFAULT_LOSS_TEXT
        self.ui_lose(loss_text)

    def fn_battle_get_enemy(self) -> Enemy | None:
        """Gets an enemy for an encounter, based on the current room.

        Returns:
            Enemy | None:
            None indicates that there is no enemy, or if an error
            was encountered and an enemy was unable to be obtained.
            Enemy is a dict (see typeddicts.py) that represents the enemy.
        """
        # If Enemies and EnemyChances do not exist, we cannot pick an enemy
        if "Enemies" not in self.room or "EnemyChances" not in self.room:
            self.err_log_error(
                error_type="Warning",
                error_msg="Unable to generate enemy: Enemies or EnemyChances"
                + "do not exist.",
            )
            return
        if not isinstance(self.room["Enemies"], list):
            self.err_log_error(
                error_type="Warning",
                error_msg="Unable to generate enemy: Enemies is not a list.",
            )
            return
        if not isinstance(self.room["EnemyChances"], list):
            self.err_log_error(
                error_type="Warning",
                error_msg="Unable to generate enemy: EnemyChances is not a list.",
            )
            return
        # If Enemies and EnemyChances are not the same length, then they are
        # meaningless.
        if not len(self.room["Enemies"]) == len(self.room["EnemyChances"]):
            self.err_log_error(
                error_type="Warning",
                error_msg="Unable to generate enemy: Enemies and EnemyChances"
                + "are not the same length.",
            )
            return

        total_chance: float = 0.0  # sum of all chances

        # number of digits after decimal point in longest float
        # used to determine the required precision
        longest_decimal: int = 0

        for i in self.room["EnemyChances"]:
            # If a chance is not a number, it is meaningless; quit
            if not isinstance(i, float | int):
                return
            length: int = len(str(i)) - 2
            if length > longest_decimal:
                longest_decimal = length
            total_chance += i

        multiplier: float = 1.0
        chances: list[float | int] = self.room["EnemyChances"].copy()

        # If the developer put total chances at above 1, we need to sort this out
        if total_chance > 1:
            multiplier: float = 1 / total_chance

        if multiplier != 1:
            for i in chances:
                i = i * multiplier
                length: int = len(str(i)) - 2
                if length > longest_decimal:
                    longest_decimal = length
        accuracy: int = int("1" + "0" * longest_decimal)
        rng: int | float = rand(0, accuracy + 1)
        rng /= accuracy
        chosen_enemy: int = -1

        # Get the randomly-chosen enemy
        for i in range(len(chances)):
            rng -= chances[i]
            if rng <= 0:
                chosen_enemy = i
                break

        # No enemy has been chosen; return None
        if chosen_enemy == -1:
            return

        enemy_id = self.room["Enemies"][chosen_enemy]
        # Enemy must be string or an integer
        if not isinstance(enemy_id, str) and not isinstance(enemy_id, int):
            return

        enemy: Enemy | None = self.game.enemies.get(enemy_id, None)

        return enemy

    def fn_itemHandler(self, attr: str) -> None:
        """Handles items within a room, including item requirements.

        Args:
            attr (str):
            A string that represents an attribute of the room;
            should be present in the room, e.g. 'Item'.
            The possible values as of SHM 1.2 are: 'Item', 'KeyItem'
        """
        if not (
            f"{attr}Requirements" in self.room
            and self.room[f"{attr}Requirements"]()
            or f"{attr}Requirements" not in self.room
        ):
            return

        if f"{attr}Text" in self.room:
            errorMsg = "An error has occurred. This message should not appear."
            print3(self.win, "\n" + self.room.get(f"{attr}Text", errorMsg))
        self.fn_get_item(self.room[attr])

    def fn_get_item(self, item: str) -> bool:
        """Function to obtain an item.

        Args:
            item (str): The item to obtain

        Returns:
            bool: A boolean return value representing if the operation
            succeeded, or if an error was encountered.
        """
        try:
            if (
                hasattr(self.game_state, "inventory")
                and hasattr(self.game, "keyItems")
                and item in self.game.keyItems
                and item not in self.game_state.inventory.keyItems
            ):
                self.game_state.inventory.getKeyItem(item, self.win)
            elif hasattr(self.game_state, "inventory"):
                self.game_state.inventory.getItem(item, self.win)
            self.win.getch()
            return True
        except AttributeError:
            self.err_log_error(
                error_type="Error",
                error_msg="Inventory does not have the proper methods to obtain items.",
            )
            return False

    def fn_main_option_handler(self, text: str) -> None:
        """The main handler of a room.

        Handles the moving between rooms and showing the options menu.

        Args:
            text (str): The text to be displayed to the user while options are
            being displayed below.
        """
        TIME_TO_SHOW_SHOP_EXIT_TEXT: float = 0.4 # Why 0.4? idk

        item_names: list[str] = self.room.get("ShopItems", [])
        item_costs: list[int] = self.room.get("ShopItemCosts", [])
        item_room: list[int] = self.room.get("ShopItemMove", [])

        # Detect if this room is a shop
        is_shop: bool = (
            "ShopItems" in self.room
            and isinstance(self.room["ShopItems"], list)
            and "ShopItemCosts" in self.room
            and isinstance(self.room["ShopItemCosts"], list)
            and "ShopEntrance" in self.room
            and isinstance(item_room, list)
            and len(item_names) == len(item_costs)
            and (len(item_names) == len(item_room) or not item_room)
        )

        # Get money hook
        if hasattr(self.game, "money_hook") and isinstance(
            getattr(self.game, "money_hook"), Box
        ):
            money_hook: Box[int] = getattr(self.game, "money_hook")
        else:
            money_hook: Box[int] = Box(0)
            item_names: list[str] = []

        # Check shop attributes are correct if present.
        for attr in ["ShopItems", "ShopItemCosts", "ShopItemMove"]:
            if attr not in self.room:
                continue
            if not isinstance(self.room[attr], list):
                self.room[attr] = [self.room[attr]]

        for i in range(len(item_costs)):
            try:
                int(item_costs[i])
            except TypeError:
                self.err_log_error(
                    error_type="Warning",
                    error_msg=f"Invalid type in item_costs in {self.roomID}.",
                )
                item_costs[i] = int(bool(item_costs[i]))

        for i in range(len(item_room)):
            try:
                int(item_room[i])
            except TypeError:
                self.err_log_error(
                    error_type="Warning",
                    error_msg=f"Invalid type in item_room in {self.roomID}.",
                )
                item_room[i] = int(bool(item_room[i]))

        # Get longest item name
        longest_name_length: int = 0
        for i in item_names:
            if len(i) > longest_name_length:
                longest_name_length: int = len(i)

        # Get longest price
        longest_price: int = 0
        for i in item_costs:
            cost_length: str = f"{i}"
            if len(cost_length) > longest_price:
                longest_price: int = len(cost_length)

        # Get list of items to display to the user
        shop_items: list[str] = []
        currency_name: str = str(self.gameInfo.get("currency_name", "Money"))
        for i in range(len(item_names)):
            # Check that lists are the same length, thus being a sensible value
            if len(item_names) != len(item_costs):
                break
            if len(item_names) != len(item_room) and item_room:
                break

            name_length_difference: int = longest_name_length - len(item_names[i])
            cost_length_difference: int = longest_price - len(f"{item_costs[i]}")

            string: str = f"Purchase {item_names[i]}"

            # If it were not for curses, there would be a strikethrough
            # Check that you have enough money
            # if item_costs[i] > money_hook:
            #     string += "\033[9mNOT ENOUGH MONEY\033[0m"

            if item_costs[i] == 0:
                string: str = string + " " * name_length_difference
                string: str = string + " " * len(" - ")
                string: str = string + " " * longest_price
                string: str = string + " " * 1
                string: str = string + " " * len(currency_name)
            else:
                string: str = string + " " * name_length_difference
                string: str = string + f" - {item_costs[i]}"
                string: str = string + " " * cost_length_difference
                string: str = string + " "
                string: str = string + f"{currency_name}"
            shop_items.append(string)

        options_index: list[int | tuple[str, int]] = []
        options: list[str] = []
        for i in self.room.get("Move", []):
            OptionRequirements = (
                "Option" + str(self.room["Move"].index(i)) + "Requirements"
            )
            if OptionRequirements not in self.room or self.room[OptionRequirements]():
                options_index.append(i)
                optionText = self.room["Options"][self.room["Move"].index(i)]
                if self.globaldebug:
                    options.append(optionText + " - RoomID: " + str(i))
                else:
                    options.append(optionText)

        # Add ShopExit option and options_index
        if is_shop and not (
            "Back" in options
            or "Exit" in options
            or "Exit Shop" in options
            or "Go Back" in options
            # or "Leave" in options
            or "Leave Shop" in options
            or "Quit" in options
            # Check that complevel 2 is supported, or errors occur
            and self.game.gameInfo["complevel"] >= 2
        ):
            options.append("Leave Shop")
            options_index.append(-2)

        choices: list[str] = shop_items + options

        if (
            "Inventory" in self.room
            and self.game_state.inventory
            and not self.room["Inventory"]
        ):
            query: int = self.ui_option(text, choices, Inventory=False)
        else:
            query: int = self.ui_option(text, choices)

        # This variable is used to test if the purchase operation was
        # successful, just in case of any errors.
        purchased_item: bool = False

        # Query is a move to location option
        if query > len(shop_items) - 1:
            self.fn_roomIDHandler(options_index[query - len(shop_items)])

        elif item_costs[query] <= money_hook:
            chosen_item: str = str(item_names[query])
            self.win.clear()
            purchased_item: bool = self.fn_get_item(chosen_item)
        if purchased_item:
            money_hook -= item_costs[query]

        # Check that it is a shop
        if not is_shop:
            return

        # Implements ShopItemMove
        if query <= len(shop_items) - 1 and item_room and item_room[query] != -1:
            self.fn_roomIDHandler(int(item_room[query]))

        # If chosen option is the last option, then the chosen option must be 
        # that of Leave Shop; then check if there is an exit phrase, and mark
        # the shop as left, returning the user outside the shop.
        if query != len(choices) - 1:
            return

        self.roomID = self.shop_exit
        self.shop_exit = -1

        if "ShopExit" not in self.room:
            return
        
        shop_exit_text: str = ""
        if isinstance(self.room["ShopExit"], str):
            shop_exit_text: str = self.room["ShopExit"]
        elif isinstance(self.room["ShopExit"], list):
            random_index: int = rand(len(self.room["ShopExit"]))
            shop_exit_text: str = str(self.room["ShopExit"][random_index])
        self.win.clear()
        print3(self.win, "\n")
        tui.centre_text(self.win, shop_exit_text)
        print3(self.win, shop_exit_text)
        time.sleep(TIME_TO_SHOW_SHOP_EXIT_TEXT)
        return

    def fn_roomIDHandler(self, room_id: int | tuple[str, int]) -> None:
        """Handles room IDs and moving between rooms.

        * Handles raw ID numbers, e.g. 2; moves to the room with that ID.
        * Handles negative ID numbers, e.g. -2; moves to previous room.
        * Handles history tuples, e.g. (history, -2); same as above.

        Args:
            tmpID (int | tuple[str, int]): The ID number to be parsed.
        """
        negIDsupport = not (self.game.gameInfo["complevel"] == 1)
        if isinstance(room_id, tuple) and room_id[0] == "history":
            self.roomID = self.history[room_id[1]]
        elif isinstance(room_id, int) and (room_id < 0 and negIDsupport):
            self.roomID = self.history[room_id]
        elif isinstance(room_id, int) and (room_id >= 0 or not negIDsupport):
            self.roomID = room_id

    def fn_save_handler(self) -> None:
        save_handler.write_save(
            self.game_state,
            self.gameInfo,
            self.roomID,
            self.history,
            self.saveFileName,
            self.engineInfo["SaveVersion"],
            self.gameInfo.get("game_id", None),
            self.current_saveid,
            self.shop_exit

        )

    def fn_gameLoop(self) -> None:
        """The main loop of the game and calls all other functions.

        Handles all attributes and parsing a room.
        """
        # Set up and get current room for access
        rooms = self.game.get_rooms(self.win)
        self.win.clear()
        self.ui_drawtitlebar()
        complevel = self.game.gameInfo["complevel"]
        subDict = self.engineInfo
        subDict["complevel"] = str(complevel)
        subDict["complevels"] = str(self.COMPATIBLE_COMPLEVELS)[1:-1]
        if complevel not in self.COMPATIBLE_COMPLEVELS:
            string = (
                "This game (complevel {complevel}) is not compatible with this"
                " version of the {Name} {MajorVersion}.\n{Name} {MajorVersion}"
                " is only compatible with the following complevels: {complevels}"
            )
            string: str = string.format_map(subDict)
            self.err_log_error(error_type="Critical Error", error_msg=string)
        if self.roomID in rooms:
            self.room = rooms[self.roomID]
        elif self.starting_room in rooms:
            self.room = rooms[self.starting_room]
            self.err_roomIDerror()
        else:
            self.room = rooms[1]
            self.err_roomIDerror()
        self.ui_drawtitlebar()
        self.history.append(self.roomID)
        if len(self.history) > HISTORY_MAX_LEN:
            self.history.pop(0)

        # Handle shop
        is_shop: bool = (
            "ShopItems" in self.room
            and isinstance(self.room["ShopItems"], list)
            and "ShopItemCosts" in self.room
            and isinstance(self.room["ShopItemCosts"], list)
            and "ShopEntrance" in self.room
        )
        if is_shop and self.shop_exit == -1:
            self.shop_exit = self.history[-2]

        # Handle room attributes
        text: str = self.ui_text_handler()
        if self.globaldebug:
            text += "\nRoomID: " + str(self.roomID)
            text += "\nHistory: " + str(self.history)
            text += "\nShop Exit: " + str(self.shop_exit)
        if "Script" in self.room:
            self.room["Script"]()
        if "Item" in self.room:
            self.fn_itemHandler("Item")
        if "KeyItem" in self.room:
            self.fn_itemHandler("KeyItem")
        if "Enemies" in self.room and "EnemyChances" in self.room:
            self.fn_battle_handler()
        if "Automove" in self.room:
            self.fn_roomIDHandler(self.room["Automove"])
            automove_delay = not (self.room.get("InstantAutomove", False))
            automove_delay = AUTOMOVE_DELAY * automove_delay
            time.sleep(int(automove_delay))
        elif "Move" in self.room:
            self.fn_main_option_handler(text)
        if "Ending" in self.room:
            automove_delay = not (self.room.get("InstantAutomove", False))
            automove_delay = ENDING_DELAY * automove_delay
            time.sleep(automove_delay)
            self.ui_ending(self.room["Ending"])
        if "Lose" in self.room:
            self.ui_lose(self.room["Lose"])

    def fn_looper(self) -> None:
        """Simple loop function that loops fn_gameLoop()"""
        while 1:
            self.fn_gameLoop()


def run(
    win: curses.window,
    starting_room: int | None = None,
    saveFileName: str = "game",
    saveFile: dict[None, None] | Save | None = None,
    gameFile_name: str = "game",
    gameFile_path: str = "./",
) -> None:
    """The wrapper to start the SHM Engine.

    Args:
        win (curses.window):
        A curses window instance.

        starting_room (int | None, optional):
        When specified, the engine starts within that room ID.
        If None, uses the starting_room within the gamefile.
        Defaults to None.

        saveFileName (str, optional):
        The name of the save file to write to when the game is saved.
        Defaults to "game".

        saveFile (dict[None, None] | Save | None, optional):
        The save file to be loaded, as a dict in the Save format.
        Defaults to None.

        gameFile_name (str, optional):
        The name of the module name which corresponds to the gamefile
        to be loaded.
        If the file extension is not specified, defaults to '.py'.
        Defaults to "game".

        gameFile_path (str, optional):
        The file path of the gamefile to be loaded.
        Accepts both relative and absolute paths.
        May not include the file itself or only the directory.
        Defaults to "./".
    """

    curses.curs_set(0)
    win.scrollok(True)
    tui.colorsetup(win)
    curses.cbreak()
    curses.noecho()
    if saveFile is None:
        saveFile: dict[None, None] = {}
    if saveFile:
        validSave: bool = save_handler.save_validifier(saveFile)
    if saveFile and validSave:
        save_version: int = int(saveFile.get("save_version", 0))
        engine_info: EngineInfo = toml_reader.read_toml("engine_info.toml")
        engine_save_version = engine_info.get("SaveVersion", 0)
        supported_version: bool = save_version <= engine_save_version
    if saveFile and not validSave:
        timestamp = datetime.now().isoformat()
        with open("error.log", "a") as log:
            log.write(
                f"{timestamp} Warning: Could not parse save file as a valid save file."
                + "\nContinuing without save file...\n"
            )
    if saveFile and not supported_version:
        timestamp: str = datetime.now().isoformat()
        with open(file="error.log", mode="a") as log:
            log.write(
                f"{timestamp} Warning: Could not parse save file. The save"
                + f" file has a version of {save_version}, but this version of"
                + f"the SHM Engine only supports up to {supported_version}\n"
                + "Continuing without save file...\n"
            )
    if saveFile and validSave and supported_version:
        main: MainHandler = MainHandler(
            win,
            saveFile["RoomID"],
            saveFile,
            gameFile_name,
            gameFile_path,
            saveFileName,
        )
    else:
        main: MainHandler = MainHandler(
            win,
            starting_room,
            gameFile_name=gameFile_name,
            gameFile_path=gameFile_path,
            saveFileName=saveFileName,
        )
    main.fn_looper()


gameLoop: Callable[..., None] = run


if __name__ == "__main__":

    # if len(sys.argv) > 1:
    # sys.argv[1]
    print(
        toml_reader.get_engine_info(
            "{Name} {MajorVersion}{PatchConnector}{Patch}\n"
            + "{ReleaseDate}\n{Link}\nThis Release: '{Dist}'"
        )
    )
    sys.exit(0)

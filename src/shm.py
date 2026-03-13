#!/usr/bin/env python3
from collections.abc import Callable
import curses
from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location
from itertools import chain
import os.path
import platform
import re
import sys
import time
from types import ModuleType
from typing import Any, TypedDict, NotRequired

import save_handler
import toml_reader
import tui
from tui import print3


HISTORY_MAX_LEN: int = 10
AUTOMOVE_DELAY: float = 1.0
ENDING_DELAY: float = 0.5


class Room(TypedDict, total=False):
    # NOTE: Type checking would require the 'extra_items' attribute from Python 3.15;
    # Python 3.15 has not yet had a stable release yet as I am writing this comment;
    # thus, this TypedDict cannot be used for type checking;
    # it is thus solely used for documentation
    # NOTE #2: Do not code at 11 PM or you will start hallucinating like AI slop
    """
    This is the canonical format for rooms in the SHM Engine 1.2.
    This has a main purpose of showing the supported keys, not type checking.
    This TypedDict supports additional fields, although compromising type checking,
    as fields such as Option[]Requirements are variable, where # represents an int.
    Rooms within a game are recommended to use this order for their attributes.
    """
    Text: str
    Requirements: Callable[[], bool]
    AlternateText: str
    TextSpeed: float
    Desc: str
    titlebarCentre: str
    titlebarLeft: str
    titlebarRight: str
    Script: Callable[[], None]
    Item: str
    ItemRequirements: Callable[[], bool]
    ItemText: str
    KeyItem: str
    KeyItemRequirements: Callable[[], bool]
    KeyItemText: str
    Options: list[str]
    Option0Requirements: Callable[[], bool]
    Inventory: bool
    Move: list[int]
    Automove: int
    InstantAutomove: bool
    Lose: str
    Ending: str


class Save(TypedDict):
    """This is the canonical format for save files with save version 1."""
    Game: str
    Saved: str
    save_version: int
    RoomID: int
    History: list[int]
    game_state: dict[str, Any]
    inventory: dict[str, list[str]]
    game_id: NotRequired[int | str]
    save_id: int | str


class EngineInfo(TypedDict):
    Name: str
    MajorVersion: str
    Patch: str
    Indev: bool
    PythonVer: float
    ReleaseDate: str
    Dist: str
    Link: str
    SaveVersion: int
    DefaultBorderStyle: int


class formatDict(dict):
    """A subclass of a dictionary which will not replace any key not present
    when format_map is used, preventing exceptions."""

    def __missing__(self, key: str) -> str:
        string = "{" + key + "}"
        return string


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
        """
        Set up an instance of the SHM Engine with a given gamefile.

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
            The name of the module name which corresponds to the gamefile to be loaded.
            Defaults to "game".

            gameFile_path (str, optional):
            The file path of the gamefile to be loaded.
            Accepts both relative and absolute paths.
            If the file extension is not specified, defaults to '.py'.
            Defaults to "./game.py".

            saveFileName (str, optional):
            The name of the save file to write to when the game is saved.
            Defaults to "game".
        """
        self.COMPATIBLE_COMPLEVELS: list[int] = [1, 2]
        self.current_saveid: int | str | None = None
        self.engineInfo: formatDict = formatDict(
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
            self.current_saveid = saveFile.get("save_id", None)

    def setup_gameFile(self, module_name: str, file_path: str) -> ModuleType:
        """
        Imports a module and allows it to be publicly available.
        This function is used to import the gamefile in context of the SHM Engine.

        Args:
            module_name (str): The name of the module to import.
            file_path (str): The path of the module to import.

        Raises:
            ImportError: This error is raised if the specified module is nonexistent.

        Returns:
            ModuleType: The module which has just been imported.
        """
        file_path = os.path.abspath(file_path)
        if file_path[-3:] != ".py":
            file_path = os.path.join(file_path, module_name)
            file_path = file_path + ".py"
        spec = spec_from_file_location(module_name, file_path)
        try:
            module = module_from_spec(spec)  # pyright: ignore
        except:
            raise ImportError("Failed to import game file")
        sys.modules[module_name] = module
        spec.loader.exec_module(module)  # pyright: ignore
        return module

    def setup_loadSave(self, saveFile: Save | None) -> None:
        """
        Sets up the save file and sets up the game state by copying values
        from the save file.

        Args:
            saveFile (dict): A dictionary in the SHM Engine save file format.
        """
        if saveFile is None:
            return
        if (
            saveFile.get("game_id") != self.gameInfo.get("game_id")
            or saveFile["Game"] != self.gameInfo["title"]
        ):
            # put error handling here
            self.roomID = self.starting_room
            return
        self.history.extend(saveFile["History"])
        for item in saveFile["game_state"]:
            setattr(self.game_state, item, saveFile["game_state"][item])
        if hasattr(self.game_state, "inventory") and "inventory" in saveFile:
            for item in saveFile["inventory"]["items"]:
                self.game_state.inventory.items.append(item)
            for item in saveFile["inventory"]["keyItems"]:
                self.game_state.inventory.keyItems.append(item)

    def setup_stdscr(self) -> None:
        """Sets up the main activity window, inside the border."""
        padding = 1
        padx1 = 0
        padx2 = 0
        pady1 = 0
        pady2 = 1
        self.win = tui.create_newwin(self.stdscr, padding, padx1, padx2, pady1, pady2)

    def db_debug(self) -> None:
        """The debug menu"""
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
        """Debug menu - test all room IDs in the game file and check for any
        invalid room IDs, and report any errors.
        Also notes when (history, -x)-style references when complevel == 2"""
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
        """
        Debug menu - check all attribute types within a room, and log whenever
        an incorrect type is found.
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
                real_type = type(room[attribute])
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
        errorMsg: str,
        colorcode: int = 0,
        delay: float = 0.0,
        pauseAtNewline: float = 0.0,
    ) -> None:
        """
        Log an error - that's basically it.

        Args:
            errorMsg (str): The message to display to the user

            colorcode (int, optional, deprecated):
            Changes the colour of the text; see tui.print3.
            Defaults to 0.

            delay (float, optional):
            The time between characters being printed; see tui.print3.
            Defaults to 0.0.

            pauseAtNewline (float, optional):
            The time that is waited when a new line is created; see tui.print3.
            Defaults to 0.0.
        """
        timestamp = datetime.now().isoformat()
        with open("error.log", "a") as log:
            log.write(f"{timestamp} {errorMsg}\n")
        self.win.refresh()
        self.ui_drawtitlebar(centreOverride="Error", leftOverride="", rightOverride="")
        print3(self.win, errorMsg, colorcode, delay, pauseAtNewline)

    def err_roomIDerror(self) -> None:
        """Handle an error when an invalid room is attempted to be loaded"""
        self.err_log_error(f"Non-critical Error: Invalid RoomID: {self.roomID}", 33, 0)
        query = self.ui_option(
            "Non-critical Error: Invalid RoomID",
            ["Open Debug Menu", "Quit Game"],
            False,
        )
        if query == 0:
            self.db_debug()
            sys.exit(2)
        if query == 1:
            sys.exit(2)
        print3(self.win, "\nPress any key to exit...", 0, 0)

    def ui_drawtitlebar(
        self,
        centreOverride: str | None = None,
        leftOverride: str | None = None,
        rightOverride: str | None = None,
    ) -> None:
        """
        Handle the titlebar and set up the strings to be displayed.
        Handles the 'titlebarCentre', 'titlebarLeft' and 'titlebarRight'
        attributes within a room, as well as the default titlebar strings set
        in game info.
        Also passes the border style as defined within game info, to tui.draw_titlebar.

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
        leftString = " F1 - Help "
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
        """
        Handles endings in a game, including autosaving.

        Args:
            end (str):
            The ending which the user has received.
            The ending text is set within the gamefile, under the endingText attribute.
        """
        titlebar_centre = "{title}"
        titlebar_left = ""
        titlebar_right = ""
        self.ui_drawtitlebar(titlebar_centre, titlebar_left, titlebar_right)
        self.roomID = self.starting_room
        save_handler.write_save(
            self.game_state,
            self.gameInfo,
            self.roomID,
            self.history,
            self.saveFileName,
            self.engineInfo["SaveVersion"],
            self.gameInfo.get("game_id", None),
            self.current_saveid,
        )
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
        """
        Formats the string with the various available keys;
        used to format the titlebar and the text of rooms.
        Keys are in the format '{key}' embedded within a string.

        Supported keys:
         - 'abbr' - the abbreviation set by the game, if present.
         - 'arch' - the architecure of the machine, uses platform.machine().
         - 'date' - returns the current date in Y-M-D format.
         - 'engine_info' - returns the current version of the SHM Engine.
         - 'game_state' - the entire current game_state;
             - call individual parts of game_state
         - 'iso_date' - returns the current date in iso-format.
         - 'python_implementation' - returns the current Python implementation
         - 'python_version' - returns the current Python version
         - 'self' - returns the entire self object;
             - [see 'game_state' above] - recommended to only call children.
         - 'system' - returns the current OS, using platform.system().
         - 'time' - returns the current time in H:M.
         - 'title' - returns the game title.
         - 'utime' - returns the current time in Unix timestamp.


        Args:
            string (str): The string to be formatted by the function.

        Returns:
            str: The output string that has been formatted.
        """
        subDict = {
            "abbr": self.gameInfo.get("abbr", "{abbr}"),
            "arch": platform.machine(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "engine_info": self.SHMversion,
            "game_state": self.game_state,
            "iso_date": datetime.now().isoformat(),
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "self": self,
            "system": platform.system(),
            "time": datetime.now().strftime("%H:%M"),
            "title": self.gameInfo.get("title", "{title}"),
            "utime": datetime.now().timestamp(),
        }
        subDict = formatDict(subDict)
        if self.room and "Desc" in self.room:
            subDict["desc"] = self.room["Desc"]
        string = string.format_map(subDict)
        return string

    def ui_lose(self, lose: str) -> None:
        """
        Handles losing the game.

        Args:
            lose (str):
            The loss which the user has received.
            The loss text is set within the gamefile, under the loseText attribute.
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
            sys.exit()
        else:
            self.roomID = self.starting_room

    def ui_text_handler(self) -> str:
        """
        Handle the text of a room, between Text, AlternateText, etc.
        Prints the text and returns the text.

        Returns:
            str: The appropriate text of the room to be used.
        """
        text = ""
        if "Requirements" in self.room and not self.room["Requirements"]():
            text = self.room["AlternateText"]
        else:
            text = self.room["Text"]
        tui.newline(self.win)
        if "\n" not in text:
            tui.centre_text(self.win, text)
        self.win.scrollok(True)
        text = self.ui_format_string(text)
        print3(self.win, text, delay=self.room.get("TextSpeed", self.text_speed))
        return text

    def ui_option(self, text: str, choices: list[str], Inventory: bool = True) -> int:
        """
        Handle options for the SHM Engine, as a wrapper for tui.option();
        - Handles quit option
        - Handles inventory optio

        Args:
            text (str):
            The text to display to the user.

            choices (list[str]):
            The list of options to display to the user.

            Inventory (bool, optional):
            Whether inventory is enabled or disabled.
            Defaults to True.

        Returns:
            int: The user's chosen option, as corresponds to place in the array.
        """
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
                save_handler.write_save(
                    self.game_state,
                    self.gameInfo,
                    self.roomID,
                    self.history,
                    self.saveFileName,
                    self.engineInfo["SaveVersion"],
                    self.gameInfo.get("game_id", None),
                    self.current_saveid,
                )
                sys.exit()
            if query == 1:
                sys.exit()
            else:
                query = self.ui_option(text, choices, Inventory)
        elif query == "d":
            self.db_debug()
            query = self.ui_option(text, choices, Inventory)
        elif Inventory and (query == choices.index("Inventory") or query == "i"):
            self.win.clear()
            self.ui_drawtitlebar(centreOverride="Inventory")
            print3(self.win, str(self.game_state.inventory))
            print3(self.win, "\nPress any key to exit inventory.")
            self.win.getch()
            self.ui_drawtitlebar()
            query = self.ui_option(text, choices, Inventory)
        if not isinstance(query, int):
            query = self.ui_option(text, choices, Inventory)
        return query

    def fn_itemHandler(self, attr: str) -> None:
        """
        Handles items within a room, including item requirements.

        Args:
            attr (str):
            A string that represents an attribute of the room;
            should be present in the room, e.g. 'Item'.
            The official possible values as of SHM 1.2 are: 'Item', 'KeyItem'
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
        if (
            hasattr(self.game_state, "inventory")
            and self.game.keyItems
            and self.room[attr] in self.game.keyItems
            and self.room[attr] not in self.game_state.inventory.keyItems
        ):
            self.game_state.inventory.getKeyItem(self.room[attr], self.win)
        elif hasattr(self.game_state, "inventory"):
            self.game_state.inventory.getItem(self.room[attr], self.win)
        self.win.getch()

    def fn_mainRoomHandler(self, text: str) -> None:
        """
        The main handler of a room;
        handles the moving between rooms and showing the options menu.

        Args:
            text (str): The text to be displayed to the user at the option menu.
        """
        OptionsIndex = []
        Options = []
        for i in self.room["Move"]:
            OptionRequirements = (
                "Option" + str(self.room["Move"].index(i)) + "Requirements"
            )
            if OptionRequirements not in self.room or self.room[OptionRequirements]():
                OptionsIndex.append(i)
                optionText = self.room["Options"][self.room["Move"].index(i)]
                if self.globaldebug:
                    Options.append(optionText + " - RoomID: " + str(i))
                else:
                    Options.append(optionText)
        if (
            "Inventory" in self.room
            and self.game_state.inventory
            and not self.room["Inventory"]
        ):
            query = self.ui_option(text, Options, Inventory=False)
        else:
            query = self.ui_option(text, Options)
        self.fn_roomIDHandler(OptionsIndex[query])

    def fn_roomIDHandler(self, tmpID: int | tuple[str, int]) -> None:
        """
        Handles room IDs and moving between rooms.
         - Handles raw ID numbers, e.g. 2;
         - Handles negative ID numbers, e.g. -2 (which are references to history);
         - Handles history tuples, e.g. (history, -2)

        Args:
            tmpID (int | tuple[str, int]): The ID number to be parsed.
        """
        negIDsupport = not (self.game.gameInfo["complevel"] == 1)
        if isinstance(tmpID, tuple) and tmpID[0] == "history":
            self.roomID = self.history[tmpID[1]]
        elif isinstance(tmpID, int) and (tmpID < 0 and negIDsupport):
            self.roomID = self.history[tmpID]
        elif isinstance(tmpID, int) and (tmpID >= 0 or not negIDsupport):
            self.roomID = tmpID

    def fn_gameLoop(self) -> None:
        """
        The main part of the engine;
        the main loop of the game and calls all other functions.
        Handles all attributes and parsing a room.
        """
        rooms = self.game.get_rooms(self.win)
        self.win.clear()
        self.ui_drawtitlebar()
        complevel = self.game.gameInfo["complevel"]
        subDict = self.engineInfo
        subDict["complevel"] = str(complevel)
        subDict["complevels"] = str(self.COMPATIBLE_COMPLEVELS)[1:-1]
        if complevel not in self.COMPATIBLE_COMPLEVELS:
            string = (
                "ERROR: This game (complevel {complevel}) is not compatible with this"
                " version of the {Name} {MajorVersion}.\n{Name} {MajorVersion} is only"
                " compatible with the following complevels: {complevels}"
            )
            string = string.format_map(subDict)
            self.err_log_error(errorMsg=string, colorcode=31, delay=0)
            print3(self.win, "\nPress any key to exit...", 0, 0)
            self.win.getch()
            sys.exit(1)
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
        text = self.ui_text_handler()
        if self.globaldebug:
            text += "\nRoomID: " + str(self.roomID) + "\nHistory: " + str(self.history)
        if "Script" in self.room:
            self.room["Script"]()
        if "Item" in self.room:
            self.fn_itemHandler("Item")
        if "KeyItem" in self.room:
            self.fn_itemHandler("KeyItem")
        if "Automove" in self.room:
            self.fn_roomIDHandler(self.room["Automove"])
            automove_delay = not (self.room.get("InstantAutomove", False))
            automove_delay = AUTOMOVE_DELAY * automove_delay
            time.sleep(int(automove_delay))
        elif "Move" in self.room:
            self.fn_mainRoomHandler(text)
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
    """
    The wrapper to start the SHM Engine.

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

        saveFile (dict, optional):
        The save file.
        Defaults to {}.

        gameFile_name (str, optional):
        The name of the module name which corresponds to the gamefile to be loaded.
        Defaults to "game".

        gameFile_path (str, optional):
        The file path of the gamefile to be loaded.
        Accepts both relative and absolute paths.
        May not include the file itself or only the directory.
        If the file extension is not specified, defaults to '.py'.
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
        supported_version: bool = (save_version <= engine_save_version)
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

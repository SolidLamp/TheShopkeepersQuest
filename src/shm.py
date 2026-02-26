#!/usr/bin/env python3
from collections.abc import Callable
import curses
from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location
import os.path 
import platform
import sys
import time
from types import ModuleType
from typing import Required, TypedDict

import save_handler
import toml_reader
import tui
from tui import print3


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
    Options: list[str]
    Option0Requirements: Callable[[], bool]
    Move: list[int]
    Automove: int
    InstantAutomove: bool
    Lose: str
    Ending: str


class formatDict(dict):
    """A subclass of a dictionary which will not replace any key not present 
    when format_map is used, preventing exceptions"""
    def __missing__(self, key: str) -> str:
        string = "{" + key + "}"
        return string


class mainHandler:
    """The main heart of the SHM Engine."""
    def __init__(
        self,
        win: curses.window,
        starting_room: int | None = None,
        saveFile: dict = {},
        gameFile_name: str = "game",
        gameFile_path: str = "./game.py",
        saveFileName: str = "game",
    ) -> None:
        self.COMPATIBLE_COMPLEVELS: list = [1, 2]
        self.current_saveid: str | None = None
        self.engineInfo = formatDict(toml_reader.read_toml("engine_info.toml"))
        self.game = self.setup_gameFile(gameFile_name, gameFile_path)
        self.gameFile_name: str = gameFile_name
        self.gameInfo: dict = self.game.gameInfo
        self.game_state = self.game.game_state
        self.globaldebug: bool = False
        self.history = self.game.history
        self.room: dict = {}
        self.saveFileName: str = saveFileName
        self.SHMversion: str = toml_reader.get_engine_info()
        self.starting_room: int = self.gameInfo.get("starting_room", 1)
        self.stdscr: curses.window = win
        self.text_speed = self.gameInfo.get("default_textspeed", 0.01)
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
        """This function imports the game script for access within the SHM Engine."""
        file_path = os.path.abspath(file_path)
        if file_path[-3:] != ".py":
            file_path = os.path.join(file_path, module_name)
            file_path = file_path + ".py"
        spec = spec_from_file_location(module_name, file_path)
        try:
            module = module_from_spec(spec)
        except:
            raise ImportError("Failed to import game file")
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def setup_loadSave(self, saveFile: dict) -> None:
        """Sets up the save file and sets up the game state by copying values
        from the save file."""
        if (
            saveFile.get("game_id") != self.gameInfo["game_id"]
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
        debug_options = ["Test room IDs", "Enable debug mode"]
        query = tui.option(self.win, "SHM Engine Debug Menu", debug_options)
        match query:
            case 0:
                self.db_test_rooms()
            case 1:
                self.globaldebug = not (self.globaldebug)

    def db_log_error(
        self,
        errorMsg: str,
        colorcode: int = 0,
        delay: float = 0.0,
        pauseAtNewline: float = 0.0,
    ) -> None:
        """Log an error - that's basically it."""
        timestamp = datetime.now().isoformat()
        with open("error.log", "a") as log:
            log.write(f"{timestamp} {errorMsg}\n")
        self.win.refresh()
        self.ui_drawtitlebar(centreOverride="Error", leftOverride="", rightOverride="")
        print3(self.win, errorMsg, colorcode, delay, pauseAtNewline)

    def db_roomIDerror(self, rooms: dict) -> None:
        """Handle an error when an invalid room is attempted to be loaded"""
        self.db_log_error(f"Non-critical Error: Invalid RoomID: {self.roomID}", 33, 0)
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

    def db_test_rooms(self) -> None:
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
            negIDv1 = isinstance(idno, tuple) and idno[0] == "history" and idno[1] < 0
            negIDv2_support = not (self.game.gameInfo["complevel"] == 1)
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
        Also handles 'border_vertical', 'border_horizontal', 'border_corner_topleft',
        'border_corner_topright', 'border_corner_btmleft', 'border_corner_btmright'
        attributes of game info, and builds the specific border design based on them.
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
        tui.draw_titlebar(
            self.stdscr,
            title=title_string,
            leftString=leftString,
            rightString=rightString,
            border_vertical=self.gameInfo.get("border_vertical","║"),
            border_horizontal=self.gameInfo.get("border_horizontal","═"),
            border_corner_topleft=self.gameInfo.get("border_corner_topleft","╔"),
            border_corner_topright=self.gameInfo.get("border_corner_topright", "╗"),
            border_corner_btmleft=self.gameInfo.get("border_corner_btmleft","╚"),
            border_corner_btmright=self.gameInfo.get("border_corner_btmright","╝"),
        )

    def ui_ending(self, end: str) -> None:
        """Handles endings of a game, including saving."""
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
        """Formats the string with the various available keys;
        used to format the titlebar and the text of rooms.
        Keys are in the format '{key}' embedded within a string.

        Supported keys:
         - 'abbr' - the abbreviation set by the game, if present.
         - 'arch' - the architecure of the machine, uses platform.machine().
         - 'date' - returns the current date in Y-M-D format.
         - 'engine_info' - returns the current version of the SHM Engine.
         - 'game_state' - the entire current game_state;
             - call individual parts of game_state e.g. game_state.get().
         - 'iso_date' - returns the current date in iso-format.
         - 'python_implementation' - returns the current Python implementation
         - 'python_version' - returns the current Python version
         - 'self' - returns the entire self object;
             - [see 'game_state' above] - recommended to only call children.
         - 'system' - returns the current OS, using platform.system().
         - 'time' - returns the current time in H:M.
         - 'title' - returns the game title.
         - 'utime' - returns the current time in Unix timestamp.
        
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
        """Handles losing the game"""
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
        """Handle the text of a room, between Text, AlternateText, etc.
        Prints the text and returns the text."""
        text = ""
        if "Requirements" in self.room and not self.room["Requirements"]():
            text = self.room["AlternateText"]
        else:
            text = self.room["Text"]
        tui.newline(self.win)
        max_y, max_x = self.win.getmaxyx()
        y, x = self.win.getyx()
        new_x = max((max_x - len(text) - 1) // 2, 0)
        self.win.move(y, new_x)
        self.win.scrollok(True)
        text = self.ui_format_string(text)
        print3(self.win, text, delay=self.room.get("TextSpeed", self.text_speed))
        return text

    def ui_option(self, text: str, options: list, Inventory: bool = True) -> int:
        """Handle options for the SHM Engine, as a wrapper for tui.option();
         - Handles quit option
         - Handles inventory option"""
        if not hasattr(self.game_state, "inventory"):
            Inventory = False
        query = 0
        choices = options
        if Inventory and hasattr(self.game_state, "inventory"):
            choices = options + ["Inventory"]
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
            tui.draw_titlebar(quitborder, "")
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

    def fn_itemHandler(self, attr: str) -> None:
        """Handles items within a room, including item requirements
        - attr is a string that represents an attribute of the room;
        - attr should be present in the room, e.g. 'Item'."""
        if (
            f"{attr}Requirements" in self.room
            and self.room[f"{attr}Requirements"]()
            or f"{attr}Requirements" not in self.room
        ):
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
        """The main handler of a room;
        handles the moving between rooms and showing the options menu.
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

    def fn_roomIDHandler(self, tmpID: int | tuple) -> None:
        """
        Handles room IDs and moving between rooms.
         - Handles raw ID numbers, e.g. 2;
         - Handles negative ID numbers, e.g. -2 (which are references to history);
         - Handles history tuples, e.g. (history, -2)
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
            self.db_log_error(errorMsg=string, colorcode=31, delay=0)
            print3(self.win, "\nPress any key to exit...", 0, 0)
            self.win.getch()
            sys.exit(1)
        if self.roomID in rooms:
            self.room = rooms[self.roomID]
        elif self.starting_room in rooms:
            self.room = rooms[self.starting_room]
            self.db_roomIDerror(rooms)
        else:
            self.room = rooms[1]
            self.db_roomIDerror(rooms)
        self.ui_drawtitlebar()
        self.history.append(self.roomID)
        if len(self.history) > 10:
            self.history.pop(0)
        text = self.ui_text_handler()
        if self.globaldebug:
            text += "\nRoomID: " + str(self.roomID) + "\nHistory: " + str(self.history)
        if "Script" in self.room:
            self.room["Script"]()
        if "Ending" in self.room:
            self.ui_ending(self.room["Ending"])
            self.roomID = self.starting_room
        if "Item" in self.room:
            self.fn_itemHandler("Item")
        if "KeyItem" in self.room:
            self.fn_itemHandler("KeyItem")
        if "Automove" in self.room:
            self.fn_roomIDHandler(self.room["Automove"])
            automove_delay = not (self.room.get("InstantAutomove", False))
            time.sleep(int(automove_delay))
        elif "Move" in self.room:
            self.fn_mainRoomHandler(text)
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
    saveFile: dict = {},
    gameFile_name: str = "game",
    gameFile_path: str = "./",
) -> None:
    """
    The wrapper to start the SHM Engine.
    """
    curses.curs_set(0)
    win.scrollok(True)
    tui.colorsetup(win)
    curses.cbreak()
    curses.noecho()
    if saveFile:
        validSave = save_handler.save_validifier(saveFile)
    if saveFile and validSave:
        save_version = saveFile.get("save_version", 0)
        engine_info = toml_reader.read_toml("engine_info.toml")
        engine_save_version = engine_info.get("SaveVersion", 0)
        supported_version = save_version <= engine_save_version
    if saveFile and not validSave:
        timestamp = datetime.now().isoformat()
        with open("error.log", "a") as log:
            log.write(
                f"{timestamp} Warning: Could not parse save file as a valid save file."
                "\nContinuing without save file...\n"
            )
    if saveFile and not supported_version:
        timestamp = datetime.now().isoformat()
        with open("error.log", "a") as log:
            log.write(
                f"{timestamp} Warning: Could not parse save file. The save"
                f" file has a version of {save_version}, but this version of"
                f"the SHM Engine only supports up to {supported_version}\n"
                "Continuing without save file...\n"
            )
    if saveFile and validSave and supported_version:
        main = mainHandler(
            win,
            saveFile["RoomID"],
            saveFile,
            gameFile_name,
            gameFile_path,
            saveFileName,
        )
    else:
        main = mainHandler(
            win,
            starting_room,
            gameFile_name=gameFile_name,
            gameFile_path=gameFile_path,
            saveFileName=saveFileName,
        )
    main.fn_looper()


gameLoop = run


if __name__ == "__main__":

    # if len(sys.argv) > 1:
    # sys.argv[1]
    print(
        toml_reader.get_engine_info(
            "{Name} {MajorVersion}{PatchConnector}{Patch}\n"
            "{ReleaseDate}\n{Link}\nThis Release: '{Dist}'"
        )
    )
    sys.exit(0)

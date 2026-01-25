#!/usr/bin/env python3
import curses
from datetime import datetime
import importlib.util
import os.path
import sys
import time
import types

import save_handler
import tui
from tui import print3


class mainHandler:
    def __init__(
        self,
        win: curses.window,
        starting_room: int = 1,
        saveFile: dict = {},
        gameFile_name: str = "game",
        gameFile_path: str = "./game.py",
    ) -> None:
        self.game = self.setup_gameFile(gameFile_name, gameFile_path)
        self.gameFile_name = gameFile_name
        self.gameInfo = self.game.gameInfo
        self.game_state = self.game.game_state
        self.globaldebug = False
        self.history = self.game.history
        self.roomID = starting_room
        self.starting_room = self.gameInfo.get("starting_room", 1)
        self.stdscr = win
        self.win = win
        self.setup_stdscr()
        if saveFile:
            self.setup_loadSave(saveFile)

    def setup_gameFile(self, module_name: str, file_path: str) -> types.ModuleType:
        file_path = os.path.abspath(file_path)
        if file_path[-3:] != ".py":
            file_path = os.path.join(file_path, module_name)
            file_path = file_path + ".py"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        try:
            module = importlib.util.module_from_spec(spec)
        except:
            raise ImportError("Failed to import game file")
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def setup_loadSave(self, saveFile) -> None:
        if saveFile["Game"] != self.gameInfo["title"]:
            return
        for item in saveFile["game_state"]:
            setattr(self.game_state, item, saveFile["game_state"][item])
        if hasattr(self.game_state, "inventory"):
            for item in saveFile["inventory"]["items"]:
                self.game_state.inventory.items.append(item)
            for item in saveFile["inventory"]["keyItems"]:
                self.game_state.inventory.keyItems.append(item)

    def setup_stdscr(self) -> None:
        padding = 1
        padx1 = 0
        padx2 = 0
        pady1 = 0
        pady2 = 1
        self.win = tui.create_newwin(self.stdscr, padding, padx1, padx2, pady1, pady2)

    def db_debug(self) -> None:
        query = tui.option(self.win, "SHM Engine Debug Menu", ["Test room IDs"])
        match query:
            case 0:
                text = ""
                rooms = self.game.get_rooms(self.win)
                for roomno in rooms:
                    room = rooms[roomno]
                    if "Move" in room:
                        for idno in room["Move"]:
                            self.win.addstr(str(idno))
                            if isinstance(idno, int) and idno not in rooms:
                                text += f"Warning: Invalid ID {idno} in {roomno}!\n"
                    if "Automove" in room:
                        automove = room["Automove"]
                        self.win.addstr(str(automove))
                        if isinstance(automove, int) and automove not in rooms:
                            text += f"Warning: Invalid ID {automove} in {roomno}!\n"
                self.win.clear()
                if text:
                    print3(self.win, text, 33, 0)
                else:
                    print3(self.win, "Success! No errors found.", 36, 0)
                print3(self.win, "\nPress any key to exit Debug Menu...", 0, 0)
                self.win.getch()

    def db_log_error(
        self, text: str, colorcode=0, delay=0.01, pauseAtNewline=0.0
    ) -> None:
        timestamp = datetime.now().isoformat()
        with open("error.log", "a") as log:
            log.write(f"{timestamp} {text}\n")
        print3(self.win, text, colorcode=0, delay=0.01, pauseAtNewline=0.0)

    def db_roomIDerror(self, rooms: dict) -> None:
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

    def ui_drawtitlebar(self) -> None:
        string = "SHM Engine 1.1c 2026-01-25 - 'The Shopkeeper's Quest'"
        tui.draw_titlebar(self.stdscr, string)

    def ui_ending(self, end: str) -> None:
        save_handler.write_save(
            self.game_state, self.gameInfo, self.roomID, self.gameFile_name
        )
        if hasattr(game, "endingText") and end in self.game.endingText:
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

    def ui_lose(self, lose: str) -> None:
        time.sleep(0.25)
        if hasattr(game, "loseText") and lose in self.game.loseText:
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

    def ui_option(self, text: str, options: list, Inventory: bool = True) -> int:
        if not hasattr(self.game_state, "inventory"):
            Inventory = False
        query = 0
        choices = options
        if Inventory and hasattr(self.game_state, "inventory"):
            choices = options + ["Inventory"]
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
                    self.game_state, self.gameInfo, self.roomID, self.gameFile_name
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
            print3(self.win, "\n" + str(self.game_state.inventory))
            print3(self.win, "\nPress any key to exit inventory.")
            self.win.getch()
            query = self.ui_option(text, options, Inventory)
        if not isinstance(query, int):
            query = self.ui_option(text, options, Inventory)
        return query

    def fn_itemHandler(self, room: dict) -> None:
        if (
            "ItemRequirements" in room
            and room["ItemRequirements"]()
            or "ItemRequirements" not in room
        ):
            if "ItemText" in room:
                print3(self.win, "\n" + room["ItemText"])
            if (
                hasattr(self.game_state, "inventory")
                and self.game.keyItems
                and room["Item"] in self.game.keyItems
            ):
                self.game_state.inventory.getKeyItem(room["Item"], self.win)
            elif hasattr(self.game_state, "inventory"):
                self.game_state.inventory.getItem(room["Item"], self.win)
            self.win.getch()

    def fn_mainRoomHandler(self, room: dict, text: str) -> None:
        OptionsIndex = []
        Options = []
        for i in room["Move"]:
            OptionRequirements = "Option" + str(room["Move"].index(i)) + "Requirements"
            if OptionRequirements not in room or room[OptionRequirements]():
                OptionsIndex.append(i)
                optionText = room["Options"][room["Move"].index(i)]
                if self.globaldebug:
                    Options.append(optionText + " - RoomID: " + str(i))
                else:
                    Options.append(optionText)
        if "Inventory" in room and self.game_state.inventory and not room["Inventory"]:
            query = self.ui_option(text, Options, Inventory=False)
        else:
            query = self.ui_option(text, Options)
        self.roomID = OptionsIndex[query]

    def fn_gameLoop(self) -> None:
        rooms = self.game.get_rooms(self.win)
        self.win.clear()
        self.ui_drawtitlebar()
        if self.game.gameInfo["complevel"] != 1:
            complevel = self.game.gameInfo["complevel"]
            self.db_log_error(
                f"ERROR: This game (complevel {complevel}) is not compatible with this version of the SHM Engine (1.0 / complevel 1).",
                31,
                0,
            )
            print3(self.win, "\nPress any key to exit...", 0, 0)
            self.win.getch()
            sys.exit(1)
        if self.roomID in rooms:
            room = rooms[self.roomID]
        else:
            room = rooms[1]
            self.db_roomIDerror(rooms)
        text = ""
        if "Requirements" in room and not room["Requirements"]():
            print3(self.win, room["AlternateText"])
            text = room["AlternateText"]
        else:
            print3(self.win, room["Text"])
            text = room["Text"]
        if self.globaldebug:
            text += "\nRoomID: " + str(self.roomID) + "\nHistory: " + str(self.history)
        if "Script" in room:
            room["Script"]()
        if "Ending" in room:
            self.ui_ending(room["Ending"])
            self.roomID = self.starting_room
        if "Item" in room:
            self.fn_itemHandler(room)
        if "Automove" in room:
            if isinstance(room["Automove"], tuple) and room["Automove"][0] == "history":
                self.roomID = self.history[room["Automove"][1]]
            elif isinstance(room["Automove"], int):
                self.roomID = room["Automove"]
            time.sleep(1)
        elif "Move" in room:
            self.fn_mainRoomHandler(room, text)
        self.history.append(self.roomID)
        if len(self.history) > 10:
            self.history.pop(0)
        if "Lose" in room:
            self.ui_lose(room["Lose"])

    def fn_looper(self) -> None:
        while 1:
            self.fn_gameLoop()


def run(
    win: curses.window,
    starting_room: int,
    saveFile: dict = {},
    gameFile_name: str = "game",
    gameFile_path: str = "./",
) -> None:
    curses.curs_set(0)
    win.scrollok(True)
    tui.colorsetup(win)
    curses.cbreak()
    curses.noecho()
    if saveFile:
        main = mainHandler(
            win, saveFile["RoomID"], saveFile, gameFile_name, gameFile_path
        )
    else:
        main = mainHandler(
            win, starting_room, gameFile_name=gameFile_name, gameFile_path=gameFile_path
        )
    main.fn_looper()


gameLoop = run


if __name__ == "__main__":

    # if len(sys.argv) > 1:
    # sys.argv[1]
    print(
        """SHM Engine 1.1b\n2026-01-16\nhttps://github.com/solidlamp\n
        This release: 'The Shopkeeper's Quest Experimental'"""
    )

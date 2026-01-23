#!/usr/bin/env python3
import curses
from datetime import datetime
import time
import sys
import game
from game import game_state
import tui
from tui import print3


class mainHandler:
    def __init__(self, win: curses.window, starting_room: int = 1) -> None:
        self.game_state = game_state
        self.globaldebug = False
        self.history = game.history
        self.roomID = starting_room
        self.starting_room = starting_room
        self.fullscr = win
        self.stdscr = win #curses.newwin(1, 1, 13, 16) #win #curses.newwin(10,10,10,20) #win.subwin(0, 0) #curses.newpad(100, 100)#win# curses.newwin(10, 20, 3, 6)
        #self.setup_stdscr()
        self.setup_stdscr()

    def setup_stdscr(self) -> None:
        max_y, max_x = self.fullscr.getmaxyx()
        if max_y < 5 or max_x < 5:
            return
        begin_x = 1
        begin_y = 1
        height = (max_y - 3)
        width = (max_x - 2)
        self.stdscr = curses.newwin(height, width, begin_y, begin_x)
        self.stdscr.scrollok(True)
        self.stdscr.keypad(True)
        tui.colorsetup(self.stdscr)

    def db_debug(self) -> None:
        query = tui.option(self.stdscr, "SHM Engine Debug Menu", ["Test room IDs"])
        match query:
            case 0:
                text = ""
                rooms = game.get_rooms(self.stdscr)
                for roomno in rooms:
                    room = rooms[roomno]
                    if "Move" in room:
                        for idno in room["Move"]:
                            self.stdscr.addstr(str(idno))
                            if isinstance(idno, int) and idno not in rooms:
                                text += f"Warning: Invalid ID {idno} in {roomno}!\n"
                    if "Automove" in room:
                        automove = room["Automove"]
                        self.stdscr.addstr(str(automove))
                        if isinstance(automove, int) and automove not in rooms:
                            text += f"Warning: Invalid ID {automove} in {roomno}!\n"
                self.stdscr.clear()
                if text:
                    print3(self.stdscr, text, 33, 0)
                else:
                    print3(self.stdscr, "Success! No errors found.", 36, 0)
                print3(self.stdscr, "\nPress any key to exit Debug Menu...", 0, 0)
                self.stdscr.getch()

    def db_log_error(
        self, text: str, colorcode=0, delay=0.01, pauseAtNewline=0.0
    ) -> None:
        timestamp = datetime.now().isoformat()
        with open("error.log", "a") as log:
            log.write(f"{timestamp} {text}\n")
        print3(self.stdscr, text, colorcode=0, delay=0.01, pauseAtNewline=0.0)

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
        print3(self.stdscr, "\nPress any key to exit...", 0, 0)

    def ui_drawtitlebar(self) -> None:
        tui.draw_titlebar(self.fullscr)

    def ui_ending(self, end: str) -> None:
        if hasattr(game, "endingText") and end in game.endingText:
            print3(
                self.stdscr,
                "\n" + game.endingText[end].replace("|", end),
                0,
                0.015,
                0.65,
            )
        time.sleep(1.5)
        self.stdscr.clear()
        print3(self.stdscr, game.defaultEnding.replace("|", end), 0, 0.015, 0.65)
        time.sleep(3.5)

    def ui_lose(self, lose: str) -> None:
        time.sleep(0.25)
        if hasattr(game, "loseText") and lose in game.loseText:
            printText = "\n" + game.loseText[lose].replace("|", lose)
        else:
            printText = game.defaultLose.replace("|", lose)
        print3(self.stdscr, printText, 0, 0.015, 0.65)
        self.stdscr.clear()
        time.sleep(0.5)
        query = tui.option(self.stdscr, printText + "Try again?", ["Yes", "No"])
        if query == 1 or query == "q":
            sys.exit()
        else:
            self.roomID = 1

    def ui_option(self, text: str, options: list, Inventory: bool = True) -> int | str:
        tui.draw_titlebar(self.fullscr)
        if not hasattr(self.game_state, "inventory"):
            Inventory = False
        query = 0
        choices = options
        if Inventory and hasattr(self.game_state, "inventory"):
            choices = options + ["Inventory"]
        query = tui.option(self.stdscr, text, choices)
        if query == "q":
            query = tui.option(
                self.stdscr, "Are you sure you want to quit?", ["Quit Game", "Return to Game"]
            )
            if query == 0 or query == "q":
                sys.exit()
            else:
                query = self.ui_option(text, options, Inventory)
        elif query == "d":
            self.db_debug()
            query = self.ui_option(text, options, Inventory)
        elif Inventory and query == choices.index("Inventory"):
            self.stdscr.clear()
            print3(self.stdscr, "\n" + str(self.game_state.inventory))
            print3(self.stdscr, "\nPress any key to exit inventory.")
            self.stdscr.getch()
            query = self.ui_option(text, options, Inventory)
        return query

    def fn_itemHandler(self, room: dict) -> None:
        if (
            "ItemRequirements" in room
            and room["ItemRequirements"]()
            or "ItemRequirements" not in room
        ):
            if "ItemText" in room:
                print3(self.stdscr, "\n" + room["ItemText"])
            if (
                hasattr(self.game_state, "inventory")
                and game.keyItems
                and room["Item"] in game.keyItems
            ):
                self.game_state.inventory.getKeyItem(room["Item"], self.stdscr)
            elif hasattr(self.game_state, "inventory"):
                self.game_state.inventory.getItem(room["Item"], self.stdscr)
            self.stdscr.getch()

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
        rooms = game.get_rooms(self.stdscr)
        self.stdscr.clear()
        self.ui_drawtitlebar()
        if game.gameInfo["complevel"] != 1:
            complevel = game.gameInfo["complevel"]
            self.db_log_error(
                f"ERROR: This game (complevel {complevel}) is not compatible with this version of the SHM Engine (1.0 / complevel 1).",
                31,
                0,
            )
            print3(self.stdscr, "\nPress any key to exit...", 0, 0)
            self.stdscr.getch()
            sys.exit(1)
        if self.roomID in rooms:
            room = rooms[self.roomID]
        else:
            room = rooms[1]
            self.db_roomIDerror(rooms)
        text = ""
        if "Requirements" in room and not room["Requirements"]():
            print3(self.stdscr, room["AlternateText"])
            text = room["AlternateText"]
        else:
            print3(self.stdscr, room["Text"])
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


def run(win: curses.window, starting_room: int) -> None:
    curses.curs_set(0)
    win.scrollok(True)
    tui.colorsetup(win)
    curses.cbreak()
    curses.noecho()
    main = mainHandler(win, starting_room)
    main.fn_looper()


gameLoop = run


if __name__ == "__main__":

    # if len(sys.argv) > 1:
    # sys.argv[1]
    print(
        """SHM Engine 1.1b\n2026-01-16\nhttps://github.com/solidlamp\n
        This release: 'The Shopkeeper's Quest Experimental'"""
    )

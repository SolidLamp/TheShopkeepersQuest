#!/usr/bin/env python3
import curses

from src import game, tui

# NOTE: This script is for testing purposes only!


def doit3(room: dict, string: str) -> str:
    if string in room:
        title = room[string]
        title = str(title).replace("\n", r"\n")
        title = str(title).replace("\033", r"\033")
        text = f"{string} = {title}\n"
        return text
    else:
        return ""


def doit3text(room: dict, string: str) -> str:
    if string in room:
        title = room[string]
        title = str(title).replace("\n", r"\n")
        title = str(title).replace("\033", r"\033")
        text = f'{string} = "{title}"\n'
        return text
    else:
        return ""


def doit3list(room: dict, string: str) -> str:
    if string in room:
        title = room[string]
        title = str(title).replace("\n", r"\n")
        title = str(title).replace("\033", r"\033")
        title = str(title).replace(",", ",\n                ")
        title = str(title).replace("[", "[\n                ")
        title = str(title).replace("]", ",\n           ]")
        text = f"{string} = {title}\n"
        return text
    else:
        return ""


def doit2(win: curses.window) -> str:
    curses.curs_set(0)
    win.scrollok(True)
    tui.colorsetup(win)
    curses.cbreak()
    rooms = game.get_rooms(win)
    text = ""
    for roomno in rooms:
        room = rooms[roomno]
        text = text + f"[{roomno}]\n"
        text = text + doit3text(room, "Text")
        text = text + doit3text(room, "AlternateText")
        text = text + doit3text(room, "Item")
        text = text + doit3text(room, "ItemText")
        text = text + doit3(room, "Automove")
        text = text + doit3list(room, "Options")
        text = text + doit3(room, "Move")
        text = text + doit3text(room, "Ending")
        text = text + doit3text(room, "Lose")
        text = text + "\n"
    return text


def doit() -> None:
    d = curses.wrapper(doit2)
    print(d)
    with open("file.txt") as f:
        f.write(d)

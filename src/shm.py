#!/usr/bin/env python3
import time
import sys
import game
from game import game_state, get_rooms
import tui
from tui import print3

game_state = game_state
history = game.history

if __name__ == "__main__":

    if len(sys.argv) > 1:
        sys.argv[1]
    else:
        print(
            "SHM Engine 0.9b\n2025-09-27\nhttps://github.com/solidlamp\nThis release: The Shopkeeper's Quest Experimental 2025-09-27"
        )

roomID = 1

def option(win, text, options, Inventory=True):
    query = 0
    query = tui.option(win, text, options)
    if query == "q":
        query = tui.option(win, "Are you sure you want to quit?", ["Yes", "No"])
        if query == 0 or query == "q":
            sys.exit()
        else:
            return 255
    return query


def gameLoop(win, starting_room=0):
    rooms = game.get_rooms(win)
    win.clear()
    if game.gameInfo["complevel"] != 0:
        print3(win, "ERROR: This game is not compatible with this version of the SHM Engine.", 1, 0)
        print3(win, "\nPress any key to exit...", 0, 0)
        win.getch()
        sys.exit(1)
    global roomID
    if starting_room:
        roomID = starting_room
    room = rooms[roomID]
    text = ""
    if "Requirements" in room and not room["Requirements"]():
        print3(win, room["AlternateText"])
        text = room["AlternateText"]
    else:
        print3(win, room["Text"])
        text = room["Text"]
    if "Script" in room:
        room["Script"]()
    if "Item" in room:
        if (
            "ItemRequirements" in room
            and room["ItemRequirements"]()
            or "ItemRequirements" not in room
        ):
            if "ItemText" in room:
                print3(win, room["ItemText"])
            if game_state.inventory and game.keyItems and room["Item"] in game.keyItems:
                game_state.inventory.getKeyItem(room["Item"])
            elif game_state.inventory:
                game_state.inventory.getItem(room["Item"])
            win.getch()
    if "Automove" in room:
        if isinstance(room["Automove"], tuple) and room["Automove"][0] == "history":
            roomID = history[room["Automove"][1]]
        elif isinstance(room["Automove"], int):
            roomID = room["Automove"]
        time.sleep(0.5)
    else:
        OptionsIndex = []
        Options = []
        for i in room["Move"]:
            OptionRequirements = "Option" + str(room["Move"].index(i)) + "Requirements"
            if OptionRequirements not in room or room[OptionRequirements]():
                OptionsIndex.append(i)
                Options.append(room["Options"][room["Move"].index(i)])
        if "Inventory" in room and game_state.inventory and not room["Inventory"]:
            query = option(win, text, Options)#, Inventory=False)
        else:
            query = option(win, text, Options)
        roomID = OptionsIndex[query]
    history.append(roomID)
    if len(history) > 10:
        history.pop(0)

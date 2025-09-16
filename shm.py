import time
from dataclasses import dataclass
import random
from game import game_state
from game import rooms
import game

if game.game_state:
    from game import game_state
history = game.history

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        sys.argv[1]
    else:
        print(
            "SHM Engine 0.7b\n2025-09-16\nhttps://github.com/solidlamp\nThis release: The Shopkeeper's Quest Experimental - 2025-09-16"
        )

roomID = 1


def print2(text, newline=True, pauseAtNewline=0.0, endingChar=False):
    for char in text:
        if char == "\n":
            time.sleep(pauseAtNewline)
        print(char, end="", flush=True)
        time.sleep(0.01)
    if newline:
        print()


def option(choice, Inventory=True):
    print()
    for i, options in enumerate(choice, start=1):
        print2(f"{i}. {options}")
    if Inventory:
        print2("i. Inventory")
    query = input(">>> ")
    if query == "i" and Inventory:
        print(game_state.inventory)
    if query == "xyzzy":
        print(game_state)
        debug()
    if query.casefold() == "q!".casefold():
        exit()
    if query.casefold() == "q".casefold():
        print2("Are you sure you want to quit?")
        query = input(">>> ")
        if query.casefold() == "y".casefold():
            exit()
        else:
            query = "255"
    print()
    return query


def ending(end):
    print2(game.endingText[end].replace("|", end), pauseAtNewline=0.65)
    print("\n\n")
    print2(game.defaultEnding.replace("|", end), pauseAtNewline=0.65)
    time.sleep(2.5)


def lose(text):
    print("\n\n")
    time.sleep(0.25)
    print("\033[31m\033[1mYou died!\033[0m")
    print("'" + text + "'")
    time.sleep(0.5)
    print("\n\n\nTry again?")


def gameLoop(starting_room=False):
    global roomID
    if starting_room:
        roomID = starting_room
    room = rooms[roomID]
    if "Requirements" in room and not room["Requirements"]():
        print2(room["AlternateText"])
    else:
        print2(room["Text"])
    if "Script" in room:
        room["Script"]()
    if "Automove" in room:
        if isinstance(room["Automove"], tuple) and room["Automove"][0] == "history":
            roomID = history[room["Automove"][1]]
        elif isinstance(room["Automove"], int):
            roomID = room["Automove"]
    else:
        OptionsIndex = []
        Options = []
        for i in room["Move"]:
            OptionRequirements = "Option" + str(room["Move"].index(i)) + "Requirements"
            if OptionRequirements not in room or room[OptionRequirements]():
                OptionsIndex.append(i)
                Options.append(room["Options"][room["Move"].index(i)])
        if "Inventory" in room and inventory in game_state and not room["Inventory"]:
            query = option(Options, Inventory=False)
        else:
            query = option(Options)
        if query.isdigit() and int(query) <= len(Options):
            roomID = OptionsIndex[int(query) - 1]
    history.append(roomID)
    if len(history) > 10:
        history.pop(0)

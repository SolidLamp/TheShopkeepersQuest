import time
from dataclasses import dataclass
import random
from example import game_state
from example import inventory
from example import rooms

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        sys.argv[1]
    else:
        print(
            "SHM Engine 0.7\n2025-09-14\nhttps://github.com/solidlamp\nThis release: The Shopkeeper's Quest Experimental - 2025-09-14"
        )

roomID = 1
history = []

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
    if query == "q":
        print2("Are you sure you want to quit?")
        query = input(">>> ")
        if query.casefold() == "y".casefold():
            exit()
        else:
            query = 255
    print()
    return query

def gameLoop(): 
    global roomID
    room = rooms[roomID]
    if "Requirements" in room and not room["Requirements"]():
        print2(room["AlternateText"])
    else:
        print2(room["Text"])
    if "Automove" in room:
        roomID = room["Automove"]
    else:
        OptionsIndex = []
        Options = []
        for i in room["Move"]:
            OptionRequirements = "Option" + str(room["Move"].index(i)) + "Requirements"
            if OptionRequirements not in room or room[OptionRequirements]():
                OptionsIndex.append(i)
                Options.append(room["Options"][room["Move"].index(i)]) 
        query = option(Options)
        if query.isdigit() and int(query) <= len(Options):
            roomID = OptionsIndex[int(query) - 1]
    if "Script" in room:
        room["Script"]()
    history.append(roomID)
    if len(history) > 5:
        history.pop(0)


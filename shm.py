import time
from game import game_state, rooms
import game
import sys

game_state = game_state
history = game.history

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        sys.argv[1]
    else:
        print(
            "SHM Engine 0.8\n2025-09-17\nhttps://github.com/solidlamp\nThis release: The Shopkeeper's Quest Project Edition"
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
        query = input(">>> ")
        global roomID
        roomID = int(query)
    if query.casefold() == "q!".casefold():
        sys.exit()
    if query.casefold() == "q".casefold():
        print2("Are you sure you want to quit?")
        query = input(">>> ")
        if query.casefold() == "y".casefold():
            sys.exit()
        else:
            query = "255"
    print()
    return query


def gameLoop(starting_room=False):
    if game.complevel != 0:
        print("This game is not compatible with this version of the SHM Engine.")
        sys.exit(1)
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
    if "Item" in room:
        if (
            "ItemRequirements" in room
            and room["ItemRequirements"]()
            or "ItemRequirements" not in room
        ):
            if "ItemText" in room:
                print2(room["ItemText"])
            if game_state.inventory and game.keyItems and room["Item"] in game.keyItems:
                game_state.inventory.getKeyItem(room["Item"])
            elif game_state.inventory:
                game_state.inventory.getItem(room["Item"])
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
        if "Inventory" in room and game_state.inventory and not room["Inventory"]:
            query = option(Options, Inventory=False)
        else:
            query = option(Options)
        if query.isdigit() and int(query) <= len(Options):
            roomID = OptionsIndex[int(query) - 1]
    history.append(roomID)
    if len(history) > 10:
        history.pop(0)

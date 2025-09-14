#Tribute
import time
from dataclasses import dataclass
import random
import shm

print2 = shm.print2
roomID = 1


history = []
inventory = ["Item","Golden Idol"]
@dataclass
class gameState:
    inventory: inventory
    rubies: int = 0
    shopkeeperName: str = "The Shopkeeper"
    position: float = 0.0
    beatenGame: bool = False
    caveOpened: bool = False
    fletcherOpen: bool = True

game_state = gameState(inventory=inventory)


def option(choice, Inventory=True):
    print()
    for i, options in enumerate(choice, start=1):
        print2(f"{i}. {options}")
    if Inventory:
        print2("i. Inventory")
    query = input(">>> ")
    if query == "q":
        exit()
    print()
    return query



rooms = {
    0: {
        "Text": "This is the Debug Room.",
        "Options": ["Go to 2", "Go to 3"],
        "Move": [2,3],
    },
    1: {
        "Text": "This is the First Room.",
        "Options": ["Go to 2", "Go to 3"],
        "Move": [2,3],
    },
    2: {
        "Text": "You are within the cave. It is a dead-end. The only path is back where you came.",
        "AlternateText": "You are within the cave. It is a dead-end. The only path is back where you came.",
        "Item": "Golden Idol",
        "ItemRequirement": lambda: "Golden Idol" in inventory,
        "ItemText": "You see, on the floor of the cave, a \033[47mGolden Idol\033[0m.",
        "Options": ["Go to 1", "Go to 3"],
        "Move": [1,3],
    },
    3: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your northeast, south and northwest.",
        "Requirements": lambda: game_state.caveOpened,
        "AlternateText": "You are within the cave. It is difficult to see. There is a path to your northeast and south. There is a lot of rubble to your northwest.",
        "ItemText": "You see, on the floor of the cave, a \033[47mGolden Idol\033[0m.",
        "Options": ["Go to 1", "Go to 4","Go to 2"],
        #"Option1Requirements": lambda: not game_state.caveOpened,
        "Option2Requirements": lambda: game_state.caveOpened,
        "Move": [1,4,2],
    },
    4: {
        "Text": "You opened the cave.",
        "Script": lambda: setattr(game_state, "caveOpened", True),
        "Automove": 3,
    },
}

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
        Options = []
        for i in range(len(room["Move"])):
            print(i)
            OptionRequirements = "Option" + str(i) + "Requirements"
            if OptionRequirements not in room or room[OptionRequirements]():
                Options.append(room["Move"][i])
        query = option(Options)
        if query.isdigit() and int(query) <= len(room["Move"]):
            roomID = room["Move"][int(query) - 1]
    if "Script" in room:
        room["Script"]()
    history.append(roomID)
    if len(history) > 5:
        history.pop(0)

def test():
    global roomID
    query = option(rooms[1]["Move"])
    if query == "1":
        action2()
    elif query == "2":
        action3()
    else:
        print2("WHAT?")
        action1()





while True:
    gameLoop()
















def action1():
    print2("")
    query = option(["Option 1", "Option 2"])
    if query == "1":
        action2()
    elif query == "2":
        action3()
    else:
        print2("WHAT?")
        action1()

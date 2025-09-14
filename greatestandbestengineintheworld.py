#Tribute
import time
from dataclasses import dataclass
import random
import shm
from example import game_state
from example import inventory
from example import rooms

print2 = shm.print2
roomID = 1


history = []

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


while True:
    gameLoop()

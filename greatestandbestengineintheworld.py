#Tribute
import time
from dataclasses import dataclass
import random
import shm

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



rooms = {
    1: {
        "Text": "This is the First Room.",
        "Options": ["Go to 2", "Go to 3"],
        "Move": [2,3]
    },
    2: {
        "Text": "This is the Second Room.",
        "Options": ["Go to 1", "Go to 3"],
        "Move": [1,3]
    },
    3: {
        "Text": "This is the Third Room.",
        "Options": ["Go to 1", "Go to 2"],
        "Move": [1,2]
    },
}

def gameLoop(): 
    global roomID
    print(rooms[roomID]["Move"]) 
    query = option(rooms[roomID]["Options"])
    print(len(rooms[roomID]["Move"]))
    if query.isdigit() and int(query) <= len(rooms[roomID]["Move"]):
        query = int(query) - 1
        print("Valid")
        roomID = rooms[roomID]["Move"][query]
        history.append(roomID)
        if len(history) > 5:
            history.pop(0)
        print(roomID)

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

print(rooms[roomID]["Move"]) 
query = option(rooms[1]["Options"])
print(len(rooms[roomID]["Move"]))
if query.isdigit() and int(query) <= len(rooms[roomID]["Move"]):
    query = int(query) - 1
    print("Valid")
    roomID = rooms[roomID]["Move"][query]
    history.append(roomID)
    if len(history) > 5:
        history.pop(0)
    print(roomID)

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

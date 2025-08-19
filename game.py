import time

def print2(a):
    for i in a:
        print(i, end="", flush=True)
        time.sleep(0.01)
    print()

def option(a):
    print()
    for i, options in enumerate(a, start=1):
        print2(f"{i}. {options}")
    query=input(">>> ")
    print()
    return(query)




def ending(a):
    print()
    print()
    print()
    time.sleep(0.25)
    print("You achieved the:")
    time.sleep(0.25)
    print()
    print("\033[1m" + a + "\033[0m")
    time.sleep(0.25)
    print()
    print("Ending.")
    time.sleep(0.5)
    print()
    print()
    print()
    print("Try again?")

def lose(text):
    print()
    print()
    print()
    time.sleep(0.25)
    print("You died!")
    print(text)
    time.sleep(0.5)
    print()
    print()
    print()
    print("Try again?")

global rubies
rubies=int(0)

def getRuby(num):
    global rubies
    print()
    print2("You got \033[1m" + str(num) + "\033[0m Rubies!")
    rubies=rubies+num
    print("\033[0m")
    print2("You currently have \033[1m" + str(rubies) + "\033[0m Rubies.")
    print()


# The Game

def intro():
    print("\033[1m" + "The Shopkeeper's Quest" + "\033[0m\n" + "or" + "\n\033[1" + "The Merchant's Q est" + "\ \033[0\" + "[[[rking title]\\n\033[0m]")
    print2("Use the numbers to choose options")
    query = option(["Begin","Quit"])
    if query == "1":
        print2("You are a travelling merchant, approaching a new town to sell your wares  another region.\nAs y you approach the town, the atmosphere seems odd and eerily silent, almost frightening in a ay. \n"Suddently, a man appears, and walks ver\n"The man speaks, 'Greetings. I am a local shopkeeper, just outside the limits of our little village Siopwyrdigofaint/Llansiopwyrdod/Siopwyrd/Llanamausiop/Llanerchwyrd.\nMany come for my high-quality wares, but none have done such today, for a mystical spell has bewitched all.\nAny that resided within the town limits have disappeared.'\nThe man grunts and scratches his chin.\nHe looks back at the town with a longing expression, before turning his gaze back to you. \n'It worries me, you know?' he continues, 'There's an old legend that if all seems to disappear overnight, then this marks a dark path for the world.'\nThe man sighs deeply, and waits a moment before speaking again, 'I do have some experience with magic, however.\nI can reverse it, but I need 3 mystical items; the first, a rusted sword; the second, an amber necklace; and the third, a silver _.\nWith those three items, I believe I can bring everything back to normal.\nI would get them myself, but my adventuring days are behind me.\nIf it helps, I believe the bazaar was unaffected - it, too, was beyond the limits of the main town.\nWhen you obtain the items, come see me in my shop.\nI shall be seeing you, then.'")
        print()
        gameLoop()
    else:
        exit()

#altar uuddlrlrba

def gameLoop():
    print2("You are standing in a field. There is a road to the north, leading to a town, a forest to the east, a cave to the south, a shop and bazaar to the west, and there are some bushes nearby.")
    query = option(["Go to the forest","Follow the road to town","Explore the cave","Go to the shop","Go to the bazaar"])
    if query == "1":
        forest()
    elif query == "2":
        road()
    elif query == "3":
        cave()
    elif query == "4":
        shop()
    elif query == "5":
        bazaar()
    else:
        field()
    query = option(["Yes","No"])
    if query == "1":
        gameLoop()
    elif query == "2":
        exit()
    else:
        exit()

def field():
    print2("You are standing in a field.")
    query = option(["Go to the forest","Follow the road to town","Explore the cave","Go to the shop","Go to the bazaar"])
    if query == "1":
        forest()
    elif query == "2":
        road()
    elif query == "3":
        cave()
    elif query == "4":
        shop()
    elif query == "5":
        bazaar()
    else:
        field()

def forest():
    print2("You come to the opening of the forest. The forest is vast and the trees tower over you.")
    query = option(["Go further in","Leave"])
    if query == "1":
        forest2()
    elif query == "2":
        field()
    else:
        forest()

def forest2():
    print2("You are deep in the forest. It is dim, and difficult to see.")
    query = option(["Go further in","Leave"])
    if query == "1":
        forest3()
    elif query == "2":
        forest()
    else:
        forest2()

def forest3():
    print2("You come to a clearing, deep in the forest. There is a bonobo sitting, facing you")
    query = option(["Fight the bonobo","Leave"])
    if query == "1":
        if 1 == 1:
            print2("You manage to defeat the bonobo, using your weapon.")
            print2("You manage to find a chest, containing 15 rubies!")
            getRuby(15)
            print2("Underneath all the rubies, you find the rusted sword.")
            forest2()
        else:
            print2("You attempt to fight the bonobo, but it easily overpowers you. You are killed.")
            lose("What did you think was going to happen?")
    elif query == "2":
        print2("You attempt to leave, but the bonobo catches you. You are killed.")
        lose("Bonobos are quite agressive.")
    else:
        forest3()




def action1():
    print2("")
    query = option(["",""])
    if query == "1":
        action2()
    elif query == "2":
        action3()
    else:
        print2("WHAT?")
        action1()


def action2():
    print2("")

def action3():
    print2("")

intro()
exit
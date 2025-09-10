import time
from dataclasses import dataclass
import random
import shm

print2 = shm.print2

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
        exit()
    print()
    return (query)


def ending(end):
    if end in endingsWithCustomText:
        index = endingsWithCustomText.index(end)
        print2(endingCustomText[index].replace("|", end), pauseAtNewline=0.65)
    print("\n\n")
    print2(defaultEndingText.replace("|", end), pauseAtNewline=0.65)
    time.sleep(2.5)


def lose(text):
    print("\n\n")
    time.sleep(0.25)
    print("\033[31m\033[1mYou died!\033[0m")
    print("'" + text + "'")
    time.sleep(0.5)
    print("\n\n\nTry again?")


ShopkeeperQuotesExit = [
    "Remember, tomorrow is another day.", "Be seeing you.",
    "I wish you the best of luck.", "I give you my grace.",
    "I wish you luck on your quest.", "I'll get started on my tea.",
    "May all the spirits be with you."
]

ShopkeeperQuotes = [
    "Welcome!", "Sit down, my friend. Stay a while.",
    "You'll always be welcome here in my shop.",
    "Have a look at my wares. They could prove to be useful.",
    "Sorry I can't give discounts - I have a business to run, and I must make my money somehow.",
    "I don't blame you for coming inside in this winter.",
    "Sit down a while. I don't want you too stressed, my friend.",
    "I always believe that everyone has a tale worth telling - maybe talk to more people.",
    "Have you checked out the bazaar? There's a fisherman there who sells excellent-quality rods.",
    "Have you heard the news about the King? It's said that he's fallen ill. He's a good man - I hope he fully recovers.",
    "Have you seen the nearby forest? There's been some monkey sightings there."
]

endingsWithCustomText = ["Good", "Secret", "SHM"]
endingCustomText = [
    "And so, overnight, all the people returned to the village, as if they had never left.\nSoon after, the village was lifted into high spirits as the harvest had been the best in almost thirty years.\nDespite the prospering village, you decided to leave.\nYou had no desire to stay after the events you just experienced, and you would rather leave than stay to make some money.",
    "And so, overnight, you became the new shopkeeper, but nothing really changed in the end.\nThe villagers never returned, but many travellers came, hearing about what happened.\nMany decided te stay after a plentiful harvest brought good omens to the village.\nThis, however, would not be the last of it...\n...and you knew that.",
    "You achieved the\n|\nEnding.\nTry Again?",
]
defaultEndingText = "\033[1mThe Shopkeeper's Quest\033[0m\n\nSchool Project Edition\n\nWith inspiration from:\nColossal Cave Adventure, by Will Crowther and Don Woods;\nKing's Quest, by Sierra On-Line;\nHenry Stickmin, by Puffballs United;\nMinecraft: Story Mode, by Telltale Games;\n and RTX Morshu: The Game, by koshkamatew\nWith special thanks to\n\033[1m\033[33mYOU\033[0m\nfor playing the game,\nfor if a tree falls and no one hears it, does it make a noise?"

mysticalRocks = {
    "What you think is an Emerald": 80,
    "A Funny-looking Rock": 5,
    "A Chunk of Marble": 15,
    "Some Tourmaline, maybe": 50,
    "A Stone that looks kind of like a face": 150,
    "A Weird shard of something": 20,
    "Some strange stone": 100,
    "A beautiful, azure blue rock": 500,
}


@dataclass
class Inventory:
    items: list[str] = None
    keyItems: list[str] = None

    def __post_init__(self):
        self.items = [] if self.items is None else self.items
        self.keyItems = [] if self.keyItems is None else self.keyItems

    def getItem(self, item: str):
        print2("\nYou got \033[1m" + str(item) + "\033[0m!")
        self.items.append(item)

    def getKeyItem(self, item: str):
        print2("\nYou got \033[1m" + str(item) + "\033[0m!")
        self.keyItems.append(item)

    def __str__(self):
        if not self.items and not self.keyItems:
            return "Your inventory is empty"
        output = []
        if self.items:
            output.append("Items:\n" + "\n".join(f"- {item}"
                                                 for item in self.items))
        if self.keyItems:
            output.append("Key Items:\n" +
                          "\n".join(f"- {item}" for item in self.keyItems))
        return "\n".join(output)


#Rusted Sword (Forest), Amber Necklace (Town), AncientKey (Fountain) and Golden Idol (Cave)
@dataclass
class gameState:
    inventory: Inventory
    rubies: int = 0
    shopkeeperName: str = "The Shopkeeper"
    position: float = 0.0
    beatenGame: bool = False
    caveOpened: bool = False
    fletcherOpen: bool = True

    def getRuby(self, obtained: int):
        print2("\nYou got \033[1m" + str(obtained) + "\033[0m Rubies!")
        self.rubies += obtained
        print2("\033[0m You currently have \033[1m" + str(self.rubies) +
               "\033[0m Rubies.\n")


game_state = gameState(inventory=Inventory(items=[]))


def caveItem():
    if random.randrange(1, 20) == 8:
        foundRock = random.choice(list(mysticalRocks))
        print2("On the ground, you find " + foundRock)
        game_state.inventory.getItem(foundRock)


##


def intro():
    print("\033[36m\033[40m" + r"""___ _  _ ____ 
 |  |__| |___ 
 |  |  | |___ 

____ _  _ ____ ___  _  _ ____ ____ ___  ____ ____ ____ 
[__  |__| |  | |__] |_/  |___ |___ |__] |___ |__/ [__  
___] |  | |__| |    | \_ |___ |___ |    |___ |  \ ___] 

____ _  _ ____ ____ ___ 
|  | |  | |___ [__   |  
|_\| |__| |___ ___]  |  
                        """ + "\033[0m")
    print2(
        "Use the numbers to choose options, or press 'Q' to quit at any time")
    query = option(["Begin", "Skip Intro", "Quit"], Inventory=False)
    if query == "1":
        print2(
            "You are a travelling merchant, approaching a new village to sell your wares in another region.\nAs you approach the village, the atmosphere seems odd and eerily silent, almost frightening in a way. \nSuddently, a man appears, and walks in your direction.\nThe man speaks, \033[33m'Greetings. I'm a local shopkeeper, just outside the limits of our little village.\nMany come for my high-quality wares, but none have done such today, for a mystical spell has bewitched them..\nAny that resided within the village limits have disappeared.'\033[0m\nThe man grunts and scratches his chin.\nHe looks back at the village with a longing expression, before turning his gaze back to you. \n\033[33m'It worries me, you know?'\033[0m he continues, \033[33m'There's an old legend that if all seems to disappear overnight, then this marks a dark path for the world.'\033[0m\nThe man sighs deeply, and waits a moment before speaking again, \033[33m'I do have some experience with magic.\nI can reverse it, but I need 3 mystical items; the first, a rusted sword; the second, an amber necklace; and the third, a golden idol.\nWith those three items, I believe I can bring everything back to normal.\nI would get them myself, but my adventuring days are behind me.\nIf it helps, I believe the bazaar was unaffected - it, too, was beyond the main limits of the village.\nWhen you obtain the items, come see me in my shop.\nI shall be seeing you, then.'\033[0m"
        )
        print()
        gameLoop()
    if query == "2":
        field()
    else:
        exit()


#altar uuddlrlrba


def gameLoop():
    print2(
        "You are standing in a field. There is a road to the north, leading to a village, a forest to the east, a cave to the south, a shop and bazaar to the west, and there are some bushes nearby."
    )
    query = option([
        "Go to the forest", "Follow the road to the village",
        "Explore the cave", "Go to " + game_state.shopkeeperName + "'s shop",
        "Go to the bazaar"
    ])
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
    query = option(["Yes", "No"])
    if query == "1":
        gameLoop()
    elif query == "2":
        exit()
    else:
        exit()


def field():
    print2("You are standing in a field.")
    query = option([
        "Go to the forest", "Follow the road to the village",
        "Explore the cave", "Go to " + game_state.shopkeeperName + "'s shop",
        "Go to the bazaar"
    ])
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
    print2(
        "You come to the opening of the forest. The forest is vast and the trees tower over you."
    )
    query = option(["Leave", "Go further in"])
    if query == "2":
        forest2()
    elif query == "1":
        field()
    else:
        forest()


def forest2():
    print2("You are deep in the forest. It is dim, and difficult to see.")
    if "Rusted Sword" in game_state.inventory.keyItems:
        query = option(["Leave"])
    else:
        query = option(["Leave", "Go further in"])
    if query == "2":
        if "Rusted Sword" not in game_state.inventory.keyItems:
            forest3()
    elif query == "1":
        forest()
    else:
        forest2()


def forest3():
    print2(
        "You come to a clearing, deep in the forest. There is a bonobo sitting, facing you"
    )
    query = option(["Fight the bonobo", "Leave"])
    if query == "1":
        if "Bow and Arrow" in game_state.inventory.keyItems:
            print2("You manage to defeat the bonobo, using your weapon.")
            print2("You manage to find a chest, containing 15 rubies!")
            game_state.getRuby(15)
            print2("Underneath all the rubies, you find the rusted sword.")
            game_state.inventory.getKeyItem("Rusted Sword")
            forest2()
        else:
            print2(
                "You attempt to fight the bonobo, but it easily overpowers you. You are killed."
            )
            lose("What did you think was going to happen?")
    elif query == "2":
        print2(
            "You attempt to leave, but the bonobo catches you. You are killed."
        )
        lose("Bonobos are quite agressive.")
    else:
        forest3()


def road():
    print2(
        "You follow the road, but although it looks like a short distance, it feels like a long journey, as if it were a mile long. You wish for a mule to travel on."
    )
    query = option(["Go to the village", "Go to the field"])
    if query == "1":
        townArrival()
    elif query == "2":
        field()
    else:
        action1()


def townArrival():
    print2(
        "You follow the road to the village. It seems barren and no one is there."
    )
    query = option(["Follow the High Street further", "Go Back"])
    if query == "1":
        town2()
    elif query == "2":
        road()
    else:
        town()


def town():
    print2("You are in the village. It seems barren and no one is there.")
    query = option(["Follow the High Street further", "Go Back"])
    if query == "1":
        town2()
    elif query == "2":
        road()
    else:
        town()


def town2():
    print2(
        "You are in the high street of the village. The village centre is to your north."
    )
    query = option(["Go to the village centre", "Go South"])
    if query == "1":
        town3()
    elif query == "2":
        town()
    else:
        town2()


def town3():
    print2(
        "You are in the centre of the village. There are paths each direction, with a fountain in the middle."
    )
    query = option(
        ["Go North", "Go East", "Go South", "Go West", "Go to the Fountain"])
    if query == "1":
        townNorth()
    elif query == "2":
        townEast()
    elif query == "3":
        town2()
    elif query == "4":
        townWest()
    elif query == "5":
        fountain()
    else:
        town3()


def fountain():
    print2("You are at the fountain in the village centre.")
    query = option(["Admire it", "Throw a ruby in for good luck", "Go back"])
    if query == "1":
        print2("You admire the fountain.")
        fountain()
    elif query == "2":
        print2("You throw a ruby in for good luck.")
        game_state.rubies = game_state.rubies - 1
        print2("Out of the fountain, a key rises to the surface of the water.")
        game_state.inventory.getKeyItem("Ancient Key")
        fountain()
    elif query == "3":
        town3()
    else:
        fountain()


def townEast():
    print2("There is a note on the floor.")
    query = option(["Read the note", "Return"])
    if query == "1":
        note()
    elif query == "2":
        town3()
    else:
        townEast()


def note():
    print2(
        "You read the note. It reads, 'None can stop me now. At 38, they will know. North, North, South, South, West, East, West, East.'"
    )
    query = option(["Read the note again", "Place it back down"])
    if query == "1":
        note()
    elif query == "2":
        townEast()
    else:
        note()


def townNorth():
    print2(
        "You enter an empty street of market stalls. A northern route leads to a smaller street."
    )
    query = option(["Go down the smaller street", "Go to the Village Centre."])
    if query == "1":
        door()
    elif query == "2":
        town3()
    else:
        townNorth()


def door():
    print(
        "You come to a dead-end on the street, where you see a mysterious door that doesn't seem to lead anywhere. Its lock seems rusted. There is a keyhole. What will you do?"
    )
    if "Ancient Key" in game_state.inventory.keyItems:
        query = option([
            "Attempt to turn the handle", "Go back",
            "Unlock the door with the Ancient Key"
        ])
    else:
        query = option(["Attempt to turn the handle", "Go back"])
    if query == "1":
        lock()
    elif query == "3":
        if "Ancient Key" in game_state.inventory.keyItems:
            unlock()
    elif query == "2":
        town3()
    else:
        door()


def lock():
    print2("You attempt to turn the handle, but it does not budge.")
    query = option(["Try Again", "Go Back"])
    if query == "1":
        lock()
    elif query == "2":
        door()
    else:
        lock()


def unlock():
    print2("You unlock the mysterious door with the Ancient Key.")
    query = option(["Continue"], Inventory=False)
    if query == "1":
        secret()
    else:
        print2("You cannot go back now.")
        secret()


def secret():
    print2("You go through the door. It is pitch-black.")
    query = option(["Continue"], Inventory=False)
    if query == "1":
        secret2()
    else:
        print2("You cannot go back now.")
        secret2()


def secret2():
    print2("As you continue, everything goes pitch-black.")
    query = option(["Continue"], Inventory=False)
    if query == "1":
        secret3()
    else:
        print2("You cannot go back now.")
        secret3()


def secret3():
    print2("As you continue, you see a light at the end.")
    query = option(["Continue"], Inventory=False)
    if query == "1":
        secret4()
    else:
        print2("You cannot go back now.")
        secret4()


def secret4():
    print2(
        "Eventually, you get to the end, and can go through the illuminated exit."
    )
    query = option(["Continue"], Inventory=False)
    if query == "1":
        secret5()
    else:
        print2("You cannot go back now.")
        secret5()


def secret5():
    print2(
        "It is the back room of " + game_state.shopkeeperName +
        "'s shop. It is full of rubies and products. There is a letter on a nearby desk."
    )
    query = option([
        "Take some rubies", "Take some lamp oil", "Take some rope",
        "Take some bombs", "Go through to the front", "Inspect the letter"
    ])
    if query == "1":
        print2("You take some rubies.")
        game_state.getRuby(9000)
        secret5()
    elif query == "2":
        print2("You take some lamp oil.")
        game_state.inventory.getItem("Lamp Oil")
        secret5()
    elif query == "3":
        print2("You take some rope.")
        game_state.inventory.getItem("Rope")
        secret5()
    elif query == "4":
        print2("You take some bombs.")
        game_state.inventory.getItem("Bomb")
        secret5()
    elif query == "5":
        secret6()
    elif query == "6":
        print2(
            "The envelope is sealed with a luxurious seal. The letter is addressed to 'The Overseer', and has the number 38 written on it. There is no letter inside the envelope."
        )
        secret5()
    else:
        print2("You cannot go back now.")
        secret5()


def secret6():
    print2("You are in the front room of " + game_state.shopkeeperName +
           "'s shop.")
    query = option(["Become " + game_state.shopkeeperName], Inventory=False)
    if query == "1":
        print2(
            "You become " + game_state.shopkeeperName +
            ". The people eventually return. You begin selling your wares again, and you finally understand the full circumstances of these events."
        )
        ending("Secret")
    else:
        print2("You cannot go back now.")
        secret6()


def townWest():
    print2(
        "There is a large square, with houses all around. There is an alley.")
    query = option(["Go down the alley", "Go to the Town Centre"])
    if query == "1":
        maze13()
    elif query == "2":
        town3()
    else:
        townWest()


def maze11():  # :(
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze21()
    elif query == "2":
        print2("Dead end.")
        maze11()
    elif query == "3":
        print2("Dead end.")
        maze11()
    elif query == "4":
        print2("Dead end.")
        maze11()
    else:
        maze11()


def maze12():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze22()
    elif query == "2":
        maze13()
    elif query == "3":
        print2("Dead end.")
        maze12()
    elif query == "4":
        print2("Dead end.")
        maze12()
    else:
        maze12()


def maze13():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze23()
    elif query == "2":
        maze14()
    elif query == "3":
        townWest()
    elif query == "4":
        maze12()
    else:
        maze13()


def maze14():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze24()
    elif query == "2":
        print2("Dead end.")
        maze14()
    elif query == "3":
        print2("Dead end.")
        maze14()
    elif query == "4":
        maze13()
    else:
        maze14()


def maze15():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze25()
    elif query == "2":
        print2("Dead end.")
        maze15()
    elif query == "3":
        print2("Dead end.")
        maze15()
    elif query == "4":
        print2("Dead end.")
        maze15()
    else:
        maze15()


def maze21():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze21()
    elif query == "2":
        maze22()
    elif query == "3":
        maze11()
    elif query == "4":
        print2("Dead end.")
        maze21()
    else:
        maze21()


def maze22():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze22()
    elif query == "2":
        maze23()
    elif query == "3":
        maze12()
    elif query == "4":
        maze21()
    else:
        maze22()


def maze23():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze23()
    elif query == "2":
        maze24()
    elif query == "3":
        maze13()
    elif query == "4":
        maze22()
    else:
        maze23()


def maze24():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze34()
    elif query == "2":
        print2("Dead end.")
        maze24()
    elif query == "3":
        maze14()
    elif query == "4":
        maze23()
    else:
        maze24()


def maze25():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze35()
    elif query == "2":
        print2("Dead end.")
        maze25()
    elif query == "3":
        maze15()
    elif query == "4":
        print2("Dead end.")
        maze25()
    else:
        maze25()


def maze31():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze41()
    elif query == "2":
        print2("Dead end.")
        maze31()
    elif query == "3":
        print2("Dead end.")
        maze31()
    elif query == "4":
        print2("Dead end.")
        maze31()
    else:
        maze31()


def maze32():
    if game_state.caveOpened:
        print2(
            "You are in a maze of twisty little alleys, all alike. There is a cave opening here. Something about this seems familiar."
        )
        query = option(
            ["Go north", "Go east", "Go south", "Go west", "Go into the cave"])
    else:
        print2(
            "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
        )
        query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze32()
    elif query == "2":
        maze33()
    elif query == "3":
        print2("Dead end.")
        maze32()
    elif query == "4":
        print2("Dead end.")
        maze32()
    elif query == "5" and game_state.caveOpened:
        cave9()
    else:
        maze32()


def maze33():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze43()
    elif query == "2":
        print2("Dead end.")
        maze33()
    elif query == "3":
        print2("Dead end.")
        maze33()
    elif query == "4":
        maze32()
    else:
        maze33()


def maze34():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze34()
    elif query == "2":
        maze35()
    elif query == "3":
        maze24()
    elif query == "4":
        print2("Dead end.")
        maze34()
    else:
        maze34()


def maze35():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze45()
    elif query == "2":
        print2("Dead end.")
        maze35()
    elif query == "3":
        maze25()
    elif query == "4":
        maze34()
    else:
        maze35()


def maze41():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze51()
    elif query == "2":
        maze42()
    elif query == "3":
        maze31()
    elif query == "4":
        print2("Dead end.")
        maze41()
    else:
        maze41()


def maze42():
    if "Amber Necklace" not in game_state.inventory.keyItems:
        print2("You see, on the ground, a beautiful necklace.")
        game_state.inventory.getKeyItem("Amber Necklace")
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze42()
    elif query == "2":
        print2("Dead end.")
        maze42()
    elif query == "3":
        print2("Dead end.")
        maze42()
    elif query == "4":
        maze41()
    else:
        maze42()


def maze43():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze53()
    elif query == "2":
        print2("Dead end.")
        maze43()
    elif query == "3":
        maze33()
    elif query == "4":
        print2("Dead end.")
        maze43()
    else:
        maze43()


def maze44():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze44()
    elif query == "2":
        maze45()
    elif query == "3":
        print2("Dead end.")
        maze44()
    elif query == "4":
        print2("Dead end.")
        maze44()
    else:
        maze44()


def maze45():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        maze55()
    elif query == "2":
        print2("Dead end.")
        maze45()
    elif query == "3":
        maze35()
    elif query == "4":
        print2("Dead end.")
        maze45()
    else:
        maze45()


def maze51():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze51()
    elif query == "2":
        maze52()
    elif query == "3":
        maze41()
    elif query == "4":
        print2("Dead end.")
        maze51()
    else:
        maze51()


def maze52():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze52()
    elif query == "2":
        maze53()
    elif query == "3":
        print2("Dead end.")
        maze52()
    elif query == "4":
        maze51()
    else:
        maze52()


def maze53():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze53()
    elif query == "2":
        maze54()
    elif query == "3":
        maze43()
    elif query == "4":
        maze52()
    else:
        maze53()


def maze54():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze54()
    elif query == "2":
        maze55()
    elif query == "3":
        print2("Dead end.")
        maze54()
    elif query == "4":
        maze53()
    else:
        maze54()


def maze55():
    print2(
        "You are in a maze of twisty little alleys, all alike. Something about this seems familiar."
    )
    query = option(["Go north", "Go east", "Go south", "Go west"])
    if query == "1":
        print2("Dead end.")
        maze55()
    elif query == "2":
        print2("Dead end.")
        maze55()
    elif query == "3":
        maze45()
    elif query == "4":
        maze53()
    else:
        maze55()


def shop():
    print2("\033[33m'" + random.choice(ShopkeeperQuotes) + "'\033[0m")
    print2("Current Rubies:" + str(game_state.rubies) +
           "\nLamp Oil - 15 Rubies\nRope - 20 Rubies\nBomb - 30 Rubies")
    query = option([
        "Purchase lamp oil", "Purchase rope", "Purchase bomb",
        "Ask about quest", "Leave"
    ])
    if query == "1":
        if game_state.rubies >= 15:
            game_state.rubies = game_state.rubies - 15
            game_state.inventory.getItem("Lamp Oil")
        else:
            print2(
                "\033[33m'Sorry, my friend. You don't have enough rubies. I'd love to give you the items for free but I have a mouth to feed.'\033[0m"
            )
        shop()
    elif query == "2":
        if game_state.rubies >= 20:
            game_state.rubies = game_state.rubies - 20
            game_state.inventory.getItem("Rope")
        else:
            print2(
                "\033[33m'Sorry, my friend. You don't have enough rubies. I'd love to give you the items for free but I have a mouth to feed.'\033[0m"
            )
        shop()
    elif query == "3":
        if game_state.rubies >= 30:
            game_state.rubies = game_state.rubies - 30
            game_state.inventory.getItem("Bomb")
        else:
            print2(
                "\033[33m'Sorry, my friend. You don't have enough rubies. I'd love to give you the items for free but I have a mouth to feed.'\033[0m"
            )
        shop()
    elif query == "4":
        cursedItems = len({"Rusted Sword", "Amber Necklace", "Golden Idol"}
                          & set(game_state.inventory.keyItems))
        if cursedItems == 3:
            print2(
                "\033[33m'Well, I'll be. That's all of them. Honestly, I kind of doubted you could do it - now I see that my doubt was misplaced! You will go down in legend for your heroism!'"
            )
            time.sleep(0.75)
            print2("\033[33m'Oh, and just one more thing: thank you.'\033[0m")
            time.sleep(1.5)
            ending("Good")
        elif cursedItems > 0:
            print2(
                f"\033[33m'Great! You managed to get {cursedItems} of the items - now we just need {3 - cursedItems} more!'\033[0m"
            )
        print2(
            "\033[33m'Sorry, I can't help you much. I do know, however, that one of the items is somewhere in the town and another is in the nearby forest. That's all I know.'\033[0m"
        )
        shop()
    elif query == "5":
        print2("\033[33m'" + random.choice(ShopkeeperQuotesExit) + "'\033[0m")
        field()
    else:
        shop()


def bazaar():
    print2(
        "You are in the bazaar. There is not many attended stalls around. There appears to be a fisherman at a stall, a fletcher, and a mineral collector."
    )
    query = option([
        "Go to the fisherman", "Go to the fletcher",
        "Go to the mineral collector", "Go to the field"
    ])
    if query == "1":
        fishermanStall()
    elif query == "2":
        if game_state.fletcherOpen:
            fletcherStall()
        else:
            print2("The stall in no longer open.")
            bazaar()
    elif query == "3":
        mineralStall()
    elif query == "4":
        field()
    else:
        bazaar()


def fishermanStall():
    print2(
        "Current Rubies:" + str(game_state.rubies) +
        "\nFillet of Cod - 2 rubies\nFillet of Salmon - 2 rubies\nSmoked Trout - 9 rubies\nJar of Tuna - 3 rubies\nFillet of Smoked Haddock - 6 rubies"
    )
    print2("\033[36m'What are you here to buy?'\033[0m")
    query = option([
        "Purchase a fillet of cod", "Purchase a fillet of salmon",
        "Purchase smoked trout", "Purchase a jar of tuna",
        "Purchase a fillet of smoked haddock", "Talk", "Leave"
    ])
    if query == "1":
        if game_state.rubies >= 2:
            game_state.rubies = game_state.rubies - 2
            game_state.inventory.getItem("Fillet of Cod")
            fishermanStall()
        else:
            print2(
                "\033[36m'If you aren't here to buy anything, then get out.'\033[0m"
            )
            bazaar()
    elif query == "2":
        if game_state.rubies >= 2:
            game_state.rubies = game_state.rubies - 2
            game_state.inventory.getItem("Fillet of Salmon")
            fishermanStall()
        else:
            print2(
                "\033[36m'If you aren't here to buy anything, then get out.'\033[0m"
            )
            bazaar()
    elif query == "3":
        if game_state.rubies >= 9:
            game_state.rubies = game_state.rubies - 9
            game_state.inventory.getItem("Smoked Trout")
            fishermanStall()
        else:
            print2(
                "\033[36m'If you aren't here to buy anything, then get out.'\033[0m"
            )
            bazaar()
    elif query == "4":
        if game_state.rubies >= 3:
            game_state.rubies = game_state.rubies - 3
            game_state.inventory.getItem("Jar of Tuna")
            fishermanStall()
        else:
            print2(
                "\033[36m'If you aren't here to buy anything, then get out.'\033[0m"
            )
            bazaar()
    elif query == "5":
        if game_state.rubies >= 6:
            game_state.rubies = game_state.rubies - 6
            game_state.inventory.getItem("Fillet of Smoked Haddock")
            fishermanStall()
        else:
            print2(
                "\033[36m'If you aren't here to buy anything, then get out.'\033[0m"
            )
            bazaar()
    elif query == "6":
        fishBought = len({
            "Fillet of Cod", "Fillet of Salmon", "Smoked Trout", "Jar of Tuna",
            "Fillet of Smoked Haddock"
        }) & set(game_state.inventory.keyItems)
        if fishBought >= 1 and "Fishing Rod" not in game_state.inventory.keyItems:
            print2(
                "\033[36m'You know, I recently got a new fishing rod. Say, you can have my old one, since you bought something.'\033[0m"
            )
            game_state.inventory.getKeyItem("Fishing Rod")
        else:
            print2(
                "\033[36m'You know, I'd be more in the mood to talk if you bought something.'\033[0m"
            )
        fishermanStall()
    elif query == "7":
        bazaar()
    else:
        fishermanStall()


def fletcherStall():
    print2("Current Rubies:" + str(game_state.rubies))
    print2(
        "\033[35m'Hey. I've got one bow in stock right now. I'm sure you heard what happened. I hope everyone will return.'\033[0m"
    )
    query = option(["Purchase the bow", "Talk", "Leave"])
    if query == "1":
        if game_state.rubies >= 75:
            game_state.rubies = game_state.rubies - 75
            game_state.inventory.getKeyItem("Bow and Arrow")
            game_state.fletcherOpen = False
            bazaar()
        else:
            print2(
                "\033[35m'Sorry, that's not really enough. I'd let it go for 75 rubies, maybe.'\033[0m"
            )
            fletcherStall()
    elif query == "2":
        if "Silver Amulet" in game_state.inventory.keyItems:
            print2(
                "\033[35m'You did it! I can't believe it! That's really it! That's my mother's \033[47mSilver Amulet\033[0m\033[35m! I can't thank you enough! Here, have this bow, no charge! Thank you, thank you!"
            )
            game_state.inventory.keyItems.remove("Silver Amulet")
            game_state.inventory.getKeyItem("Bow and Arrow")
            game_state.fletcherOpen = False
            bazaar()
        else:
            print2(
                "\033[35m'Hey, do you think you could do something for me? Since everyone disappeared last night, I miss my mother. Do you think you could see if you could find her \033[47mSilver Amulet\033[0m\033[35m? I'd give you the bow for free if you did.'\033[0m"
            )
            fletcherStall()
    elif query == "3":
        bazaar()
    else:
        fletcherStall()


def mineralStall():
    print2(
        "\033[32m'Hello, I collect minerals. If you find any minerals, give them to me.'\033[0m"
    )
    query = option(["Sell minerals", "Leave"])
    if query == "1":
        rocksYouHave = set(mysticalRocks) & set(game_state.inventory.items)
        if rocksYouHave == 0:
            print2(
                "\033[32m'I'm sorry, but you don't appear to have any minerals. Good day.'\033[0m"
            )
        else:
            for item in [
                    item for item in list(game_state.inventory.items)
                    if item in list(mysticalRocks)
            ]:  #This is not that readable but it does stuff basically]
                value = mysticalRocks[item]
                game_state.getRuby(value)
                game_state.inventory.items.remove(item)
            print2(
                "\033[32m'Thank you so much. These will be excellent to add to my collection.'\033[0m"
            )
        bazaar()
    elif query == "2":
        bazaar()
    else:
        mineralStall()


def cave(
):  #This is the worst and most fustrating part of the game. Have fun :)
    print2("You are at the cave's entrance.")
    query = option(["Enter the cave", "Go back to the open field"])
    if query == "1":
        cave1()
    elif query == "2":
        field()
    else:
        cave()


def cave1():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and south."
    )
    query = option(["Go north", "Go south"])
    if query == "1":
        cave2()
    elif query == "2":
        cave()
    else:
        cave1()


def cave2():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north, south and west."
    )
    query = option(["Go north", "Go south", "Go west"])
    if query == "1":
        cave3()
    elif query == "2":
        cave1()
    elif query == "3":
        cave7()
    else:
        cave2()


def cave3():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and south."
    )
    query = option(["Go north", "Go south"])
    if query == "1":
        cave4()
    elif query == "2":
        cave2()
    else:
        cave3()


def cave4():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and south."
    )
    query = option(["Go east", "Go south"])
    if query == "1":
        cave5()
    elif query == "2":
        cave3()
    else:
        cave4()


def cave5():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north, south and west."
    )
    query = option(["Go north", "Go south", "Go west"])
    if query == "1":
        cave6()
    elif query == "2":
        cave11()
    elif query == "3":
        cave4()
    else:
        cave5()


def cave6():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your south and west."
    )
    query = option(["Go south", "Go west"])
    if query == "1":
        cave5()
    elif query == "2":
        cave10()
    else:
        cave6()


def cave7():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and east."
    )
    query = option(["Go north", "Go east"])
    if query == "1":
        cave8()
    elif query == "2":
        cave2()
    else:
        cave7()


def cave8():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and south."
    )
    query = option(["Go north", "Go south"])
    if query == "1":
        cave9()
    elif query == "2":
        cave7()
    else:
        cave8()


def cave9():
    caveItem()
    if game_state.caveOpened:
        print2(
            "You are within the cave. It is difficult to see. There is a path to your northeast, south and northwest."
        )
    else:
        print2(
            "You are within the cave. It is difficult to see. There is a path to your northeast and south. There is a lot of rubble to your northwest."
        )
    if game_state.caveOpened:
        query = option(["Go northeast", "Go south", "Go northwest"])
    elif "Bomb" in game_state.inventory.items:
        query = option(
            ["Go northeast", "Go south", "Destroy the rubble with a bomb"])
    else:
        query = option(["Go northeast", "Go south"])
    if query == "1":
        cave10()
    elif query == "2":
        cave8()
    elif query == "3":
        if game_state.caveOpened:
            maze32()
        elif "Bomb" in game_state.inventory.items:
            print2(
                "You blow up the rubble. Light shines through, and a path to the surface appears."
            )
            game_state.caveOpened = True
            game_state.inventory.items
            cave9()
        else:
            print(343)
            cave9()
    else:
        cave9()


def cave10():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north, east and southwest."
    )
    query = option(["Go north", "Go south", "Go southwest"])
    if query == "1":
        cave39()
    elif query == "2":
        cave6()
    elif query == "3":
        cave9()
    else:
        cave10()


def cave11():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north, northeast and south."
    )
    query = option(["Go north", "Go northeast", "Go south"])
    if query == "1":
        cave5()
    elif query == "2":
        cave19()
    elif query == "3":
        cave12()
    else:
        cave11()


def cave12():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north, northeast, southeast and south."
    )
    query = option(["Go north", "Go northeast", "Go southeast", "Go south"])
    if query == "1":
        cave11()
    elif query == "2":
        cave14()
    elif query == "3":
        cave13()
    elif query == "4":
        cave26()
    else:
        cave12()


def cave13():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and west."
    )
    query = option(["Go east", "Go west"])
    if query == "1":
        cave15()
    elif query == "2":
        cave12()
    else:
        cave13()


def cave14():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and west."
    )
    query = option(["Go east", "Go west"])
    if query == "1":
        cave17()
    elif query == "2":
        cave12()
    else:
        cave14()


def cave15():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and west."
    )
    query = option(["Go east", "Go west"])
    if query == "1":
        cave16()
    elif query == "2":
        cave13()
    else:
        cave15()


def cave16():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and west."
    )
    query = option(["Go north", "Go west"])
    if query == "1":
        cave18()
    elif query == "2":
        cave15()
    else:
        cave16()


def cave17():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and west."
    )
    query = option(["Go east", "Go west"])
    if query == "1":
        cave18()
    elif query == "2":
        cave14()
    else:
        cave17()


def cave18():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your south and west."
    )
    query = option(["Go south", "Go west"])
    if query == "1":
        cave16()
    elif query == "2":
        cave17()
    else:
        cave18()


def cave19():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north, southeast and southwest."
    )
    query = option(["Go north", "Go southeast", "Go southwest"])
    if query == "1":
        cave20()
    elif query == "2":
        cave24()
    elif query == "3":
        cave11()
    else:
        cave19()


def cave20():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your northeast and south."
    )
    query = option(["Go northeast", "Go south"])
    if query == "1":
        cave21()
    elif query == "2":
        cave19()
    else:
        cave20()


def cave21():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your southeast and southwest."
    )
    query = option(["Go southeast", "Go southwest"])
    if query == "1":
        cave22()
    elif query == "2":
        cave20()
    else:
        cave21()


def cave22():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your northwest and south."
    )
    query = option(["Go northwest", "Go south"])
    if query == "1":
        cave21()
    elif query == "2":
        cave23()
    else:
        cave22()


def cave23():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and southwest."
    )
    query = option(["Go north", "Go southwest"])
    if query == "1":
        cave22()
    elif query == "2":
        cave24()
    else:
        cave23()


def cave24():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your northeast and northwest."
    )
    query = option(["Go northeast", "Go northwest"])
    if query == "1":
        cave23()
    elif query == "2":
        cave19()
    else:
        cave24()


def cave26():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and south."
    )
    query = option(["Go north", "Go south"])
    if query == "1":
        cave12()
    elif query == "2":
        cave27()
    else:
        cave26()


def cave27():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north, east and southeast."
    )
    query = option(["Go north", "Go east", "Go southeast"])
    if query == "1":
        cave26()
    elif query == "2":
        cave28()
    elif query == "3":
        cave31()
    else:
        cave27()


def cave28():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and west."
    )
    query = option(["Go east", "Go west"])
    if query == "1":
        cave29()
    elif query == "2":
        cave27()
    else:
        cave28()


def cave29():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and west."
    )
    query = option(["Go east", "Go west"])
    if query == "1":
        if "Golden Idol" not in game_state.inventory.keyItems:
            print2("You see a Golden Idol on the floor of the cave.")
            game_state.inventory.getKeyItem("Golden Idol")
        cave30()
    elif query == "2":
        cave28()
    else:
        cave29()


def cave30():
    caveItem()
    print2(
        "You are within the cave. It is a dead-end. The only path is back where you came."
    )
    query = option(["Go back"])
    if query == "1":
        cave29()
    else:
        cave30()


def cave31():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your northwest and east."
    )
    query = option(["Go northwest", "Go east"])
    if query == "1":
        cave27()
    elif query == "2":
        cave32()
    else:
        cave31()


def cave32():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and west."
    )
    query = option(["Go east", "Go west"])
    if query == "1":
        cave33()
    elif query == "2":
        cave31()
    else:
        cave32()


def cave33():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and west."
    )
    query = option(["Go east", "Go west"])
    if query == "1":
        cave34()
    elif query == "2":
        cave32()
    else:
        cave33()


def cave34():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and west."
    )
    query = option(["Go north", "Go west"])
    if query == "1":
        cave35()
    elif query == "2":
        cave33()
    else:
        cave34()


def cave35():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and south."
    )
    query = option(["Go north", "Go south"])
    if query == "1":
        cave36()
    elif query == "2":
        cave34()
    else:
        cave35()


def cave36():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your north and south."
    )
    query = option(["Go north", "Go south"])
    if query == "1":
        cave37()
    elif query == "2":
        cave35()
    else:
        cave36()


def cave37():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your south and west. There is also a small pond."
    )
    if "Fishing Rod" in game_state.inventory.keyItems:
        query = option(["Go south", "Go west", "Fish in the pond"])
    else:
        query = option(["Go south", "Go west"])
    if query == "1":
        cave36()
    elif query == "2":
        cave38()
    elif query == "3":
        if "Fishing Rod" in game_state.inventory.keyItems and not "Silver Amulet" not in game_state.inventory.keyItems and game_state.fletcherOpen:
            print2("You fish in the fishing pond and find a silver amulet.")
            game_state.inventory.getKeyItem("Silver Amulet")
        elif "Fishing Rod" in game_state.inventory.keyItems:
            print2("You fish in the fishing pond but you find nothing.")
        else:
            cave37()
    else:
        cave37()


def cave38():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and west."
    )
    query = option(["Go east", "Go west"])
    if query == "1":
        cave37()
    elif query == "2":
        cave39()
    else:
        cave38()


def cave39():
    caveItem()
    print2(
        "You are within the cave. It is difficult to see. There is a path to your east and south."
    )
    query = option(["Go east", "Go south"])
    if query == "1":
        cave38()
    elif query == "2":
        cave10()
    else:
        cave38()


def action1():
    print2("")
    query = option(["", ""])
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


##


def debug():
    query = option([
        "ShopkeeperQuote", "ShopkeeperQuoteExit", "Rusted Sword",
        "Win the game", "Secret ending", "Get all items", "Debug ending code",
        "SHM Ending", "Warp to pond", "Warp to Golden Idol", "Warp to rubble",
        "Warp to end of maze", "Warp to starting area", "Give over 9000 rubies"
    ])
    if query == "1": print(random.choice(ShopkeeperQuotes))
    elif query == "2": print(random.choice(ShopkeeperQuotesExit))
    elif query == "3": game_state.inventory.getKeyItem("Rusted Sword")
    elif query == "4": ending("Good")
    elif query == "5": ending("Secret")
    elif query == "6":
        game_state.inventory.getKeyItem("Rusted Sword")
        game_state.inventory.getKeyItem("Amber Necklace")
        game_state.inventory.getKeyItem("Golden Idol")
        game_state.inventory.getKeyItem("Ancient Key")
        game_state.inventory.getKeyItem("Fishing Rod")
        game_state.inventory.getKeyItem("Bow and Arrow")
        game_state.inventory.getKeyItem("Silver Amulet")
        game_state.inventory.getItem("Lamp Oil")  #Forest
        game_state.inventory.getItem("Lamp Oil")  #Cave
        game_state.inventory.getItem("Rope")  #Cave
        game_state.inventory.getItem("Bomb")  #Cave
        game_state.inventory.getItem("Bomb")  #Cave
        game_state.getRuby(9001)
        for i in list(mysticalRocks):
            game_state.inventory.getItem(i)
    elif query == "7":
        print("Good")
        if "Good" in endingsWithCustomText:
            print("Good is in there")
        else:
            print("Not this time")
        index = endingsWithCustomText.index("Good")
        print(index)
        print2(endingCustomText[index], pauseAtNewline=0.65)
        print(defaultEndingText)
    elif query == "8":
        ending("SHM")
    elif query == "9":
        game_state.inventory.getKeyItem("Fishing Rod")
        cave37()
    elif query == "10":
        cave29()
    elif query == "11":
        cave9()
    elif query == "12":
        maze41()
    elif query == "13":
        field()
    elif query == "14":
        game_state.getRuby(9001)


##

while True:
    intro()
exit

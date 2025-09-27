import time
from dataclasses import dataclass
import random
import sys

complevel = 0
history = []

ShopkeeperQuotesExit = [
    "Remember, tomorrow is another day.",
    "Be seeing you.",
    "I wish you the best of luck.",
    "I give you my grace.",
    "I wish you luck on your quest.",
    "I'll get started on my tea.",
    "May all the spirits be with you.",
]

ShopkeeperQuotes = [
    "Welcome!",
    "Sit down, my friend. Stay a while.",
    "You'll always be welcome here in my shop.",
    "Have a look at my wares. They could prove to be useful.",
    "Sorry I can't give discounts - I have a business to run, and I must make my money somehow.",
    "I don't blame you for coming inside in this winter.",
    "Sit down a while. I don't want you too stressed, my friend.",
    "I always believe that everyone has a tale worth telling - maybe talk to more people.",
    "Have you checked out the bazaar? There's a fisherman there who sells excellent-quality rods.",
    "Have you heard the news about the King? It's said that he's fallen ill. He's a good man - I hope he fully recovers.",
    "Have you seen the nearby forest? There's been some monkey sightings there.",
]

endingText = {
    "Good": "And so, overnight, all the people returned to the village, as if they had never left.\nSoon after, the village was lifted into high spirits as the harvest had been the best in almost thirty years.\nDespite the prospering village, you decided to leave.\nYou had no desire to stay after the events you just experienced, and you would rather leave than stay to make some money.",
    "Secret": "And so, overnight, you became the new shopkeeper, but nothing really changed in the end.\nThe villagers never returned, but many travellers came, hearing about what happened.\nMany decided te stay after a plentiful harvest brought good omens to the village.\nThis, however, would not be the last of it...\n...and you knew that.",
    "SHM": "You achieved the\n|\nEnding.\nTry Again?",
}
defaultEnding = "\033[1mThe Shopkeeper's Quest\033[0m\n\nSchool Project Edition\n\nWith inspiration from:\nColossal Cave Adventure, by Will Crowther and Don Woods;\nKing's Quest, by Sierra On-Line;\nHenry Stickmin, by Puffballs United;\nMinecraft: Story Mode, by Telltale Games;\n and RTX Morshu: The Game, by koshkamatew\nWith special thanks to\n\033[1m\033[33mYOU\033[0m\nfor playing the game,\nfor if a tree falls and no one hears it, does it make a noise?"

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

keyItems = [
    "Rusted Sword",
    "Amber Necklace",
    "Golden Idol",
    "Silver Amulet",
    "Bow and Arrow",
    "Fishing Rod",
]


def print2(text, newline=True, pauseAtNewline=0.0, endingChar=False):
    for char in text:
        if char == "\n":
            time.sleep(pauseAtNewline)
        print(char, end="", flush=True)
        time.sleep(0.01)
    if newline:
        print()


def lose(text):
    print("\n\n")
    time.sleep(0.25)
    print("\033[31m\033[1mYou died!\033[0m")
    print("'" + text + "'")
    time.sleep(0.5)
    print("\n\n\nTry again?")


def ending(end):
    print2(endingText[end].replace("|", end), pauseAtNewline=0.65)
    print("\n\n")
    print2(defaultEnding.replace("|", end), pauseAtNewline=0.65)
    time.sleep(2.5)


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
        print2("\nYou got \033[1m\033[47m" + str(item) + "\033[0m!")
        self.keyItems.append(item)

    def __str__(self):
        if not self.items and not self.keyItems:
            return "Your inventory is empty"
        output = []
        if self.items:
            output.append("Items:\n" + "\n".join(f"- {item}" for item in self.items))
        if self.keyItems:
            output.append(
                "Key Items:\n" + "\n".join(f"- {item}" for item in self.keyItems)
            )
        return "\n".join(output)


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
        print2(
            "\033[0m You currently have \033[1m"
            + str(self.rubies)
            + "\033[0m Rubies.\n"
        )


game_state = gameState(inventory=Inventory(items=[]))


def itemEvaluation():
    cursedItems = len(
        {"Rusted Sword", "Amber Necklace", "Golden Idol"}
        & set(game_state.inventory.keyItems)
    )
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


def fishEvaluation():
    fishBought = len(
        {
            "Fillet of Cod",
            "Fillet of Salmon",
            "Smoked Trout",
            "Jar of Tuna",
            "Fillet of Smoked Haddock",
        }
        & set(game_state.inventory.keyItems)
    )
    if fishBought >= 1 and "Fishing Rod" not in game_state.inventory.keyItems:
        print2(
            "\033[36m'You know, I recently got a new fishing rod. Say, you can have my old one, since you bought something.'\033[0m"
        )
        game_state.inventory.getKeyItem("Fishing Rod")
    else:
        print2(
            "\033[36m'You know, I'd be more in the mood to talk if you bought something.'\033[0m"
        )


def mineralEvaluation():
    for item in [
        item for item in list(game_state.inventory.items) if item in list(mysticalRocks)
    ]:  # This is not that readable but it does stuff basically]
        value = mysticalRocks[item]
        game_state.getRuby(value)
        game_state.inventory.items.remove(item)
    print2(
        "\033[32m'Thank you so much. These will be excellent to add to my collection.'\033[0m"
    )


rooms = {
    0: {
        "Text": "\033[32m[Debug] This is the Debug Room.\033[0m",
        "Options": ["Go to 2", "Go to 3"],
        "Move": [2, 3],
    },
    1: {
        "Text": "You are standing at the outskirts of the village. There is a road to the north, leading to the main parts of the village, a forest to the east, a cave to the south, a shop and bazaar to the west.",
        "Options": [
            "Go to the forest",
            "Follow the road to the village",
            "Explore the cave",
            "Go to " + game_state.shopkeeperName + "'s shop",
            "Go to the bazaar",
        ],
        "Move": [3, 9, 88, 66, 73],
    },
    2: {
        "Text": "You are standing at the outskirts of the village.",
        "Options": [
            "Go to the forest",
            "Follow the road to the village",
            "Explore the cave",
            "Go to " + game_state.shopkeeperName + "'s shop",
            "Go to the bazaar",
        ],
        "Move": [3, 9, 88, 66, 73],
    },
    3: {
        "Text": "You come to the opening of the forest. The forest is vast and the trees tower over you.",
        "Options": ["Go further in", "Leave"],
        "Move": [4, 2],
    },
    4: {
        "Text": "You are deep in the forest. It is dim, and difficult to see.",
        "Options": ["Go further in", "Leave"],
        "Option0Requirements": lambda: "Rusted Sword" not in game_state.inventory.keyItems,
        "Move": [5, 3],
    },
    5: {
        "Text": "You come to a clearing, deep in the forest. There is a bonobo sitting, facing you.",
        "Options": ["Fight the bonobo", "Fight the bonobo", "Leave"],
        "Option0Requirements": lambda: "Bow and Arrow"
        not in game_state.inventory.keyItems,
        "Option1Requirements": lambda: "Bow and Arrow" in game_state.inventory.keyItems,
        "Move": [6, 7, 8],
    },
    6: {
        "Text": "You attempt to fight the bonobo, but it easily overpowers you. You are killed.",
        "Script": lambda: lose("What did you think was going to happen?"),
        "Automove": 1,
    },
    7: {
        "Text": "You manage to defeat the bonobo, using your weapon.\nYou manage to find a chest, containing the \033[47mRusted Sword\033[0m.",
        "Script": lambda: game_state.inventory.getKeyItem("Rusted Sword"),
        "Options": ["Fight the bonobo", "Fight the bonobo", "Leave"],
        "Automove": 4,
    },
    8: {
        "Text": "You attempt to leave, but the bonobo catches you. You are killed.",
        "Script": lambda: lose("Bonobos are quite agressive."),
        "Options": ["Fight the bonobo", "Fight the bonobo", "Leave"],
        "Automove": 1,
    },
    9: {
        "Text": "You are standing within the village. It seems barren and no one is there.",
        "Options": [
            "Follow the High Steet",
            "Sit on a bench for a while",
            "Return to the outskirts of the village",
        ],
        "Move": [11, 10, 2],
    },
    10: {
        "Text": "You sit on a bench for a while.",
        "Automove": 9,
    },
    11: {
        "Text": "You are in the high steet of the village. The village centre is to your north, and the way back to the village outskirts is to your south.",
        "Options": ["Go towards the high street", "Go towards the village outskirts"],
        "Move": [12, 9],
    },
    12: {
        "Text": "You are in the centre of the village. There are paths each direction, with a fountain in the middle.",
        "Options": ["Go North", "Go East", "Go South", "Go West", "Go to the Fountain"],
        "Move": [18, 16, 11, 39, 13],
    },
    13: {
        "Text": "You are at the fountain in the village centre.",
        "Options": ["Admire it", "Throw a ruby in for good luck", "Go back"],
        "Option1Requirements": lambda: game_state.rubies > 0,
        "Move": [14, 15, 12],
    },
    14: {
        "Text": "You admire the fountain.",
        "Item": "Ancient Key",
        "ItemRequirements": lambda: history == [18, 19, 18, 12, 39, 12, 39, 12, 13, 14],
        "ItemText": "Out of the fountain, a \033[47mkey\033[0m rises to the surface of the water.",
        "Automove": 13,
    },
    15: {  # uuddlrlr
        "Text": "You throw a ruby into the fountain for good luck.",
        "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 1),
        "Item": "Ancient Key",
        "ItemRequirements": lambda: history == [18, 19, 18, 12, 39, 12, 39, 12, 13, 15],
        "ItemText": "Out of the fountain, a \033[47mkey\033[0m rises to the surface of the water.",
        "Automove": 13,
    },
    16: {
        "Text": "There is a note on the floor.",
        "Options": ["Read the note", "Return"],
        "Move": [17, 12],
    },
    17: {
        "Text": "You read the note. It reads, 'None can stop me now. At 38, they will know. North, North, South, South, West, East, West, East.'",
        "Options": ["Read the note again", "Place it back down"],
        "Move": [17, 16],
    },
    18: {
        "Text": "You find yourself amongst an empty street of market stalls. A northern route leads to a smaller street.",
        "Options": ["Go down the smaller street", "Go to the Village Centre."],
        "Move": [19, 12],
    },
    19: {
        "Text": "You come to a dead-end on the street, where you see a mysterious door that doesn't seem to lead anywhere. Its lock seems rusted. There is a keyhole. What will you do?",
        "Options": [
            "Unlock the door with the \033[47mAncient Key\033[0m",
            "Attempt to turn the handle",
            "Go back",
        ],
        "Option0Requirements": lambda: "Ancient Key" in game_state.inventory.keyItems,
        "Move": [21, 20, 18],
    },
    20: {
        "Text": "You attempt to turn the handle, but it does not budge.",
        "Options": ["Try Again", "Go Back"],
        "Move": [20, 19],
    },
    21: {
        "Text": "You cannot go back now.",
        "Requirements": lambda: 21 in history,
        "AlternateText": "You unlock the mysterious door with the \033[47mAncient Key\033[0m.",
        "Options": ["Continue"],
        "Inventory": False,
        "Move": 22,
    },
    22: {
        "Text": "You cannot go back now.",
        "Requirements": lambda: 22 in history,
        "AlternateText": "You go through the door. It is pitch-black. You feel that you can no longer control yourself.",
        "Options": ["Continue"],
        "Inventory": False,
        "Move": 23,
    },
    23: {
        "Text": "You cannot go back now.",
        "Requirements": lambda: 23 in history,
        "AlternateText": "As you continue, the tunnel around you appears to be darker than what you thought possible.",
        "Options": ["Continue"],
        "Inventory": False,
        "Move": 24,
    },
    24: {
        "Text": "You cannot go back now.",
        "Requirements": lambda: 24 in history,
        "AlternateText": "As you continue, you see a light at the end.",
        "Options": ["Continue"],
        "Inventory": False,
        "Move": 22,
    },
    25: {
        "Text": "You cannot go back now.",
        "Requirements": lambda: 25 in history,
        "AlternateText": "Eventually, you get to the end, and can go through the illuminated exit.",
        "Options": ["Continue"],
        "Inventory": False,
        "Move": 26,
    },
    26: {
        "Text": "It is the back room of "
        + game_state.shopkeeperName
        + "'s shop. It is full of rubies and products. There is a letter on a nearby desk.",
        "Options": [
            "Take some rubies",
            "Take some lamp oil",
            "Take some rope",
            "Take some bombs",
            "Go through to the front",
            "Inspect the letter",
        ],
        "Inventory": False,
        "Move": [27, 28, 29, 30, 32, 31],
    },
    27: {
        "Text": "You take some rubies.",
        "Script": lambda: game_state.getRuby(9000),
        "Automove": 26,
    },
    28: {
        "Text": "You take some lamp oil.",
        "Item": "Lamp Oil",
        "Automove": 26,
    },
    29: {
        "Text": "You take some rope.",
        "Item": "Rope",
        "Automove": 26,
    },
    30: {
        "Text": "You take some bombs.",
        "Item": "Bomb",
        "Automove": 26,
    },
    31: {
        "Text": "The envelope is sealed with a luxurious seal. The letter is addressed to 'The Overseer', and has the number 38 written on it. There is no letter inside the envelope.",
        "Automove": 26,
    },
    32: {
        "Text": "You cannot go back now.",
        "Requirements": lambda: 32 in history,
        "AlternateText": "You are in the front room of "
        + game_state.shopkeeperName
        + "'s shop.",
        "Options": ["Become " + game_state.shopkeeperName],
        "Inventory": False,
        "Move": [33],
    },
    33: {
        "Text": "You cannot go back now.",
        "Requirements": lambda: 33 in history,
        "AlternateText": "You become " + game_state.shopkeeperName + ".",
        "Script": lambda: ending("Secret"),
        "Inventory": False,
        "Automove": 38,
    },
    34: {
        "Text": "Dead end.",
        "Automove": (history, -2),
    },
    35: {
        "Text": "Dead end.",
        "Automove": (history, -2),
    },
    38: {
        "Text": "You cannot go back now.",
        "Script": lambda: sys.exit(),
        "Options": ["You cannot."],
        "Inventory": False,
        "Automove": 38,
    },
    39: {
        "Text": "There is a large square, with houses all around. There is an alley.",
        "Options": ["Go down the alley", "Go to the Town Centre"],
        "Move": [43, 12],
    },
    40: {
        "Text": "Dead end.",
        "Automove": (history, -2),
    },
    41: {  # :(
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [46, 40, 34, 35],
    },
    42: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [47, 43, 34, 35],
    },
    43: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [48, 44, 39, 42],
    },
    44: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [49, 40, 35, 43],
    },
    45: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [50, 40, 34, 35],
    },
    46: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 47, 41, 35],
    },
    47: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 48, 42, 46],
    },
    48: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 49, 43, 47],
    },
    49: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [54, 40, 44, 48],
    },
    50: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [55, 40, 45, 35],
    },
    51: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [56, 40, 35, 36],
    },
    52: {
        "Text": "You are in a maze of twisty little alleys, all alike. There is a cave opening here. Something about this seems familiar.",
        "Requirements": lambda: game_state.caveOpened,
        "AlternateText": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west", "Go into the cave"],
        "Option4Requirements": lambda: game_state.caveOpened,
        "Move": [40, 53, 35, 36, 99],
    },
    53: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [58, 40, 35, 52],
    },
    54: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 55, 49, 35],
    },
    55: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [60, 40, 50, 54],
    },
    56: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [61, 57, 51, 40],
    },
    57: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Item": "Golden Idol",
        "ItemRequirements": lambda: "Golden Idol" not in game_state.inventory.keyItems,
        "ItemText": "You see, on the ground, a beautiful \033[47mAmber Necklace\033[0m.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 35, 36, 56],
    },
    58: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [63, 40, 53, 35],
    },
    59: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 60, 35, 36],
    },
    60: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [65, 40, 55, 35],
    },
    61: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 62, 56, 35],
    },
    62: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 63, 35, 61],
    },
    63: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 64, 58, 62],
    },
    64: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 65, 35, 63],
    },
    65: {
        "Text": "You are in a maze of twisty little alleys, all alike. Something about this seems familiar.",
        "Options": ["Go north", "Go east", "Go south", "Go west"],
        "Move": [40, 35, 60, 63],
    },
    66: {
        "Text": "",
        "Script": lambda: print2(
            "\033[33m'"
            + random.choice(ShopkeeperQuotes)
            + "'\033[0m\nCurrent Rubies:"
            + str(game_state.rubies)
            + "\nLamp Oil - 15 Rubies\nRope - 20 Rubies\nBomb - 30 Rubies"
        ),
        "Options": [
            "Purchase Lamp Oil",
            "Purchase Rope",
            "Purchase Bomb",
            "Haggle",
            "Ask about quest",
            "Leave",
        ],
        "Option0Requirements": lambda: game_state.rubies >= 15,
        "Option1Requirements": lambda: game_state.rubies >= 20,
        "Option2Requirements": lambda: game_state.rubies >= 30,
        "Option3Requirements": lambda: game_state.rubies < 30,
        "Move": [67, 68, 69, 72, 70, 71],
    },
    67: {
        "Text": "You purchased some Lamp Oil. [15 Rubies]",
        "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 15),
        "Item": "Lamp Oil",
        "Automove": 66,
    },
    68: {
        "Text": "You purchased some Rope. [20 Rubies]",
        "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 20),
        "Item": "Rope",
        "Automove": 66,
    },
    69: {
        "Text": "You purchased a Bomb. [30 Rubies]",
        "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 30),
        "Item": "Bomb",
        "Automove": 66,
    },
    70: {
        "Text": "",
        "Script": lambda: itemEvaluation(),
        "Automove": 66,
    },
    71: {
        "Text": "\033[33m'" + random.choice(ShopkeeperQuotesExit) + "'\033[0m",
        "Automove": 2,
    },
    72: {
        "Text": "\033[33m'Sorry, my friend. You don't have enough rubies. I'd love to give you the items for free but I have a mouth to feed.'\033[0m",
        "Automove": 66,
    },
    73: {
        "Text": "You are in the bazaar. There are not many attended stalls around. There appears to be a fisherman, a fletcher, and a mineral collector, at three seperate stalls.",
        "TextRequirements": lambda: game_state.fletcherOpen,
        "AlternateText": "You are in the bazaar. There are not many attended stalls around. There appears to be a fisherman and a mineral collector at two seperate stalls.",
        "Options": [
            "Go to the fisherman",
            "Go to the fletcher",
            "Go to the mineral collector",
            "Go back to the village outskirts",
        ],
        "Option1Requirements": lambda: "Bow and Arrow"
        not in game_state.inventory.keyItems,
        "Move": [74, 82, 85, 2],
    },
    74: {
        "Text": "",
        "Script": lambda: print2(
            "Current Rubies:"
            + str(game_state.rubies)
            + "\nFillet of Cod - 2 rubies\nFillet of Salmon - 2 rubies\nSmoked Trout - 9 rubies\nJar of Tuna - 3 rubies\nFillet of Smoked Haddock - 6 rubies\n\033[36m'What are you here to buy?'\033[0m"
        ),
        "Options": [
            "Purchase a fillet of cod",
            "Purchase a fillet of salmon",
            "Purchase smoked trout",
            "Purchase a jar of tuna",
            "Purchase a fillet of smoked haddock",
            "Haggle",
            "Talk",
            "Leave",
        ],
        "Option0Requirements": lambda: game_state.rubies >= 2,
        "Option1Requirements": lambda: game_state.rubies >= 2,
        "Option2Requirements": lambda: game_state.rubies >= 9,
        "Option3Requirements": lambda: game_state.rubies >= 3,
        "Option4Requirements": lambda: game_state.rubies >= 6,
        "Option5Requirements": lambda: game_state.rubies < 9,
        "Move": [75, 76, 77, 78, 79, 80, 81, 73],
    },
    75: {
        "Text": "You purchased a Fillet of Cod [2 Rubies]",
        "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 2),
        "Item": "Fillet of Cod",
        "Automove": 74,
    },
    76: {
        "Text": "You purchased a Fillet of Salmon [2 Rubies]",
        "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 2),
        "Item": "Fillet of Salmon",
        "Automove": 74,
    },
    77: {
        "Text": "You purchased some Smoked Trout [9 Rubies]",
        "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 9),
        "Item": "Smoked Trout",
        "Automove": 74,
    },
    78: {
        "Text": "You purchased a Jar of Tuna [3 Rubies]",
        "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 3),
        "Item": "Jar of Tuna",
        "Automove": 74,
    },
    79: {
        "Text": "You purchased a Fillet of Smoked Haddock [6 Rubies]",
        "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 6),
        "Item": "Fillet of Smoked Haddock",
        "Automove": 74,
    },
    80: {
        "Text": "\033[36m'If you aren't here to buy anything, then get out.'\033[0m",
        "Automove": 73,
    },
    81: {
        "Text": "",
        "Script": lambda: fishEvaluation(),
        "Automove": 74,
    },
    82: {
        "Text": "",
        "Script": lambda: print2(
            "Current Rubies:"
            + str(game_state.rubies)
            + "\n\033[35m'Hey. I've got one bow in stock right now. It's 75 Rubies."
        ),
        "Options": ["Purchase the bow", "Talk", "Talk", "Leave"],
        "Option0Requirements": lambda: "Bow and Arrow"
        not in game_state.inventory.keyItems,
        "Option1Requirements": lambda: "Bow and Arrow"
        not in game_state.inventory.keyItems,
        "Move": [83, 84, 73],
    },
    83: {
        "Text": "Be seeing you around. I'm going home to pack my stuff - there's nothing left for me here.",
        "Requirements": game_state.rubies >= 75,
        "AlternateText": "\033[35m'Sorry, that's not really enough. I'd let it go for 75 rubies, maybe.'\033[0m",
        "Item": "Bow and Arrow",
        "ItemRequirements": game_state.rubies >= 75,
        "Automove": 82,
    },
    84: {
        "Text": "\033[35m'You did it! I can't believe it! That's really it! That's my mother's \033[47mSilver Amulet\033[0m\033[35m! I can't thank you enough! Here, have this bow, no charge! Thank you, thank you!",
        "Requirements": lambda: "Silver Amulet" in game_state.inventory.keyItems,
        "AlternateText": "\033[35m'Hey, do you think you could do something for me? Since everyone disappeared last night, I miss my mother. Do you think you could see if you could find her \033[47mSilver Amulet\033[0m\033[35m? I'd give you the bow for free if you did.'\033[0m",
        "Item": "Bow and Arrow",
        "ItemRequirements": lambda: "Silver Amulet" in game_state.inventory.keyItems,
        "Automove": 82,
    },
    85: {
        "Text": "\033[32m'Hello, I collect minerals. If you find any minerals, give them to me.'\033[0m",
        "Options": ["Sell minerals", "Sell minerals", "Leave"],
        "Option0Requirements": lambda: len(
            set(mysticalRocks) & set(game_state.inventory.items)
        )
        == 0,
        "Option1Requirements": lambda: len(
            set(mysticalRocks) & set(game_state.inventory.items)
        )
        != 0,
        "Move": [86, 87, 73],
    },
    86: {
        "Text": "\033[32m'I'm sorry, but you don't appear to have any minerals. Good day.'\033[0m",
        "Automove": 73,
    },
    87: {
        "Text": "",
        "Script": lambda: mineralEvaluation(),
        "Automove": 73,
    },
    88: {  # This is the worst and most fustrating part of the game Have fun :)
        "Text": "You are at the cave's entrance.",
        "Options": ["Enter the cave", "Go back to the village outskirts"],
        "Move": [91, 2],
    },
    89: {
        "Text": "You blow up the rubble. Light shines through, and a path to the surface appears.",
        "Script": lambda: setattr(game_state, "caveOpened", True),
        # game_state.inventory.items
        "Automove": 99,
    },
    90: {
        "Text": "You fish in the fishing pond and find a \033[47mSilver Amulet\033[0m.",
        "Requirements": lambda: "Fishing Rod" in game_state.inventory.keyItems
        and "Silver Amulet" not in game_state.inventory.keyItems
        and "Bow and Arrow" not in game_state.inventory.keyItems,
        "AlternateText": "You fish in the fishing pond but you find nothing.",
        "Items": "Silver Amulet",
        "ItemRequirements": lambda: "Fishing Rod" in game_state.inventory.keyItems
        and "Silver Amulet" not in game_state.inventory.keyItems
        and "Bow and Arrow" not in game_state.inventory.keyItems,
        "Automove": 127,
    },
    91: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and south.",
        "Options": ["Go north", "Go south"],
        "Move": [92, 88],
    },
    92: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north, south and west.",
        "Options": ["Go north", "Go south", "Go west"],
        "Move": [93, 91, 97],
    },
    93: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and south.",
        "Item": "A Funny-looking Rock",
        "ItemRequirements": lambda: "A Funny-looking Rock"
        not in game_state.inventory.items,
        "ItemText": "On the ground, you find a funny-looking rock.",
        "Options": ["Go north", "Go south"],
        "Move": [94, 92],
    },
    94: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and south.",
        "Options": ["Go east", "Go south"],
        "Move": [95, 93],
    },
    95: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north, south and west.",
        "Item": "What you think is an Emerald",
        "ItemRequirements": lambda: "What you think is an Emerald"
        not in game_state.inventory.items,
        "ItemText": "On the ground, you find what you think is an emerald.",
        "Options": ["Go north", "Go south", "Go west"],
        "Move": [96, 101, 94],
    },
    96: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your south and west.",
        "Options": ["Go south", "Go west"],
        "Move": [95, 100],
    },
    97: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and east.",
        "Options": ["Go north", "Go east"],
        "Move": [98, 92],
    },
    98: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and south.",
        "Item": "Some strange stone",
        "ItemRequirements": lambda: "Some strange stone"
        not in game_state.inventory.items,
        "ItemText": "On the ground, you find some strange stones.",
        "Options": ["Go north", "Go south"],
        "Move": [99, 97],
    },
    99: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your northeast, south and northwest.",
        "Requirements": lambda: game_state.caveOpened,
        "AlternateText": "You are within the cave. It is difficult to see. There is a path to your northeast and south. There is a lot of rubble to your northwest.",
        "Options": [
            "Go northeast",
            "Go south",
            "Go northwest",
            "Destroy the rubble with a bomb",
        ],
        "Option2Requirements": lambda: game_state.caveOpened,
        "Option3Requirements": lambda: not game_state.caveOpened
        and "Bomb" in game_state.inventory.items,
        "Move": [100, 98, 52, 89],
    },
    100: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north, east and southwest.",
        "Options": ["Go north", "Go east", "Go southwest"],
        "Move": [129, 96, 99],
    },
    101: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north, northeast and south.",
        "Options": ["Go north", "Go northeast", "Go south"],
        "Move": [95, 109, 102],
    },
    102: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north, northeast, southeast and south.",
        "Options": ["Go north", "Go northeast", "Go southeast", "Go south"],
        "Move": [101, 104, 103, 116],
    },
    103: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and west.",
        "Options": ["Go east", "Go west"],
        "Move": [105, 102],
    },
    104: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and west.",
        "Options": ["Go east", "Go west"],
        "Move": [107, 102],
    },
    105: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and west.",
        "Options": ["Go east", "Go west"],
        "Move": [106, 103],
    },
    106: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and west.",
        "Options": ["Go north", "Go west"],
        "Move": [108, 105],
    },
    107: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and west.",
        "Options": ["Go east", "Go west"],
        "Move": [108, 104],
    },
    108: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your south and west.",
        "Options": ["Go south", "Go west"],
        "Move": [106, 107],
    },
    109: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north, southeast and southwest.",
        "Item": "Some Tourmaline, maybe",
        "ItemRequirements": lambda: "Some Tourmaline,maybe",
        "ItemText": "On the ground, you find what might be some tourmaline.",
        "Options": ["Go north", "Go southeast", "Go southwest"],
        "Move": [110, 114],
    },
    110: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your northeast and south.",
        "Options": ["Go northeast", "Go south"],
        "Move": [111, 109],
    },
    111: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your southeast and southwest.",
        "Options": ["Go southeast", "Go southwest"],
        "Move": [112, 110],
    },
    112: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your northwest and south.",
        "Options": ["Go northwest", "Go south"],
        "Move": [111, 113],
    },
    113: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and southwest.",
        "Options": ["Go north", "Go southwest"],
        "Move": [112, 114],
    },
    114: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your northeast and northwest.",
        "Item": "A Weird shard of something",
        "ItemRequirements": lambda: "A Weird shard of something"
        not in game_state.inventory.items,
        "ItemText": "On the ground, you find a weird shard of something.",
        "Options": ["Go northeast", "Go northwest"],
        "Move": [113, 109],
    },
    116: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and south.",
        "Options": ["Go north", "Go south"],
        "Move": [102, 117],
    },
    117: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north, east and southeast.",
        "Options": ["Go north", "Go east", "Go southeast"],
        "Move": [116, 118, 121],
    },
    118: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and west.",
        "Options": ["Go east", "Go west"],
        "Move": [119, 117],
    },
    119: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and west.",
        "Options": ["Go east", "Go west"],
        "Move": [120, 118],
    },
    120: {
        "Text": "You are within the cave. It is a dead-end. The only path is back where you came.",
        "Item": "Golden Idol",
        "ItemRequirements": lambda: "Golden Idol" not in game_state.inventory.keyItems,
        "ItemText": "You see a \033[47mGolden Idol\033[0m on the floor of the cave.",
        "Options": ["Go back"],
        "Move": [119],
    },
    121: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your northwest and east.",
        "Options": ["Go northwest", "Go east"],
        "Move": [117, 122],
    },
    122: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and west.",
        "Item": "A Chunk of Marble",
        "ItemRequirements": lambda: "A Chunk of Marble"
        not in game_state.inventory.items,
        "ItemText": "On the ground, you find a chunk of marble.",
        "Options": ["Go east", "Go west"],
        "Move": [123, 121],
    },
    123: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and west.",
        "Options": ["Go east", "Go west"],
        "Move": [124, 122],
    },
    124: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and west.",
        "Options": ["Go north", "Go west"],
        "Move": [125, 123],
    },
    125: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and south.",
        "Options": ["Go north", "Go south"],
        "Move": [126, 124],
    },
    126: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your north and south.",
        "Item": "A Stone that looks kind of like a face",
        "ItemRequirements": lambda: "A Stone that looks kind of like a face"
        not in game_state.inventory.items,
        "ItemText": "On the ground, you find a stond that looks kind of like a face.",
        "Options": ["Go north", "Go south"],
        "Move": [127, 125],
    },
    127: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your south and west. You can make out a small pond in front of you.",
        "Options": ["Go north", "Go south", "Fish in the pond"],
        "Option2Requirements": lambda: "Fishing Rod" in game_state.inventory.keyItems,
        "Move": [126, 128, 90],
    },
    128: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and west.",
        "Item": "A beautiful, azure blue rock",
        "ItemRequirements": lambda: "A beautiful, azure blue rock"
        not in game_state.inventory.items,
        "ItemText": "On the ground, you find a beautiful, azure blue rock.",
        "Options": ["Go east", "Go west"],
        "Move": [127, 129],
    },
    129: {
        "Text": "You are within the cave. It is difficult to see. There is a path to your east and south.",
        "Options": ["Go east", "Go south"],
        "Move": [128, 100],
    },
}

##

import curses
import time
from dataclasses import dataclass
import random
import sys
from typing import Any

import tui
import toml_reader

print3 = tui.print3


gameInfo: dict[str, Any]
history: dict[int]
endingText: dict[str, str]
defaultEnding: str
loseText: dict[str, str]
defaultLose: str
keyItems: list[str]


gameInfo: dict[str, Any] = toml_reader.read_toml("game.toml")["game_info"]

history: list[int] = []

endingText: dict[str, str] = {
    "Good": "And so, overnight, all the people returned to the village, as "
        "if they had never left.\nSoon after, the village was lifted into high "
        "spirits as the harvest had been the best in almost thirty years.\n"
        "Despite the prospering village, you decided to leave.\nYou had no "
        "desire to stay after the events you just experienced, and you would "
        "rather leave than stay to make some money.",
    "Secret": "And so, overnight, you became the new shopkeeper, but nothing "
        "really changed in the end.\nThe villagers never returned, but many "
        "travellers came, hearing about what happened.\nMany decided to stay "
        "after a plentiful harvest brought good omens to the village.\nThis, "
        "however, would not be the last of it...\n...and you knew that.",
    "SHM": "You achieved the\n|\nEnding.\nTry Again?",
}

defaultEnding: str = (
    "\033[1mThe Shopkeeper's Quest\033[0m\n"
    "1.2\n\n"
    "Created by SolidLamp\n\n"
    "With inspiration from:\n"
    "Colossal Cave Adventure, by Will Crowther and Don Woods;\n"
    "King's Quest, by Sierra On-Line;\n"
    "Henry Stickmin, by Puffballs United;\n"
    "Minecraft: Story Mode, by Telltale Games;\n"
    "and RTX Morshu: The Game, by koshkamatew\n"
    "With special thanks to\n"
    "\033[1m\033[33mYOU\033[0m\n"
    "for playing the game,\n"
    "for if a tree falls and no one hears it, does it make a sound?"
)

loseText: dict[str, str] = {
    "SHM": "You achieved the\n|\nEnding.\nTry Again?",
}

defaultLose: str = "\n\n\033[31m\033[1mYou died!\033[0m\n'|'\n\n\n"

keyItems: list[str] = [
    "Rusted Sword",
    "Amber Necklace",
    "Golden Idol",
    "Silver Amulet",
    "Bow and Arrow",
    "Fishing Rod",
    "Ancient Key",
]


@dataclass
class Inventory:
    """
    The main inventory of a game, which allows for adding items and key items,
    as well as displaying them as a string.
    """

    # which I may or may not have mainly used StackOverflow to figure out.
    items: list[str] = None
    keyItems: list[str] = None

    def __post_init__(self) -> None:
        self.items = [] if self.items is None else self.items
        self.keyItems = [] if self.keyItems is None else self.keyItems

    def getItem(self, item: str, win: curses.window) -> None:
        print3(win, "\nYou got \033[1m" + str(item) + "\033[0m!\n")
        self.items.append(item)
        print3(win, "Press any button to continue...")
        win.getch()

    def getKeyItem(self, item: str, win: curses.window) -> None:
        if item in self.keyItems:
            return
        print3(win, "\nYou got \033[1m" + str(item) + "\033[0m!\n")
        self.keyItems.append(item)
        print3(win, "Press any button to continue...")
        win.getch()

    def hasItem(self, item: str) -> bool:
        if item in self.items:
            return True
        if item in self.keyItems:
            return True
        return False

    def __str__(self) -> str:
        if not self.items and not self.keyItems:
            return "Your inventory is empty"
        output = []
        if self.items:
            output.append(
                "\033[1mItems\033[0m:\n" + "\n".join(f"- {item}" for item in self.items)
            )
        if self.keyItems:
            output.append(
                "\033[1mKey Items\033[0m:\n"
                + "\n".join(f"- {item}" for item in self.keyItems)
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

    def getRuby(self, obtained: int, win: curses.window) -> None:
        print3(win, "\nYou got \033[1m" + str(obtained) + "\033[0m Rubies!")
        self.rubies += obtained
        print3(
            win,
            "\033[0m\n You currently have \033[1m"
            + str(self.rubies)
            + "\033[0m Rubies.\n",
        )
        print3(win, "Press any button to continue...")
        win.getch()


game_state = gameState(inventory=Inventory(items=[]))


def overwrite_rooms(rooms: dict, extrarooms: dict) -> dict:
    new_rooms = rooms.copy()
    for key in filter(lambda key: key in rooms.keys(), extrarooms.keys()):  # orubt
        new_rooms[key].update(extrarooms[key])
    return new_rooms


def get_rooms(win: curses.window) -> dict:
    """The most important part; returns a dict of rooms to the engine."""
    hasItem = game_state.inventory.hasItem
    rooms = toml_reader.read_gamedata("game.toml")
    room_scripts = {
        0: {
            "Script": lambda: debug(win),
        },
        4: {
            "Option0Requirements": lambda: hasItem("Rusted Sword"),
        },
        5: {
            "Option0Requirements": lambda: not hasItem("Bow and Arrow"),
            "Option1Requirements": lambda: hasItem("Bow and Arrow"),
        },
        13: {
            "Option1Requirements": lambda: game_state.rubies > 0,
        },
        14: {
            "KeyItemRequirements": lambda: not hasItem("Ancient Key")
            and history[:10] == [18, 19, 18, 12, 39, 12, 39, 12, 13, 14],
        },
        15: {
            "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 1),
            "KeyItemRequirements": lambda: not hasItem("Ancient Key")
            and history[:10] == [18, 19, 18, 12, 39, 12, 39, 12, 13, 15],
        },
        19: {
            "Option0Requirements": lambda: hasItem("Ancient Key"),
        },
        27: {
            "Script": lambda: game_state.getRuby(9000, win),
        },
        33: {
            "Script": lambda: (win.clear(), setattr(game_state, "beatenGame", True)),
        },
        38: {
            "Script": lambda: (time.sleep(0.3), sys.exit()),
        },
        52: {
            "Requirements": lambda: game_state.caveOpened,
            "Option4Requirements": lambda: game_state.caveOpened,
        },
        57: {
            "KeyItemRequirements": lambda: not hasItem("Amber Necklace"),
        },
        66: {
            "Text": "\033[93m'"
            + random.choice(ShopkeeperQuotes)
            + "'\033[0m\nCurrent Rubies: "
            + str(game_state.rubies)
            + "\nLamp Oil - 15 Rubies\nRope - 20 Rubies\nBomb - 30 Rubies",
            "Option0Requirements": lambda: game_state.rubies >= 15,
            "Option1Requirements": lambda: game_state.rubies >= 20,
            "Option2Requirements": lambda: game_state.rubies >= 30,
            "Option3Requirements": lambda: game_state.rubies < 30,
            "Option4Requirements": lambda: itemEvaluation() == 3,
            "Option5Requirements": lambda: itemEvaluation() > 1,
            "Option6Requirements": lambda: itemEvaluation() == 0,
        },
        67: {
            "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 15),
        },
        68: {
            "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 20),
        },
        69: {
            "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 30),
        },
        70: {
            "Script": lambda: (
                ShopkeeperFinalSpeech(win),
                setattr(game_state, "beatenGame", True),
            ),
        },
        71: {
            "Text": "\033[93m'" + random.choice(ShopkeeperQuotesExit) + "'\033[0m",
        },
        73: {
            "Requirements": lambda: game_state.fletcherOpen,
            "Option1Requirements": lambda: game_state.fletcherOpen,
        },
        74: {
            "Text": "Current Rubies:"
            + str(game_state.rubies)
            + "\nFillet of Cod - 2 rubies\nFillet of Salmon - 2 rubies\n"
            + "Smoked Trout - 9 rubies\nJar of Tuna - 3 rubies\n"
            + "Fillet of Smoked Haddock - 6 rubies\n"
            + "\033[36m'What are you here to buy?'\033[0m",
            "Option0Requirements": lambda: game_state.rubies >= 2,
            "Option1Requirements": lambda: game_state.rubies >= 2,
            "Option2Requirements": lambda: game_state.rubies >= 9,
            "Option3Requirements": lambda: game_state.rubies >= 3,
            "Option4Requirements": lambda: game_state.rubies >= 6,
            "Option5Requirements": lambda: game_state.rubies < 9,
        },
        75: {
            "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 2),
        },
        76: {
            "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 2),
        },
        77: {
            "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 9),
        },
        78: {
            "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 3),
        },
        79: {
            "Script": lambda: setattr(game_state, "rubies", game_state.rubies - 6),
        },
        81: {
            "Script": lambda: fishEvaluation(win),
        },
        82: {
            "Text": "Current Rubies:"
            + str(game_state.rubies)
            + "\n\033[35m'Hey. I've got one bow in stock right now. It's 75 Rubies.",
            "Options": ["Purchase the bow", "Talk", "Talk", "Leave"],
            "Option0Requirements": lambda: not hasItem("Bow and Arrow"),
            "Option1Requirements": lambda: not hasItem("Bow and Arrow"),
        },
        83: {
            "Requirements": lambda: game_state.rubies >= 75,
            "Script": lambda: setattr(
                game_state,
                "rubies",
                (
                    game_state.rubies - 75
                    if game_state.rubies >= 75
                    else game_state.rubies
                ),
            ),
            "KeyItemRequirements": lambda: game_state.rubies >= 75,
        },
        84: {
            "Requirements": lambda: hasItem("Silver Amulet"),
            "KeyItemRequirements": lambda: hasItem("Silver Amulet"),
        },
        85: {
            "Option0Requirements": lambda: len(
                set(mysticalRocks) & set(game_state.inventory.items)
            )
            == 0,
            "Option1Requirements": lambda: len(
                set(mysticalRocks) & set(game_state.inventory.items)
            )
            != 0,
        },
        87: {
            "Script": lambda: mineralEvaluation(win),
        },
        89: {
            "Script": lambda: setattr(game_state, "caveOpened", True),
        },
        90: {
            "Requirements": lambda: hasItem("Fishing Rod")
            and not hasItem("Silver Amulet")
            and not hasItem("Bow and Arrow"),
            "KeyItemRequirements": lambda: hasItem("Fishing Rod")
            and not hasItem("Silver Amulet")
            and not hasItem("Bow and Arrow"),
        },
        93: {
            "ItemRequirements": lambda: not hasItem("A Funny-looking Rock")
            and random.randrange(0, 3) == "2",
        },
        95: {
            "ItemRequirements": lambda: not hasItem("What you think is an Emerald")
            and random.randrange(0, 3) == "2",
        },
        98: {
            "ItemRequirements": lambda: not hasItem("Some strange stone")
            and random.randrange(0, 3) == "2",
        },
        99: {
            "Requirements": lambda: game_state.caveOpened,
            "Option2Requirements": lambda: game_state.caveOpened,
            "Option3Requirements": lambda: not game_state.caveOpened
            and hasItem("Bomb"),
        },
        109: {
            "ItemRequirements": lambda: not hasItem("Some Tourmaline, maybe")
            and random.randrange(0, 3) == "2",
        },
        114: {
            "Text": "You are within the cave. It is difficult to see. "
                    "There is a path to your northeast and northwest.",
            "Item": "A Weird shard of something",
            "ItemRequirements": lambda: not hasItem("A Weird shard of something")
            and random.randrange(0, 3) == "2",
            "ItemText": "On the ground, you find a weird shard of something.",
            "Options": ["Go northeast", "Go northwest"],
            "Move": [113, 109],
        },
        120: {
            "KeyItemRequirements": lambda: not hasItem("Golden Idol"),
        },
        122: {
            "ItemRequirements": lambda: not hasItem("A Chunk of Marble")
            and random.randrange(0, 3) == "2",
        },
        126: {
            "ItemRequirements": lambda: not hasItem(
                "A Stone that looks kind of like a face"
            )
            and random.randrange(0, 3) == "2",
        },
        127: {"Option2Requirements": lambda: hasItem("Fishing Rod")},
        128: {
            "ItemRequirements": lambda: not hasItem("A beautiful, azure blue rock")
            and random.randrange(0, 3) == "2",
        },
        130: {
            "Script": lambda: ShopkeeperFinalSpeech(win),
        },
    }
    rooms = overwrite_rooms(rooms, room_scripts)
    return rooms


# Additional Scripts


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
    "Sorry I can't give discounts - I have a business to run, and I must make my "
        "money somehow.",
    "I don't blame you for coming inside in this winter.",
    "Sit down a while. I don't want you too stressed, my friend.",
    "I always believe that everyone has a tale worth telling - maybe talk to "
        "more people.",
    "Have you checked out the bazaar? There's a fisherman there who sells "
        "excellent-quality rods.",
    "Have you heard the news about the King? It's said that he's fallen ill. "
        "He's a good man - I hope he fully recovers.",
    "Have you seen the nearby forest? There's been some monkey sightings there.",
]

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


def itemEvaluation() -> int:
    cursedItems = len(
        {"Rusted Sword", "Amber Necklace", "Golden Idol"}
        & set(game_state.inventory.keyItems)
    )
    return cursedItems


def ShopkeeperFinalSpeech(win: curses.window) -> None:
    print3(
        win,
        "\033[93m'Well, I'll be. That's all of them. Honestly, I kind of "
        "doubted you could do it - now I see that my doubt was misplaced! "
        "You will go down in legend for your heroism!'",
    )
    time.sleep(0.75)
    print3(win, "\033[93m\n'Oh, and just one more thing: thank you.'\033[0m")
    time.sleep(1.5)


def ShopkeeperAffirmations(win: curses.window) -> None:
    cursedItems = len(
        {"Rusted Sword", "Amber Necklace", "Golden Idol"}
        & set(game_state.inventory.keyItems)
    )
    print3(
        win,
        f"\033[93m'Great! You managed to get {cursedItems} of the items - now "
        f"we just need {3 - cursedItems} more!'\033[0m",
    )


def fishEvaluation(win: curses.window) -> None:
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
    if fishBought >= 1 and not game_state.inventory.hasItem("Fishing Rod"):
        print3(
            win,
            "\033[36m'You know, I recently got a new fishing rod. Say, you "
            "can have my old one, since you bought something.'\033[0m",
        )
        game_state.inventory.getKeyItem("Fishing Rod", win)
    else:
        print3(
            win,
            "\033[36m'You know, I'd be more in the mood to talk if you bought "
            "something.'\033[0m",
        )


def mineralEvaluation(win: curses.window) -> None:
    for item in [
        item for item in list(game_state.inventory.items) if item in list(mysticalRocks)
    ]:  # This is not that readable but it does stuff basically]
        value = mysticalRocks[item]
        game_state.getRuby(value, win)
        game_state.inventory.items.remove(item)
    print3(
        win,
        "\033[32m'Thank you so much. These will be excellent to add to my "
        "collection.'\033[0m",
    )


def debug(win: curses.window) -> None:
    game_state.inventory.getKeyItem("Rusted Sword", win)
    game_state.inventory.getKeyItem("Amber Necklace", win)
    game_state.inventory.getKeyItem("Golden Idol", win)
    game_state.inventory.getKeyItem("Ancient Key", win)
    game_state.inventory.getKeyItem("Fishing Rod", win)
    game_state.inventory.getKeyItem("Bow and Arrow", win)
    game_state.inventory.getKeyItem("Silver Amulet", win)
    game_state.inventory.getItem("Lamp Oil", win)
    game_state.inventory.getItem("Lamp Oil", win)
    game_state.inventory.getItem("Rope", win)
    game_state.inventory.getItem("Bomb", win)
    game_state.inventory.getItem("Bomb", win)
    game_state.getRuby(9001, win)

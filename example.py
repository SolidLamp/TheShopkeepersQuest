from dataclasses import dataclass

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
        "Option1Requirements": lambda: not game_state.caveOpened,
        "Option2Requirements": lambda: game_state.caveOpened,
        "Move": [1,4,2],
    },
    4: {
        "Text": "You opened the cave.",
        "Script": lambda: setattr(game_state, "caveOpened", True),
        "Automove": 3,
    },
}
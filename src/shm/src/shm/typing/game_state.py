from dataclasses import dataclass, field

from shm.tui import print3
from shm.typing.box import Box
from shm.typing.restrictedscr import RestrictedWindow


@dataclass
class Inventory:
    """
    The main inventory of a game, which allows for adding items and key items,
    as well as displaying them as a string.
    """

    items: list[str] = field(default_factory=list)
    keyItems: list[str] = field(default_factory=list)

    def getItem(self, item: str, win: RestrictedWindow) -> None:
        print3(win, "\nYou got \033[1m" + str(item) + "\033[0m!\n")
        self.items.append(item)
        print3(win, "Press any button to continue...")
        win.getch()

    def getKeyItem(self, item: str, win: RestrictedWindow) -> None:
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
class GameState:
    inventory: Inventory
    money: Box[int] = field(default_factory=lambda: Box(0))

    def getRuby(self, obtained: int, win: RestrictedWindow) -> None:
        print3(win, "\nYou got \033[1m" + str(obtained) + "\033[0m Money!")
        self.money += obtained
        print3(
            win,
            "\033[0m\n You currently have \033[1m"
            + str(self.money)
            + "\033[0m Money.\n",
        )
        print3(win, "Press any button to continue...")
        win.getch()

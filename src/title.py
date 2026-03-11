from typing import Any


from collections.abc import Callable
import os.path
import sys
import time

try:
    import curses
except ImportError as e:
    print(f"The curses module was not found.\nError: {e}")
    sys.exit(1)

import save_handler
import shm
import toml_reader
import tui


class MiniSHM:
    """
    MiniSHM is a tiny engine designed to run the title screen and nothing else.
    It expects a dictionary of 'rooms' with every key is either an int, str or lambda.
    When the key is an int or str, that option will take you to that room;
    when the key is a lambda, it is executed. It has ZERO error checking.
    For more features, use the real SHM Engine.
    """

    def __init__(
        self, win: curses.window, options_dict: dict, title_string: str = "SHM Engine"
    ) -> None:
        """
        Initialises MiniSHM

        Args:
            win (curses.window):
            A curses window instance.

            options_dict (dict):
            The dictionary containing all options for the menu.

            title_string (str, optional):
            The string to display to the user while navigating the title screen.
            Defaults to "SHM Engine".
        """
        self.options_dict = options_dict
        self.title_string = title_string
        self.win = win

    def _option(self, key: int | str = 0) -> None:
        """
        Displays an option to the user

        Args:
            key (int | str, optional):
            The particular menu of the title screen to display.
            Defaults to 0.

        Returns:
            int: The chosen option by the user.
        """
        choices: Any = self.options_dict[key]
        options: list[Any] = list(choices.keys())
        query: int | str = tui.option(self.win, self.title_string, options, False)
        if isinstance(query, str):
            sys.exit(0)
        return query

    def screen(self, task: int | str | Callable[[], None] = 0) -> None:
        while isinstance(task, int) or isinstance(task, str):
            query = self._option(task)
            choices = self.options_dict[task]
            task = list(choices.values())[query]
        if callable(task):
            task()


def handle_save(
    win: curses.window, game_path: str = "game", save_path: str = "game"
) -> None:
    """
    Handles the save files

    Args:
        win (curses.window): A curses window instance.

        game_path (str, optional):
        The relative path to the gamefile. 
        Defaults to "game".

        save_path (str, optional):
        The relative path to the savefile.
        Defaults to "game".

    """
    if os.path.exists(save_path + ".sav") and save_handler.save_validifier(
        save_handler.read_save(save_path)
    ):
        saveFile = save_handler.read_save(save_path)
        shm.run(
            win,
            0,
            saveFileName=save_path,
            saveFile=saveFile,
            gameFile_name=game_path,
            gameFile_path="./",
        )
    else:
        shm.run(
            win, saveFileName=save_path,
            gameFile_name=game_path,
            gameFile_path="./"
        )


def main(win: curses.window) -> None:
    curses.curs_set(0)
    win.scrollok(True)
    win.nodelay(True)
    tui.colorsetup(win)
    curses.cbreak()
    engineInfo = toml_reader.get_engine_info()
    tui.draw_titlebar(win, engineInfo)
    padding = 1
    padx1 = 0
    padx2 = 0
    pady1 = 0
    pady2 = 1
    newwin = tui.create_newwin(win, padding, padx1, padx2, pady1, pady2)
    string = (
        "\033[1;38;5;75m"
        + r"""
        ___ _  _ ____
         |  |__| |___
         |  |  | |___

        ____ _  _ ____ ___  _  _ ____ ____ ___  ____ ____ ____ '
        [__  |__| |  | |__] |_/  |___ |___ |__] |___ |__/ [__
        ___] |  | |__| |    | \_ |___ |___ |    |___ |  \ ___]

                               ____ _  _ ____ ____ ___
                               |  | |  | |___ [__   |
                               |_\| |__| |___ ___]  |
                                                       """
        + "\033[0m"
    )
    screen_options = {
        0: {
            "Play The Shopkeeper's Quest": 1,
            "Quit": lambda: sys.exit(),
        },
        1: {
            "Save 1": lambda: handle_save(win, game_path="game", save_path="game1"),
            "Save 2": lambda: handle_save(win, game_path="game", save_path="game2"),
            "Save 3": lambda: handle_save(win, game_path="game", save_path="game3"),
            "Back": 0,
        },
    }
    title = MiniSHM(newwin, screen_options, string)
    title.screen(0)
    sys.exit(0)


def title() -> None:
    print("[The Shopkeeper's Quest]")
    while 1:
        curses.wrapper(main)


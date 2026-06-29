"""The title screen to be displayed to the user.

Typical usage example:

title.title()
title_screen = MiniSHM(win, options_dict, title_string)
"""

import os.path
import sys
from collections.abc import Callable
from typing import Any, NoReturn
from importlib.resources import files


try:
    import curses
except ImportError as e:
    print(f"The curses module was not found.\nError: {e}")
    sys.exit(1)

import shm
import shm.save_handler as save_handler
import shm.toml_reader as toml_reader
import shm.tui as tui


class MiniSHM:
    """Tiny engine designed to run the title screen and nothing else.

    It expects a dictionary of 'rooms' with every key is either an
    int, str or lambda.
    When the key is an int or str, that option will take you to that room;
    when the key is a lambda, it is executed. It has ZERO error checking.
    For more features, use the real SHM Engine.
    """

    def __init__(
        self,
        win: curses.window,
        options_dict: dict[int | str, dict[str, int | Callable[[], NoReturn | None]]],
        title_string: str = "SHM Engine",
    ) -> None:
        """Initialises MiniSHM.

        Args:
            win (curses.window):
            A curses window instance.

            options_dict (dict[int | str, dict]):
            The dictionary containing all options for the menu.

            title_string (str, optional):
            The string to display to the user while navigating the title
            screen.
            Defaults to "SHM Engine".
        """
        self.options_dict: dict[
            int | str, dict[str, int | Callable[[], NoReturn | None]]
        ] = options_dict
        self.title_string: str = title_string
        self.win: curses.window = win

    def _option(self, key: str | int = 0) -> int:
        """Displays an option to the user. Internal use only.

        Args:
            key (int | str, optional):
            The particular menu of the title screen to display.
            Defaults to 0.

        Returns:
            int: The chosen option by the user.
        """
        choices: dict[str, int | Callable[[], None]] = self.options_dict[key]
        options: list[str] = list(choices.keys())
        query: int | str = tui.option(self.win, self.title_string, options, False)
        if isinstance(query, str):
            sys.exit(0)
        return query

    def screen(self, task: int | str | Callable[[], None] = 0) -> None:
        """Executes the current task of the chosen option.

        Args:
            task (int | str | Callable[[], None], optional):
            If an int or str, moves to that room.
            If a Callable, executes the task.
            Defaults to 0.
        """
        while isinstance(task, int) or isinstance(task, str):
            query: str | int = self._option(task)
            choices: dict[str, int | Callable[[], None]] = self.options_dict[task]
            task: int | Callable[[], None] = list(choices.values())[query]
        if callable(task):
            task()


def handle_save(
    win: curses.window, game_path: str = "game", save_path: str = "game", dir_save: bool = False
) -> None:
    """Handles the save files.

    Args:
        win (curses.window): A curses window instance.

        game_path (str, optional):
        The relative path to the gamefile, relative to the program's install location.
        Defaults to "game".

        save_path (str, optional):
        The relative path to the savefile, relative to the program's install location.
        Defaults to "game".

    """
    module_path: str = str(files(__spec__.parent))
    save_path: str = os.path.join(module_path, save_path)
    
    if os.path.exists(save_path + ".sav") and save_handler.save_validifier(
        save_handler.read_save(save_path)
    ):
        saveFile: dict[Any, Any] = save_handler.read_save(save_path)
        shm.run(
            win,
            starting_room=0,
            saveFileName=save_path,
            saveFile=saveFile,
            gameFile_name=game_path,
            gameFile_path=module_path,
        )
    else:
        shm.run(
            win, starting_room=0, saveFileName=save_path, gameFile_name=game_path, gameFile_path=module_path
        )


def main(win: curses.window) -> None:
    """The main title screen, must be loaded with curses.wrapper.

    Args:
        win (curses.window): A curses window instance.
    """
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
        + r"""⠀⢀⡠⣤⣀⡀⠀⠀⠀⠀ ⣀⣀⠄⠀⠀
⠀⢂⠀⠀⢈⠛⠋⠊⠀ ⠀⢸⣽⠀⣠⠀ ⠀⠀⣀⣤⠀⠀
⠀⠀⠀⠀⠸⣧⠀⠀⠀ ⠀⢸⣽⠈⢹⣗ ⠀⢼⡇⠹⡷⠀
⠀⠀⡠⣤⣠⠃⠀⠀⡀ ⠀⢸⣽⠀⢸⣟⠀ ⢽⣧⠁⢀⠀
⠀⠀⠀⠀⠉⠛⠓⠁⠀⠀ ⠈⠋⠁⡼⠇⠀ ⠀⠙⠋⠁⠀
⠀⠀⣀⢤⢤⣀⣀⢀  ⠀⣀⣀⠄⠀⠀⠀⠀             ⠀⣀⣀⠄⠀⠀                               ⠠⣤
⠀⠔⠀⠀⠀⠉⠉⠀   ⢸⣽⠀⣠⠀⠀⠀⢀⢀⣤⣄⠀⠀⠀⣠⡀⣠⣄⠀ ⠀⢹⡗⠀⢀⠀⠀ ⠀⣀⣤⠀⠀ ⠀⣀⣤⠀⠀⠀⣠⡀⣠⣄⠀  ⠀⣀⣤⠀⠀⠀⣠⣄⢠⣄⠘⠋⠀⣠⣀⡀⠀
⠀⡀⠐⢤⡴⠞⠛⠢ ⠀ ⢸⣽⠈⢹⣗⠀⠀⢸⣗⠈⣾⡇ ⠈⢽⡏⠀⣿⡆ ⠀⢸⡯⠒⣟⠃⠀⠀⢼⡇⠹⡷⠀⠀⢼⡇⠹⡷⠀⠈⢽⡏⠀⣿⡆ ⠀⢼⡇⠹⡷⠀⠀⢸⣽⠈⠃⠀⠠⣿⡈⣁⡀⠀
⠀⠡⣄⠀⠀⠀⢀⡠⠁  ⢸⣽⠀⢸⣟⠀⠀⣸⣗⠀⣞⠇ ⠀⣽⣇⠀⣷⠇⠀⠀⢸⡯⠘⣟⣇ ⠀⢽⣧⠁⢀⠀⠀⢽⣧⠁⢀⠀⠀⣽⣇⠀⣷⠇ ⠀⢽⣧⠁⢀⠀⠀⢰⣻⠀⡀ ⠀⢛⠈⢹⡗
⠀⠀⠈⠛⠛⠛⠋⠀⠀⠀ ⠈⠋⠁⡼⠇⠀⠀⠈⠙⠋⠁⠀ ⠈⢽⡞⠋⠁⠀ ⠀⠙⠋⠁⠹⠋⠀ ⠀⠙⠋⠁⠀ ⠀⠙⠋⠁ ⠈⢽⡞⠋⠁⠀ ⠀ ⠙⠋⠁⠀⠀⠈⠙⠉⠀ ⠀⠋⠛⠊⠀
⠀⠀⠠⣤⢤⣤⣀⠀⠀⠀                   ⠀⠀⡀⠀⠀
⠀⢸⡀⠀⠁⠀⠈⠱⡀⠀ ⣀⣤⠀⢀⡤⠀ ⠀⣀⣤⠀⠀⠀⣠⣀⡀ ⠀⢀⣰⣇⡀⠀
⠀⠈⢿⠄⠀⠀⠀⠀⠂⠀ ⠀⣿ ⢹⡯⠀⠀⢼⡇⠹⡷⠀⠠⣿⡈⣁⡀⠀⠈⣹⡇⠁⠀
⠀⡠⣬⣀⠀⠠⢦⣄⠃⠀ ⢀⣿⣀⢸⡯⠀⠀⢽⣧⠁⢀⠀⠀⢛⠈⢹⡗⠀⠀⣺⡇⠀⠀
⠀⠀⠈⠙⠛⠒⠂⠙⠒  ⠈⠙⠁⠈⠋⠁⠀⠀⠙⠋⠁ ⠀⠋⠛⠊⠀⠀⠀⠉⠏⠁⠀
"""
        + "\033[0m"
    )
    screen_options: dict[int | str, dict[str, int | Callable[[], NoReturn | None]]] = {
        0: {
            "Play The Shopkeeper's Quest": 1,
            "Quit": lambda: sys.exit(),
        },
        1: {
            "Save 1": lambda: handle_save(win, game_path="game", save_path="game1"),
            "Save 2": lambda: handle_save(win, game_path="game", save_path="game2"),
            "Save 3": lambda: handle_save(win, game_path="game2", save_path="game3"),
            "Back": 0,
        },
    }
    title = MiniSHM(newwin, screen_options, string)
    title.screen(0)
    sys.exit(0)


def title() -> None:
    """Sets up a curses wrapper and creates the title screen.
    """
    print("[The Shopkeeper's Quest]")
    while 1:
        curses.wrapper(main)

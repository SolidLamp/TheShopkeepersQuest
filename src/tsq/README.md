# The Shopkeeper's Quest
[![Get it on Itch.io](https://img.shields.io/badge/Get%20it%20on%20Itch.io-fa5c5c)](https://solidlamp.itch.io/tsq)
[![License: MIT](https://img.shields.io/github/license/SolidLamp/TheShopkeepersQuest)](https://github.com/SolidLamp/TheShopkeepersQuest/blob/main/LICENSE)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python 3.11](https://img.shields.io/badge/Python-3.11%2B-blue)
[![CodeFactor](https://www.codefactor.io/repository/github/solidlamp/theshopkeepersquest/badge)](https://www.codefactor.io/repository/github/solidlamp/theshopkeepersquest)

***

## About

The Shopkeeper's Quest is an adventure game with a curses-based TUI. The game takes you through a cursed (pun intended) world, guided by the advice of a mysterious shopkeeper and his quest for you to acquire three legendary items. You explore this world with the keyboard, mainly the arrow keys - as any traditional curses TUI provides. The game is developed in Python using curses, with a custom 'SHM Engine' 1.2, enabling an open modding API.

The Shopkeeper's Quest is licensed MIT.

<br>

The Shopkeeper's Quest has taken considerable inspiration from many brilliant games across the internet. The main inspirations for The Shopkeeper's Quest are the following:

- [Colossal Cave Adventure](https://en.wikipedia.org/wiki/Colossal_Cave_Adventure)
- [King's Quest](https://en.wikipedia.org/wiki/King%27s_Quest_I)
- [Henry Stickmin](https://simple.wikipedia.org/wiki/The_Henry_Stickmin_Collection)
- [Minecraft: Story Mode](https://en.wikipedia.org/wiki/Minecraft%3A_Story_Mode)
- [RTX Morshu: The Game](https://koshkamatew.itch.io/morshugame-demo)

## Requirements

- Python 3.11+.
- `ncurses`, ususally pre-installed on *nix systems. For Windows, you must install [windows-curses](https://pypi.org/project/windows-curses/).

## Usage
The game can be run as a module with `src/`, e.g. `python -m src` in the parent directory. Alternatively, the entry point script `TheShopkeepersQuest.py` can be used.
Example: 
```shell
$ python3 -m src
$ python3 ./TheShopkeepersQuest.py
```

## Contributing
For contributing, please see `CONTRIBUTING.rst` and read the docs for an understanding to the current state of the project.

AI contributions are not and will not be accepted.

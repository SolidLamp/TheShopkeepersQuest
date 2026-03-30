from collections.abc import Callable
from curses import window
from typing import Any, NotRequired, TypedDict

from .box import Box


class BattleHooks(TypedDict):
    level_hook: Box[int]
    exp_hook: Box[int]
    power_hook: Box[int]
    health_hook: Box[int]
    get_money_hook: Callable[[window, int], None]
    loss_text: str
    level_up_xp: NotRequired[Callable[[], int | Box[int]] | int | Box[int]]
    power_increase: NotRequired[Callable[[], int | Box[int]] | int | Box[int]]
    health_increase: NotRequired[Callable[[], int | Box[int]] | int | Box[int]]


class Enemy(TypedDict):
    name: str
    health: int
    exp: int
    money: int
    power: int


class EngineInfo(TypedDict):
    Name: str
    MajorVersion: str
    Patch: str
    Indev: bool
    PythonVer: float
    ReleaseDate: str
    Dist: str
    Link: str
    SaveVersion: int
    DefaultBorderStyle: int


class GameInfo(TypedDict):
    Name: str
    Version: str
    ReleaseDate: str
    Licence: str
    Creator: str
    Link: str
    game_id: str
    complevel: int
    abbr: str
    title: str
    desc: str
    starting_room: int
    default_titlebar_left: str
    default_titlebar_centre: str
    default_titlebar_right: str
    default_textspeed: float
    border_style: int
    variable_damage: bool
    hide_warnings: bool
    disable_debug: bool


class Room(TypedDict, total=False):
    # NOTE: Type checking would require the 'extra_items' attribute from Python 3.15;
    # Python 3.15 has not yet had a stable release yet as I am writing this comment;
    # thus, this TypedDict cannot be used for type checking;
    # it is thus solely used for documentation
    # NOTE #2: Do not code at 11 PM or you will start hallucinating like AI slop
    """
    This is the canonical format for rooms in the SHM Engine 1.2.
    This has a main purpose of showing the supported keys, not type checking.
    This TypedDict supports additional fields, although compromising type checking,
    as fields such as Option[]Requirements are variable, where # represents an int.
    Rooms within a game are recommended to use this order for their attributes.
    """
    Text: str
    Requirements: Callable[[], bool]
    AlternateText: str
    TextSpeed: float
    Desc: str
    titlebarCentre: str
    titlebarLeft: str
    titlebarRight: str
    Script: Callable[[], None]
    Item: str
    ItemRequirements: Callable[[], bool]
    ItemText: str
    KeyItem: str
    KeyItemRequirements: Callable[[], bool]
    KeyItemText: str
    Enemy: int | list[int]  # Refers to the ID of the enemy
    Options: list[str]
    Option0Requirements: Callable[[], bool]
    Move: list[int | tuple[str, int]]
    Automove: int | tuple[str, int]
    InstantAutomove: bool
    Inventory: bool
    CanSave: bool
    Lose: str
    Ending: str


class Save(TypedDict):
    """This is the canonical format for save files with save version 1."""

    Game: str
    Saved: str
    save_version: int
    RoomID: int
    History: list[int]
    game_state: dict[str, Any]
    inventory: dict[str, list[str]]
    game_id: NotRequired[int | str]
    save_id: int | str

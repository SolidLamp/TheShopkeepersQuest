from collections.abc import Callable
from curses import window
from typing import Any, NotRequired, TypedDict

from .box import Box
from .room import Room


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


class GameFile(TypedDict):
    gameInfo: GameInfo
    history: list[int]
    defaultEnding: str
    defaultLose: str
    Inventory: NotRequired[type]
    gameState: NotRequired[type]
    game_state: Any
    enemies: NotRequired[dict[str, Enemy]]
    boss_list: NotRequired[list[str]]
    battle_hooks: NotRequired[BattleHooks]
    get_rooms: Callable[[window], dict[int, Room]]


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

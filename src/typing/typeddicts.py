from collections.abc import Callable
from curses import window
from typing import Any, Literal, NotRequired, Required, TypedDict

from .box import Box
from .room import Room


class BattleItem(TypedDict, total=False):
    description: str
    item_type: Required[Literal["Damage", "Heal", "Escape", "Script"]]
    magnitude: int # only used with "Damage" and "Heal" types
    script: Callable[[], None] # only used with "Script" type
    escape_chance: float # must be less than 1; only used with "Escape" type
    escape_chance_modifier: float # only used with "Escape" type


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
    boss: bool
    health: int
    exp: int
    money: int
    power: int
    run_chance: float


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
    currency_name: str


class GameFile(TypedDict):
    gameInfo: GameInfo
    history: list[int]
    endingText: NotRequired[dict[str, str]]
    defaultEnding: str
    loseText: NotRequired[dict[str, str]]
    defaultLose: str
    keyItems: NotRequired[list[str]]
    Inventory: NotRequired[type]
    gameState: NotRequired[type]
    game_state: Any
    enemies: NotRequired[dict[int | str, Enemy]]
    battle_hooks: NotRequired[BattleHooks]
    battle_items: NotRequired[dict[str, BattleItem]]
    money_hook: Box[int]
    get_rooms: Callable[[window], dict[int, Room]]


class Save(TypedDict):
    """This is the canonical format for save files with save version 2."""

    Game: str
    Saved: str
    save_version: int
    RoomID: int
    History: list[int]
    shop_exit: NotRequired[int]
    game_state: dict[str, Any]
    inventory: dict[str, list[str]]
    game_id: NotRequired[int | str]
    save_id: int | str

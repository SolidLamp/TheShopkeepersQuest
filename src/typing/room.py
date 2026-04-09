from typing import Callable, TypedDict


class Room(TypedDict, total=False):
    # NOTE: Type checking would require the 'extra_items' attribute from Python 3.15;
    # Python 3.15 has not yet had a stable release yet as I am writing this comment;
    # thus, this TypedDict cannot be used for type checking;
    # it is thus solely used for documentation
    """
    This is the canonical format for rooms in the SHM Engine 1.2.
    This has a main purpose of showing the supported keys, not type checking.
    This TypedDict supports additional fields, although compromising type checking,
    as fields such as Option[int]Requirements are variable.
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
    ShopItems: list[str]
    ShopItemCosts: list[int] 
    ShopItemMove: list[int | tuple[str, int]] # -1 represents none
    ShopEntrance: str | list[str]
    ShopExit: str | list[str]
    BattleText: str
    Enemies: list[int | str]  # Refers to the ID or name of the enemy
    EnemyChances: list[float | int]
    Options: list[str]
    Option0Requirements: Callable[[], bool]
    Move: list[int | tuple[str, int]]
    Automove: int | tuple[str, int]
    InstantAutomove: bool
    Inventory: bool
    CanSave: bool
    Lose: str
    Ending: str
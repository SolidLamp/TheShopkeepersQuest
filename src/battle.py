"""Handles the battles within the SHM Engine

Typical usage example:
    battle = BattleHandler(win, hook_dict, enemy, True)
    battle_result = battle.battle_handler()
"""

import curses
import math
import time
from collections.abc import Callable
from enum import IntEnum
from random import randrange as rand

from src import tui
from src.tui import print3
from src.typing import BattleHooks, BattleItem, Box, Enemy


class BattleHandler:
    """The handler for battles within the SHM Engine.

    Does not handle finding enemies, but only the battles themselves.

    Attributes:
        win (curses.window):
        A Curses window instance.

        hooks (BattleHooks):
        A dict in the BattleHooks format, which contains hooks.

        player_level (Box[int]):
        The player's level, in a Box (see box.py for more info).

        player_exp (Box[int]):
        The player's exp, in a Box (see box.py for more info).

        player_power (Box[int]):
        The player's power/damage, in a Box (see box.py for more info).

        player_health (Box[int]):
        The player's current health, in a Box (see box.py for more info).

        max_player_health (Box[int]):
        The player's maximum health, in a Box (see box.py for more info).

        get_money (Callable[[curses.window, int], None]):
        A hook provided by the gamefile, which is a function for getting money,
        which takes a curses window and an integer, and returns None.

        enemy (Enemy):
        The current enemy being encountered, in the Enemy TypedDict format.

        enemy_name (str):
        The enemy name, obtained from the enemy dict.

        is_boss (bool):
        If the enemy is a boss, obtained from the enemy dict.

        enemy_health (int):
        The health which the enemy currently has, from the enemy dict.

        max_enemy_health (int):
        The enemy's maximum health, obtained from the enemy dict.

        enemy_exp (int):
        The exp which the enemy yields, obtained from the enemy dict.

        money (int):
        The money which the enemy yields, obtained from the enemy dict.

        enemy_power (int):
        How much damage the enemy does, obtained from the enemy dict.

        run_chance (float):
        The chance which the player has of running, from the enemy dict.

        variable_damage (bool):
        Whether there is an RNG factor to damage, passed as parameter.

        battle_items (dict[str, BattleItem] | None):
        The dictionary of battle items which the gamefile has.

        player_items (list[str] | None):
        The list of items which the player has.

        level_up_xp (int | Box[int]):
        The amount of xp which the player must get to level up.

        power_increase (int | Box[int]):
        The increase in player's power upon level up.

        health_increase (int | Box[int]):
        The increase in player's health upon level up.

        in_fight (bool):
        Whether the fight has concluded or not.

        total_var (float):
        The total variance in the RNG factor if variable_damage is True.
    """

    def __init__(
        self,
        stdscr: curses.window,
        hook_dict: BattleHooks,
        enemy: Enemy,
        variable_damage: bool,
        battle_items: dict[str, BattleItem] | None = None,
        items: list[str] | None = None,
    ) -> None:
        """
        The handler for battles within the SHM Engine.
        Does not handle finding enemies, but only the battles themselves.

        Args:
            stdscr (curses.window):
            A curses window instance.

            hook_dict (BattleHooks):
            The dictionary containing the battle hooks from the gamefile.
            Must be in the dict format BattleHooks.

            enemy (Enemy):
            A dictionary representing the enemy to be encountered,
            in the Enemy TypedDict format.

            variable_damage (bool):
            A boolean value representing if there should be a partial RNG
            factor to damage.

            battle_items (dict[str, BattleItem] | None, optional):
            A dictionary representing all items which can be used in battles.
            The keys of the dictionary should be the name of the item.
            The values of the dictionary are BattleItem TypedDicts.
            Defaults to None.

            items (list[str] | None, optional):
            A list of items which the player has.
            Should be the exact inventory item list, not a copy.
            Defaults to None.
        """
        self.win: curses.window = stdscr

        # Setup hooks
        self.hooks: BattleHooks = hook_dict
        self.player_level: Box[int] = self.hooks["level_hook"]
        self.player_exp: Box[int] = self.hooks["exp_hook"]
        self.player_power: Box[int] = self.hooks["power_hook"]
        self.max_player_health: Box[int] = self.hooks["health_hook"]
        self.player_health: int = int(self.max_player_health)
        self.get_money: Callable[[curses.window, int], None]
        self.get_money = self.hooks["get_money_hook"]

        # Default values for enemies
        DEFAULT_NAME: str = "Default Enemy"
        DEFAULT_HEALTH: int = 100
        DEFAULT_EXP: int = 30
        DEFAULT_MONEY: int = 5
        DEFAULT_POWER: int = 50
        DEFAULT_RUN_CHANCE: float = 0.75

        # Unpack Enemy and setup enemy values
        self.enemy: Enemy = enemy
        self.enemy_name: str = self.enemy.get("name", DEFAULT_NAME)
        self.is_boss: bool = self.enemy.get("boss", False)
        self.enemy_health: int = self.enemy.get("health", DEFAULT_HEALTH)
        self.max_enemy_health: int = self.enemy.get("health", DEFAULT_HEALTH)
        self.enemy_exp: int = self.enemy.get("exp", DEFAULT_EXP)
        self.money: int = self.enemy.get("money", DEFAULT_MONEY)
        self.enemy_power: int = self.enemy.get("power", DEFAULT_POWER)
        self.run_chance: float = self.enemy.get("run_chance", DEFAULT_RUN_CHANCE)

        # Validate enemy values, and set to default values if invalid
        if not isinstance(self.enemy_name, str):
            self.enemy_name = DEFAULT_NAME
        if not isinstance(self.is_boss, (bool, int)):
            self.is_boss = False
        if not isinstance(self.enemy_health, int):
            self.enemy_health = DEFAULT_HEALTH
            self.max_enemy_health = DEFAULT_HEALTH
        if not isinstance(self.enemy_exp, int):
            self.enemy_exp = DEFAULT_EXP
        if not isinstance(self.money, int):
            self.money = DEFAULT_MONEY
        if not isinstance(self.enemy_power, int):
            self.enemy_power = DEFAULT_POWER
        if not isinstance(self.run_chance, (float, int)):
            self.run_chance = DEFAULT_RUN_CHANCE

        # Setup other parameters
        self.variable_damage: bool = variable_damage
        self.battle_items: dict[str, BattleItem] | None = battle_items
        self.player_items: list[str] | None = items

        # Setup important attributes which will be used by internal methods.
        self.level_up_xp: int | Box[int] = 0
        self.power_increase: int | Box[int] = 0
        self.health_increase: int | Box[int] = 0
        self.in_fight: bool = True
        self.total_var: float = 0.0

    def setup_level_up_stats(self) -> None:
        """Sets up the stats increase and requirements, from hooks."""
        POWER_INCREASE: int = 10
        HEALTH_INCREASE: int = 10
        LEVEL_UP_XP: int = 100

        if "level_up_xp" in self.hooks and isinstance(
            self.hooks["level_up_xp"], Callable
        ):
            self.level_up_xp = self.hooks["level_up_xp"]()
        elif "level_up_xp" in self.hooks and isinstance(
            self.hooks["level_up_xp"], (int, Box)
        ):
            self.level_up_xp = self.hooks["level_up_xp"]
        else:
            self.level_up_xp = LEVEL_UP_XP

        if "power_increase" in self.hooks and isinstance(
            self.hooks["power_increase"], Callable
        ):
            self.power_increase = self.hooks["power_increase"]()
        elif "power_increase" in self.hooks and isinstance(
            self.hooks["power_increase"], (int, Box)
        ):
            self.power_increase = self.hooks["power_increase"]
        else:
            self.power_increase = POWER_INCREASE

        if "health_increase" in self.hooks and isinstance(
            self.hooks["health_increase"], Callable
        ):
            self.health_increase = self.hooks["health_increase"]()
        elif "health_increase" in self.hooks and isinstance(
            self.hooks["health_increase"], (int, Box)
        ):
            self.health_increase = self.hooks["health_increase"]
        else:
            self.health_increase = HEALTH_INCREASE

    def battle_handler(self) -> bool:
        """Main battle handler, and should be called to start the battle.

        Returns:
            bool: If False, the battle was lost.
        """
        self.setup_level_up_stats()

        total_round: int = 0
        while self.player_health > 0 and self.enemy_health > 0 and self.in_fight:
            self.do_turn()
            total_round += 1
        if not self.in_fight:
            return True
        if self.player_health == 0 and self.enemy_health == 0:
            return True
        if self.player_health > 0:
            print3(self.win, text="\n\033[32mYou won!\033[0m")
            self.win.refresh()
            time.sleep(0.25)
            tui.print3(
                self.win, text=f"\n\033[32mYou gained {self.enemy_exp} EXP!\033[0m"
            )
            self.win.refresh()
            time.sleep(0.25)

            self.player_exp += self.enemy_exp
            while self.player_exp >= self.level_up_xp:
                self.player_level += 1
                self.player_exp -= self.level_up_xp
                self.player_power += self.power_increase
                self.player_health += self.health_increase
                print3(
                    self.win,
                    text="\n\033[32mYou leveled up!\n"
                    + f"Current level: {self.player_level}\033[0m",
                )
                self.win.refresh()
                self.setup_level_up_stats()
                time.sleep(0.25)
            avg_var: float = self.total_var / total_round
            gained_money: int = int(self.money * avg_var)
            if gained_money > 0:
                self.get_money(self.win, gained_money)
            self.win.refresh()
            time.sleep(0.75)
            return True
        else:
            return False

    def do_turn(self) -> None:
        """Completes one turn of the battle."""
        VARIANCE_DIVISOR: int = 10
        self.win.clear()
        text: str = self.create_hud()
        in_menu: bool = True
        if self.battle_items:
            options: list[str] = ["Fight", "Item", "Escape"]
            Options = IntEnum("Options", [("Fight", 0), ("Inventory", 1), ("Run", 2)])
        else:
            options: list[str] = ["Fight", "Escape"]
            Options = IntEnum("Options", [("Fight", 0), ("Inventory", 3), ("Run", 1)])
        while in_menu:
            query = "q"
            while not (isinstance(query, int)) and query != "i":
                query: int | str = tui.option(self.win, text, options)
            if query == "i" and self.battle_items:
                query = Options.Inventory
            elif query == "i" and not self.battle_items:
                continue

            if query == Options.Fight:
                variance: float = self.player_power / VARIANCE_DIVISOR
                abs_variance: int = rand(int(-1 * variance), int(variance))
                abs_variance = abs_variance if self.variable_damage else 0
                damage: int = self.player_power + abs_variance
                self.enemy_health -= damage
                self.win.clear()
                print3(self.win, "\n" + text, delay=0)
                print3(self.win, f"\nYou did {damage} damage to {self.enemy_name}!")
                self.win.refresh()
                time.sleep(0.25)
                in_menu = False
                break

            elif query == Options.Inventory and isinstance(self.battle_items, dict):
                if not self.player_items or len(self.player_items) == 0:
                    self.win.clear()
                    tui.option(
                        self.win,
                        text=f"{text}\nYou have no items available for battle!",
                        options=["Back"],
                    )
                    continue
                item = self.show_inventory(text)
                if not item:
                    continue
                if item in self.player_items:
                    self.player_items.remove(item)
                break
                items: set[str] = set(self.game_state.inventory.items)
                keyItems: set[str] = set(self.game_state.inventory.keyItems)
                player_items: set[str] = items | keyItems
                usables: set[str] = set(self.battle_items.keys()) & player_items
                in_menu = bool(len(usables))
                if not (in_menu):
                    print3(self.win, text="Your inventory is empty.")
                    time.sleep(0.35)
                    continue
                options: list[str] = list(usables)
                options.append("Back")
                while not (isinstance(query, int)) and query != "i":
                    query: int | str = tui.option(self.win, text, options)
                if query == "i":
                    query = len(options) - 1
                # self.battle_items[query]()

            elif query == Options.Run:
                if self.is_boss:
                    print3(self.win, text="\nYou cannot run from a boss!")
                    self.win.refresh()
                    time.sleep(0.25)
                    in_menu = True
                    continue

                length: int = len(str(float(self.run_chance))) - 2
                precision: int = int("1" + "0" * length)
                rng = rand(0, precision + 1) / precision

                if rng >= self.run_chance:
                    print3(self.win, text="\nYou couldn't get away!")
                    self.win.refresh()
                    time.sleep(0.25)
                    in_menu = False
                    break
                else:
                    print3(self.win, text="\nYou managed to get away!")
                    self.win.refresh()
                    time.sleep(0.65)
                    self.win.clear()
                    self.in_fight = False
                    return
            else:
                continue

        if self.enemy_health <= 0:
            return

        damage: int = self.enemy_power
        if self.enemy_power >= 20:
            variance: float = self.enemy_power / VARIANCE_DIVISOR
            abs_variance: int = rand(int(-1 * variance), int(variance))
            abs_variance = abs_variance if self.variable_damage else 0
            self.total_var += variance
            damage += rand(start=int(-1 * variance), stop=int(variance))
        self.player_health -= damage
        print3(self.win, f"\033[31m\n{self.enemy_name} did {damage} damage!\033[0m")
        self.win.refresh()
        time.sleep(0.45)
        return

    def create_hud(self) -> str:
        """Creates the HUD to display in the battle.

        Returns:
            str: The created HUD as a string.
        """
        get_hp_bar = lambda hp, maxhp: str("▊" * math.floor(hp / maxhp * 10))
        make_hud = lambda name, hp, maxhp, hpbar: f"{name}: {hp}/{maxhp}    {hpbar}"
        make_ui = lambda name, hp, maxhp: make_hud(
            name, hp, maxhp, hpbar=get_hp_bar(hp, maxhp)
        )

        player_name: str = f"You (Level {self.player_level})"
        enemy_hud = make_ui(self.enemy_name, self.enemy_health, self.max_enemy_health)
        player_hud = make_ui(player_name, self.player_health, self.max_player_health)

        text: str = f"{enemy_hud}\n\n{player_hud}\n"
        return text

    def show_inventory(self, text: str) -> str | None:
        """Handles the inventory.

        Args:
            text (str): The HUD to display.

        Returns:
            str | None:
            Either the string representing the item chosen;
            or None, representing no chosen item and the player backs out.
        """
        if not self.battle_items or not self.player_items:
            return

        items: set[str] = set(self.player_items) & set(self.battle_items.keys())
        options: list[str] = list(items)
        options.append("Back")
        query = "a"
        while not (isinstance(query, int)) and query != "i" and query != "q":
            query: int | str = tui.option(self.win, text, options)
        if query == "i" or query == "q":
            query = len(options) - 1

        if query == len(options) - 1:
            return

        chosen_item: str = options[query]

        if chosen_item == "Back":
            return

        return chosen_item

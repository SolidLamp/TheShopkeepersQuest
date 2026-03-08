Room Format
~~~~~~~~~~~


Preamble
========
This document describes the format used for a room within the SHM Engine.

For the format used for the full room dict, please see gamefile_format.rst.


Quick Reference Table
=====================

+-----------------------+--------------------+---------------------------------+
| Room Attribute        | Type               | Description                     |
+=======================+====================+=================================+
| Text                  | str                | A string which is printed while |
|                       |                    | the user is within the room.    |
+-----------------------+--------------------+---------------------------------+
| Requirements          | Callable[[], bool] | If True, 'Text' is printed; if  |
|                       |                    | False, 'AlternateText' is       |
|                       |                    | printed.                        |
+-----------------------+--------------------+---------------------------------+
| AlternateText         | str                | A string which is printed while |
|                       |                    | the user is within the room     |
|                       |                    | when Requirements returns False |
+-----------------------+--------------------+---------------------------------+
| TextSpeed             | float              | Value for the delay between     |
|                       |                    | characters being printed within |
|                       |                    | a given room.                   |
+-----------------------+--------------------+---------------------------------+
| Desc                  | str                | A (very) short description of   |
|                       |                    | the room.                       |
+-----------------------+--------------------+---------------------------------+
| titlebarCentre        | str                | The string in the titlebar      |
|                       |                    | centre whilst in the room.      |
+-----------------------+--------------------+---------------------------------+
| titlebarLeft          | str                | The string on the left of the   |
|                       |                    | titlebar  whilst in the room.   |
+-----------------------+--------------------+---------------------------------+
| titlebarRight         | str                | The string on the right of      |
|                       |                    | titlebar whilst in the room.    |
+-----------------------+--------------------+---------------------------------+
| Script                | Callable[[], None] | Executed if present.            |
+-----------------------+--------------------+---------------------------------+
| Item                  | str                | The item the player will        |
|                       |                    | receive.                        |
+-----------------------+--------------------+---------------------------------+
| ItemRequirements      | Callable[[], bool] | If True, the player gets the    |
|                       |                    | item; otherwise, the player     |
|                       |                    | gets no item.                   |
+-----------------------+--------------------+---------------------------------+
| ItemText              | str                | The string printed when the     |
|                       |                    | user receives the item in this  |
|                       |                    | room.                           |
+-----------------------+--------------------+---------------------------------+
| KeyItem               | str                | Alias for 'Item'.               |
+-----------------------+--------------------+---------------------------------+
| KeyItemRequirements   | Callable[[], bool] | Alias for 'ItemRequirements'.   |
+-----------------------+--------------------+---------------------------------+
| KeyItemText           | str                | Alias for 'ItemText'.           |
+-----------------------+--------------------+---------------------------------+
| Options               | list[str]          | A list of the text options      |
|                       |                    | available to the player, in the |
|                       |                    | same positions as 'Move'.       |
+-----------------------+--------------------+---------------------------------+
| Option[#]Requirements | Callable[[], bool] | Where '[#]' represents an       |
|                       |                    | integer, this applies to        |
|                       |                    | whichever option is at that     |
|                       |                    | position in 'Options'. If True, |
|                       |                    | the options displays as         |
|                       |                    | default; otherwise, that option |
|                       |                    | is hidden from the player.      |
+-----------------------+--------------------+---------------------------------+
| Inventory             | bool               | Whether the inventory should be |
|                       |                    | accessible from within that     |
|                       |                    | room; True if not present.      |
+-----------------------+--------------------+---------------------------------+
| Move                  | list[int]          | In the same order as 'Options'. |
|                       |                    | Every option moves you to the   |
|                       |                    | room ID in the same position    |
|                       |                    | within this list.               |
+-----------------------+--------------------+---------------------------------+
| Automove              | int                | A room ID to automatically move |
|                       |                    | to, without an option dialogue. |
+-----------------------+--------------------+---------------------------------+
| InstantAutomove       | bool               | Whether there should be a delay |
|                       |                    | for 'Automove' or not; treated  |
|                       |                    | as True if not present.         |
+-----------------------+--------------------+---------------------------------+
| Lose                  | str                | If present in the room, the     |
|                       |                    | player loses and the string     |
|                       |                    | message is received by the lose |
|                       |                    | function.                       |
+-----------------------+--------------------+---------------------------------+
| Ending                | str                | If present in the room, the     |
|                       |                    | player finishes the game and    |
|                       |                    | the string message is received  |
|                       |                    | by the ending function.         |
+-----------------------+--------------------+---------------------------------+


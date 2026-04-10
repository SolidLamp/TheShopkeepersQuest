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
|                       |                    | gets no item. If not present,   |
|                       |                    | acts as True.                   |
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
| ShopItems             | list[str]          | Defines the list of items sold  |
|                       |                    | within a shop in this room.     |
+-----------------------+--------------------+---------------------------------+
| ShopItemCosts         | list[int]          | The list of costs for items     |
|                       |                    | within the shop. Indexes        |
|                       |                    | correspond to ShopItems, and    |
|                       |                    | both lists should always be the |
|                       |                    | same length.                    |
+-----------------------+--------------------+---------------------------------+
| ShopItemMove          | list[int |         | The room to move to if the item |
|                       |   tuple[str, int]] | is purchased. Indexes always    |
|                       |                    | correspond to ShopItems, and    |
|                       |                    | both lists should always be the |
|                       |                    | same length. To disable, set to |
|                       |                    | -1, as such a room would        |
|                       |                    | correspond to the current room, |
|                       |                    | and thus would not do anything  |
|                       |                    | regardless.                     |
+-----------------------+--------------------+---------------------------------+
| ShopEntrance          | str | list[str]    | The string to display when      |
|                       |                    | entering the shop. If it is a   |
|                       |                    | list of strings, then the       |
|                       |                    | string to display will be       |
|                       |                    | randomly chosen from the list.  |
+-----------------------+--------------------+---------------------------------+
| ShopExit              | str | list[str]    | The string to display when      |
|                       |                    | exiting the shop. If it is a    |
|                       |                    | list of strings, then the       |
|                       |                    | string to display will be       |
|                       |                    | randomly chosen from the list.  |
+-----------------------+--------------------+---------------------------------+
| BattleText            | str                | The string to display when      |
|                       |                    | a battle initiates. Not         |
|                       |                    | required for a battle, but      |
|                       |                    | recommended.                    |
+-----------------------+--------------------+---------------------------------+
| Enemies               | list[int | str]    | A list of identifiers,          |
|                       |                    | corresponding to the identifier |
|                       |                    | of an enemy given by the        |
|                       |                    | enemies dict in the gamefile.   |
+-----------------------+--------------------+---------------------------------+
| EnemyChances          | list[float | int]  | A list of chances for an enemy  |
|                       |                    | to appear, with each chance     |
|                       |                    | corresponding to the enemy with |
|                       |                    | the index within the Enemies    |
|                       |                    | list. If the sum of chances in  |
|                       |                    | the list is less than 1, then   |
|                       |                    | the float values is the exact   |
|                       |                    | chance of an enemy appearing.   |
|                       |                    | However, if the sum of chances  |
|                       |                    | is greater than 1, then an      |
|                       |                    | enemy is guaranteed to appear,  |
|                       |                    | and it the chances are          |
|                       |                    | calculated by the sum of total  |
|                       |                    | chances, finding the multiplier |
|                       |                    | to get to 1, and multiplying    |
|                       |                    | each chance by this multiplier. |
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
| Move                  | list[int |         | In the same order as 'Options'. |
|                       |   tuple[str, int]] | Every option moves you to the   |
|                       |                    | room ID in the same position    |
|                       |                    | within this list.               |
|                       |                    |                                 |
|                       |                    | Also see `Room ID Format`_      |
+-----------------------+--------------------+---------------------------------+
| Automove              | int |              | A room ID to automatically move |
|                       |   tuple[str, int]] | to, without an option dialogue. |
|                       |                    |                                 |
|                       |                    | Also see `Room ID Format`_      |
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


Room ID Format
==============
Room IDs are usually represented by the int ``x``, where x represents the room 
with ID x.
An ID can also dynamically refer to a previous room that the user has visited, 
by using a negative ID. For example, the ID ``-x`` will refer to the room that 
the user was in x rooms ago.

*Note that the current room the user is within is also considered within these 
calculations - the ID ``-1`` will refer to the current room.*

*Also note that saving and loading a file will change the list of 
previously-visited rooms. This is by adding the room the user saved in to the 
list of previously-visited rooms. This will make it appear twice.
For this reason, it is not recommended to use negative IDs within rooms with 
multiple connections. As the user cannot save and quit within a room with 
Automove, you can ensure expected behaviour in such a scenario.*

Negative IDs can also be represented in the older form ``("history", -x)``, 
which will refer to the room that the user was in x rooms ago.
This form was the only negative ID form which was only available prior to 
SHM 1.2. This form is not recommened and the modern negative ID system 
should be used over this older system in all possible situations.

However, developers should be familar with this older system to know that 
the ID ``("history", -x)`` is equivalent to ``-x`` - the former should be 
converted to the latter when touching up a gamefile. 

You can also check for this older system and invalid room IDs in the Debug 
Menu, with the option ``Test room IDs``. The Debug Menu is triggered by 
pressing 'D' within a room.

The format of save files for SHM Engine games
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Preamble
========
The SHM Engine, from 1.2, produces save files which allow the player to save
their progress and continue from a given point. To achieve this, data must be
written in a format which can be easily exchanged and understood by the
engine.

For this purpose, the SHM Engine stores all save files in JSON format, as it
is a common format, with standard library support in Python. This document
outlines the structure of the save file, including what possible keys and
values will be found within a usual save file.

The most important value is the 'version' key, as versions may add keys (or
potentially remove them) - in order to understand what keys are available, the
version must be considered.

This document provides a table, with a list of all keys, what they contain,
and how they are used.

Format
======

+--------------+----------------------+--------------------+-----------------+
| Key          | Type                 | Version Introduced | Description     |
+--------------+----------------------+--------------------+-----------------+
| Game         | string               | 1                  | The name of the |
|              |                      |                    | game which the  |
|              |                      |                    | save file is    |
|              |                      |                    | used for.       |
+--------------+----------------------+--------------------+-----------------+
| Saved        | string               | 1                  | When the game   |
|              |                      |                    | was last saved, |
|              |                      |                    | in ISO format.  |
+--------------+----------------------+--------------------+-----------------+
| save_version | number               | 1                  | The version of  |
|              |                      |                    | the save file.  |
+--------------+----------------------+--------------------+-----------------+
| RoomID       | number               | 1                  | The room ID     |
|              |                      |                    | where the game  |
|              |                      |                    | was saved, and  |
|              |                      |                    | where the       |
|              |                      |                    | player should   |
|              |                      |                    | continue from.  |
+--------------+----------------------+--------------------+-----------------+
| History      | number[]             | 1                  | An array of     |
|              |                      |                    | room IDs,       |
|              |                      |                    | representing    |
|              |                      |                    | the previous    |
|              |                      |                    | rooms visited   |
|              |                      |                    | by the player.  |
+--------------+----------------------+--------------------+-----------------+
| shop_exit    | number               | 2                  | If the player   |
|              |                      |                    | is within the   |
|              |                      |                    | room, the room  |
|              |                      |                    | where the       |
|              |                      |                    | player should   |
|              |                      |                    | exit from.      |
+--------------+----------------------+--------------------+-----------------+
| game_state   | Object               | 1                  | The game state. |
|              |                      |                    | Game-specific.  |
+--------------+----------------------+--------------------+-----------------+
| inventory    | { string: number[] } | 1                  | An object of    |
|              |                      |                    | string keys and |
|              |                      |                    | values of       |
|              |                      |                    | arrays of       |
|              |                      |                    | numbers.        |
+--------------+----------------------+--------------------+-----------------+
| game_id      | string               | 1                  | The UUID of the |
|              |                      |                    | game.           |
+--------------+----------------------+--------------------+-----------------+
| save_id      | string               | 1                  | A randomly      |
|              |                      |                    | generated UUID  |
|              |                      |                    | of this         |
|              |                      |                    | specific save   |
|              |                      |                    | file.           |
+--------------+----------------------+--------------------+-----------------+
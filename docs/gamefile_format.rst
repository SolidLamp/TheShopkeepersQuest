The format of gamefiles in the SHM Engine
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Preamble
========
Gamefiles in the SHM Engine are Python files which contain the assets of the
game itself, which are called by the engine.

They may also be supplemented by other files in addition, such as TOML files,
which include additional game content.


Required
========
Every gamefile MUST include the following attributes (publicly accessible 
identifier that is located within a gamefile):

+---------------+-----------+-------------------------------------------------+
| Attribute     | Class     | Overview                                        |
+===============+===========+=================================================+
| gameInfo      | dict      | The information and settings of the game.       |
+---------------+-----------+-------------------------------------------------+
| history       | list[int] | Used as a list of the last 10 rooms visited.    |
+---------------+-----------+-------------------------------------------------+
| defaultEnding | str       | String printed upon an ending of the game.      |
+---------------+-----------+-------------------------------------------------+
| defaultLose   | str       | String printing upon losing a game.             |
+---------------+-----------+-------------------------------------------------+
| game_state    | Custom    | Uses a game-specific class and uses attributes. |
+---------------+-----------+-------------------------------------------------+
| get_rooms     | Callable  | A function which returns a dict of rooms.       |
+---------------+-----------+-------------------------------------------------+

*(Note that within Python, 'Callable' refers to a function, or any object which
can be called.)*


gameInfo
--------
gameInfo is used to store the identifiers of the game as well as the settings 
of the game. It is used to define the game's title, as well as many other 
fields. The following table has all expected values within gameInfo:

+-------------------------+-------+-----------+-------------------------------+
| Field                   | Class | Required? | Overview                      |
+=========================+=======+===========+===============================+
| Name                    | str   | Yes       | Name of the game              |
+-------------------------+-------+-----------+-------------------------------+
| Version                 | str   | Yes       | String representation of the  |
|                         |       |           | game version (e.g. "1.3.0")   |
+-------------------------+-------+-----------+-------------------------------+
| ReleaseDate             | str   | Yes       | Version string, e.g. "v1.3.0" |
+-------------------------+-------+-----------+-------------------------------+
| Licence                 | str   | Yes       | String representation of  the |
|                         |       |           | game's licence.               |
+-------------------------+-------+-----------+-------------------------------+
| Creator                 | str   | Yes       | The creator's name.           |
+-------------------------+-------+-----------+-------------------------------+
| Link                    | str   | Yes       | Link to the game's homepage.  |
+-------------------------+-------+-----------+-------------------------------+
| game_id                 | str   | No        | A UUID string, used to        |
|                         |       |           | distinguish the game.         |
+-------------------------+-------+-----------+-------------------------------+
| complevel               | int   | Yes       | Which API version the game    |
|                         |       |           | is designed for. (1.2 = 2)    |
+-------------------------+-------+-----------+-------------------------------+
| abbr                    | str   | Yes       | A short abbreviation of the   |
|                         |       |           | game title. e.g. "TSQ"        |
+-------------------------+-------+-----------+-------------------------------+
| title                   | str   | Yes       | Title of the game             |
+-------------------------+-------+-----------+-------------------------------+
| desc                    | str   | Yes       | A description of the game.    |
+-------------------------+-------+-----------+-------------------------------+
| starting_room           | int   | Yes       | The ID of the room where the  |
|                         |       |           | game should start.            |
+-------------------------+-------+-----------+-------------------------------+
| default_titlebar_left   | str   | No        | The default left string on    |
|                         |       |           | the titlebar.                 |
+-------------------------+-------+-----------+-------------------------------+
| default_titlebar_centre | str   | No        | The default right string on   |
|                         |       |           | the titlebar.                 |
+-------------------------+-------+-----------+-------------------------------+
| default_titlebar_right  | str   | No        | The default centre string on  |
|                         |       |           | the titlebar.                 |
+-------------------------+-------+-----------+-------------------------------+
| default_textspeed       | float | No        | The default delay between     |
|                         |       |           | characters being printed.     |
+-------------------------+-------+-----------+-------------------------------+
| border_style            | int   | No        | The style of border used for  |
|                         |       |           | the game. (Usually omitted)   |
+-------------------------+-------+-----------+-------------------------------+


history
-------
``history`` is a list. It should be initialised to an empty list. It is used to
store the visited rooms as ints while the game is running.

The gamefile only requires only the line:

``history = []``

No other code is required to be present.


defaultEnding
-------------
``defaultEnding`` is a string. It is printed whenever the user gets an ending
to the game. If ``endingText`` is present (see `Optional`_) and the ending is
not within the dict, then only the ``defaultEnding`` is printed. If present,
both its specific string and ``defaultEnding`` will be printed.

Within the string, "|" can be used to represent the ending name.
For example, if the user received the "Test" Ending, and the value of 
``defaultEnding`` is "You achieved the\\n|\\nEnding.\\nTry Again?", then it will 
be formatted and printed to the user as following:

| You achieved the
| Test
| Ending.
| Try Again?


defaultLose
-----------
``defaultLose`` is a string. It is printed whenever the user loses the game, 
through the room containing the ``Lose`` attribute. If ``loseText`` is
present (see `Optional`_) and the specific loss is not present within that
dict, then only the ``defaultLose`` is printed. If present, both its specific 
string present within the dict and ``defaultLose`` will be printed.
Within the string, ``"|"`` can be used to represent the ending name.

For example, if a room contained ``Lose`` with a value of ``"Test"``, and the 
value of ``defaultLose`` is ``"\nYou died!\n'|'"``, then it will be formatted and 
printed to the user as follows:

| 
| You died!
| 'Test'
|  


game_state
----------
``game_state`` is used to store most of the game's given state while the game 
is running.

It must be based upon a class which the gamefile defines and instatiates to 
create the ``game_state`` object. Attributes are game specific, and only 
affected by game scripts.

Only requirement is that ``game_state`` has the magic method ``__dict__`` 
available; it must not be replaced or disabled.


get_rooms
---------
``get_rooms`` is a function within the gamefile which returns the dictionary 
of rooms [1]_.

It should take one parameter, being ``curses.window`` and return a single dict.

This dictionary should be in the format dict[int, Room], where Room is the 
format of a room [1]_. There are no defined rules on how ``get_rooms`` must 
function internally - the following configuration is recommened for SHM 1.2, 
where TOML can be used: 

* An internal variable named ``rooms``, read from a TOML file containing 
  the static content of a given room [1]_.
* A second dict, ``room_scripts`` contains the Callable content and scripts 
  for all rooms.
* Every room present in both dicts have the contents of ``room_scripts`` 
  copied to ``rooms``, and ``rooms`` is then returned.
* The following code snippet can be used:
  
  | ``for key in filter(lambda key: key in rooms.keys(), extrarooms.keys()):``
  |     ``new_rooms[key].update(extrarooms[key])``

.. rubric:: Footnotes

.. [1] For the format used of individual rooms, see room_format.rst.


Optional
========
Every gamefile CAN include the following attributes:

+---------------+-----------+-------------------------------------------------+
| Attribute     | Class     | Overview                                        |
+===============+===========+=================================================+
| endingText    | dict      | String printed upon an ending of the game.      |
+---------------+-----------+-------------------------------------------------+
| loseText      | dict      | String printing upon losing a game.             |
+---------------+-----------+-------------------------------------------------+
| keyItems      | list[str] | List of items which are key items in the game.  |
+---------------+-----------+-------------------------------------------------+



The Shopkeeper Quest current configuration
==========================================
The gamefile for The Shopkeeper's Quest is stored within ``src/game.py``. 
The gamefile also calls ``src/game.toml``, where most of the non-script 
content (e.g. static room attributes) is stored.

Generally, any static game content should be stored within ``src/game.toml``, 
and any callable scripts, as well as the game_state setup should be stored
within ``src/game.py``, as Python is required.

In text, escape characters should be represented by ``\x`` within
``src/game.py``, and as ``\\x`` within ``game.toml``.


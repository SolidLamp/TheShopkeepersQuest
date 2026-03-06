Contributing to the SHM Engine and games which implement it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Code Style
==========
The style for Python code within the SHM Engine and games which implement it
should be as follows:

* Match general Python style recommendations (PEP 8, etc.)
* Should be formatted using the Black formatter on default settings.

  * This includes the 88-line default.
  * Exceptions to this are possible, such as the list of characters
    within tui.py, which is a list of the final byte within a CSI code,
    as the list is automatically formatted to one character per line.
  * The general rule is that if the code looks awful when formatted,
    put ``fmt: off`` and ``fmt: on`` around it. Otherwise, don't.
  * Line count should never be considered to be an exception.

* Functions should be written with docstings provided.
* All functions should use type hinting (See PEP 484 for more details).


Commit Styling
==============
Commits to a given repository should stick to a consistent style.
The recommended style includes prefixing a tag within square brackets
which represents the category of commit.

The following commit message is provided as an example:
``[Enhancement] Improved control character support in print3 and modularised
escape sequence code``
(This is commit dbf854d of The Shopkeeper's Quest)

The following categories of commit are recommended:

* [Bug Fix] - represents a commit which fixes unintended behaviour within the
  engine or game.
* [Documentation] - represents a commit which only affects the documentation - 
  not the code.
* [Enhancement] - represents an improvement to the engine which does not affect
  how the engine interacts with the game or any exposed functions.
  e.g. the introduction of UUIDs to save files, which only affects engine-side.
* [Feature] - represents a commit where a new feature is introduced to the
  engine which affects how the engine interacts with the game.
  e.g. the introduction of KeyItem as a new room attribute.
* [Game] - represents a commit which primarily introduces alterations to the
  gamefile and has little effect on the code of the SHM Engine.
* [Refactor] - represents a commit which does not change the logic of the game
  or the SHM Engine, only clearing up code, writing new doc strings, and
  improving code style.

*Note that the distinction between Enhancement and Feature is often blurred.
Generally, a new room attribute or API are considered to be a Feature.
Those that do not affect the API and do not require new docs are Enhancements*

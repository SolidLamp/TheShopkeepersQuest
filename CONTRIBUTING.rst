Contributing to the SHM Engine and games which implement it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Code Style
==========
The style for Python code within the SHM Engine and games which implement it
should be as follows:

* Code should match general Python style recommendations (see `PEP 8`_, etc.).
* Any new parameter names introduced in a given commit should be provided in
  snake_case.

  * Parameter names that do not use snake_case should be changed if they were
    introduced within the same development cycle/branch.
  * If the parameters have been present since at least the last stable release,
    they should not be changed as to preserve compatibility with existing code.

* Nesting should not be excessive - excluding nesting due to code being within
  a class, nesting should be minimised.

   * General rule: if you have to scroll horizontally to focus on the code,
     it's too much nesting.

* Class definitions should not be nested within each other, as it makes code
  complicated and difficult to read.
* git clone Code should be formatted using the `Black`_ formatter on default settings.

  * This includes the 88-line default.
  * Exceptions to this are possible, such as the list of characters
    within tui.py, which is a list of the final byte within a CSI code,
    as the list is automatically formatted to one character per line.
  * The general rule is that if the code looks awful when formatted,
    put ``fmt: off`` and ``fmt: on`` around it. Otherwise, just don't.
  * Even when an exception to using Black is made, the line count should still
    be capped at 88 - line count should not be considered significant enough
    to warrant an exception to formatting rules.
  * Remember the following guideline from `PEP 8`_:
    
      "In particular: do not break backwards compatibility just to comply with
      this PEP!

      Some other good reasons to ignore a particular guideline:

      1. When applying the guideline would make the code less readable, even
      for someone who is used to reading code that follows this PEP.

      2. To be consistent with surrounding code that also breaks it (maybe for
      historic reasons) – although this is also an opportunity to clean up
      someone else’s mess (in true XP style)."
    
      -- Python Enhancement Proposals, `PEP 8`_

* Any function added or modified to have new functionality should have a
  docstring provided (see `PEP 257`_).
* All functions should include function annotations wherever possible (see
  `PEP 484`_).
* All class attributes should include variable annotations, but variables
  within individual functions do not require this.
* Avoid implicit string concatenation in most cases, except on assignment of 
  the string to a variable without operators.
* Return statements should have redundant parentheses.
* Docstrings should within the format created by autoDocstring

  * Whenever a given argument requires multiple lines, all arguments should
    be seperated by line, and the default value should also be provided on 
    a new line.
  * Docstrings should have the triple quotes (``"""``) on seperate lines from 
    the docstring itself.


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

+---------------+-------------------------------------------------------------+
| Tag           | Explanation                                                 |
+===============+=============================================================+
| Bug Fix       | Represents a commit which fixes unintended behaviour        |
|               | within the engine or game.                                  |
+---------------+-------------------------------------------------------------+
| Documentation | Represents a commit which only affects the documentation -  |
|               | not the code.                                               |
+---------------+-------------------------------------------------------------+
| Enhancement   | An improvement to the engine which does not affect          |
|               | how the engine interacts with the game or any exposed       |
|               | functions.                                                  |
|               | e.g. the introduction of UUIDs to save files, which only    |
|               | affects engine-side.                                        |
+---------------+-------------------------------------------------------------+
| Feature       | The introduction of a new feature to the engine which       |
|               | affects how the engine interacts with the game.             |
|               | e.g. the introduction of KeyItem as a new room attribute.   |
+---------------+-------------------------------------------------------------+
| Game          | Primarily introduces alterations to the gamefile and has    |
|               | little effect on the code of the SHM Engine.                |
+---------------+-------------------------------------------------------------+
| Refactor      | A commit which does not change the logic of the game or the |
|               | or the SHM Engine, being limited to only code clean up and  |
|               | styling fixes.                                              |
+---------------+-------------------------------------------------------------+

*Note that the distinction between Enhancement and Feature is often blurred.
Generally, a new room attribute or API are considered to be a Feature.
Those that do not affect the API and do not require new docs are Enhancements*


See Also
--------
* `PEP 7`_
* `PEP 8`_
* `PEP 257`_
* `PEP 484`_
* `Black`_


.. _Black: https://github.com/psf/black
.. _PEP 7: https://peps.python.org/pep-0007/
.. _PEP 8: https://peps.python.org/pep-0008/
.. _PEP 257: https://peps.python.org/pep-0257/
.. _PEP 484: https://peps.python.org/pep-0484/


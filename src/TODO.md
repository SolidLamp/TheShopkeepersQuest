[ ] Saving (toml? xml? json? maybe use toml as already used in project, but call .sav. wait no we need to write and toml not supported so probably go with json)
[ ] Titlebar
[ ] Centre choices
[ ] Fix the text code parser for \033[52;43m or whatever, and don't override bg and fg colour when the other is changed (make more configurable?)
[ ] Import game from other locations and names - put inside class

## Saving structure
- Title
- Date
- game.game_state.__dict__

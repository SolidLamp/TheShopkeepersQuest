import os.path
import sys

try:
    import curses
except ImportError as e:
    print(
        f"The curses module was not found. If you are running Windows, please install windows-curses with pip.\nError: {e}"
    )
    sys.exit(1)
import engine_info
import save_handler
import shm
import tui


def main(win):
    curses.curs_set(0)
    win.scrollok(True)
    win.nodelay(True)
    tui.colorsetup(win)
    curses.cbreak()
    engineInfo = engine_info.get()
    tui.draw_titlebar(win, engineInfo)
    padding = 1
    padx1 = 0
    padx2 = 0
    pady1 = 0
    pady2 = 1
    newwin = tui.create_newwin(win, padding, padx1, padx2, pady1, pady2)
    theString = (
        "\033[36m"
        r"""
        ___ _  _ ____
         |  |__| |___
         |  |  | |___

        ____ _  _ ____ ___  _  _ ____ ____ ___  ____ ____ ____ '
        [__  |__| |  | |__] |_/  |___ |___ |__] |___ |__/ [__
        ___] |  | |__| |    | \_ |___ |___ |    |___ |  \ ___]

                               ____ _  _ ____ ____ ___
                               |  | |  | |___ [__   |
                               |_\| |__| |___ ___]  |
                                                       """
        "\033[0m"
    )
    options = [
        "Play The Shopkeeper's Quest",
        "Play The Shopkeeper's Quest [Skip Intro]",
        "Load Save",
        "Quit",
    ]
    savedGame = os.path.exists("game.sav")
    if not savedGame:
        options.pop(2)
    query = tui.option(
        newwin,
        "\033[36m\n___ _  _ ____\n |  |__| |___ \n |  |  | |___ \n\n"
        "____ _  _ ____ ___  _  _ ____ ____ ___  ____ ____ ____ '\n"
        "[__  |__| |  | |__] |_/  |___ |___ |__] |___ |__/ [__  \n"
        "___] |  | |__| |    | \_ |___ |___ |    |___ |  \ ___] \n"
        "\n                       ____ _  _ ____ ____ ___ \n"
        "                       |  | |  | |___ [__   |  \n"
        "                       |_\| |__| |___ ___]  |  \n"
        "                                               \033[0m",
        options,
    )
    newwin.clear()
    win.clear()
    win.move(0, 0)
    curses.curs_set(0)
    tui.draw_titlebar(win, engineInfo)
    # example: plan
    # Play The Shopkeeper's Quest
    # --
    # Save 1 -- Last Saved: 2026-02-06
    # Save 2 -- No Data
    # Save 3 -- Error Parsing Save
    # Back
    # --
    # Settings
    # Quit
    if query == 0:
        tui.draw_titlebar(win, "The Shopkeeper's Quest")
        tui.print3(
            newwin,
            "You are a travelling merchant, approaching a new village to sell your wares in another region.\nAs you approach the village, the atmosphere seems odd and eerily silent, almost frightening in a way. \nSuddently, a man appears, and walks in your direction.\nThe man speaks, \033[33m'Greetings. I'm a local shopkeeper, just on the outskirts of our little village.\nMany come for my high-quality wares, but none have done such today, for a mystical spell has bewitched them.\nAny that resided within the main parts of the village limits last night have disappeared.'\033[0m\nThe man grunts and scratches his chin.\nHe looks back at the village with a longing expression, before turning his gaze back to you. \n\033[33m'It worries me, you know?'\033[0m he continues, \033[33m'There's an old legend that if all seems to disappear overnight, then it marks a dark path for the world.'\033[0m\nThe man sighs deeply, and waits a moment before speaking again, \033[33m'I do have some experience with magic.\nI can reverse it, but I need 3 mystical items; the first, a rusted sword; the second, an amber necklace; and the third, a golden idol.\nWith those three items, I believe I can bring everything back to normal.\nI would get them myself, but my adventuring days are behind me.\nIf it helps, I believe the bazaar was unaffected - it, too, was beyond the main limits of the village.\nWhen you obtain the items, come see me in my shop.\nI shall be seeing you, then.'\033[0m\nThe man leaves.\nPress any key to continue...",
            delay=0.02,
        )
        newwin.refresh()
        win.refresh()
        curses.flushinp()
        win.getch()
    elif (query == 3 and savedGame) or isinstance(query, str):
        sys.exit()
    if query == 2 and os.path.exists("debugSave.sav"):
        saveFile = save_handler.read_save("debugSave")
        shm.run(
            win,
            0,
            saveFile,
            gameFile_name="game",
            gameFile_path="./",
            saveFileName="debugSave",
        )
    else:
        shm.run(
            win, starting_room=(query + 1), gameFile_name="game", gameFile_path="./"
        )
    sys.exit()


def title():
    print("[The Shopkeeper's Quest]")
    while 1:
        curses.wrapper(main)

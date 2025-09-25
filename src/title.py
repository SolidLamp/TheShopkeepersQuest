import curses
import time
import sys
import tui
from shm import gameLoop
from shm import print2
from shm import option

def main(win):
    win.clear()
    curses.curs_set(0)
    win.scrollok(True)
    curses.start_color() #curses.A_NORMAL | curses.A_BOLD
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    query = tui.option(win,r"""
___ _  _ ____
 |  |__| |___
 |  |  | |___

____ _  _ ____ ___  _  _ ____ ____ ___  ____ ____ ____ '
[__  |__| |  | |__] |_/  |___ |___ |__] |___ |__/ [__
___] |  | |__| |    | \_ |___ |___ |    |___ |  \ ___]

                       ____ _  _ ____ ____ ___
                       |  | |  | |___ [__   |
                       |_\| |__| |___ ___]  |
                                               """,["Begin", "Skip Intro", "Quit"])
    win.clear()
    win.move(0,0)
    curses.curs_set(0)
    if query == 0:
        tui.print3(win, "You are a travelling merchant, approaching a new village to sell your wares in another region.\nAs you approach the village, the atmosphere seems odd and eerily silent, almost frightening in a way. \nSuddently, a man appears, and walks in your direction.\nThe man speaks, \033[33m'Greetings. I'm a local shopkeeper, just on the outskirts of our little village.\nMany come for my high-quality wares, but none have done such today, for a mystical spell has bewitched them..\nAny that resided within the main parts of the village limits last night have disappeared.'\033[0m\nThe man grunts and scratches his chin.\nHe looks back at the village with a longing expression, before turning his gaze back to you. \n\033[33m'It worries me, you know?'\033[0m he continues, \033[33m'There's an old legend that if all seems to disappear overnight, then it marks a dark path for the world.'\033[0m\nThe man sighs deeply, and waits a moment before speaking again, \033[33m'I do have some experience with magic.\nI can reverse it, but I need 3 mystical items; the first, a rusted sword; the second, an amber necklace; and the third, a golden idol.\nWith those three items, I believe I can bring everything back to normal.\nI would get them myself, but my adventuring days are behind me.\nIf it helps, I believe the bazaar was unaffected - it, too, was beyond the main limits of the village.\nWhen you obtain the items, come see me in my shop.\nI shall be seeing you, then.'\033[0m")
        win.refresh()
        win.getch()
        gameLoop(1)
    if query == 1:
        gameLoop(2)
    else:
        sys.exit()

    #while True:
        #gameLoop()

def title():
    print("If you can read this, the game is not displaying. The most likely scenario is that you have closed the game.")
    curses.wrapper(main)

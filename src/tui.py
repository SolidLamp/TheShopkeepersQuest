import curses
import math
import os
import sys
import time

_TAB_SIZE = 4

_ENDBYTE_CHARS = [
    "@",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "[",
    "\\",
    "]",
    "^",
    "_",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "{",
    "|",
    "}",
    "~",
]

# 2097152


def colorsetup(win):
    curses.start_color()  # curses.A_NORMAL | curses.A_BOLD
    curses.use_default_colors()
    curses._use_ansi_colors = True
    curses.init_pair(31, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(32, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(33, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(34, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(35, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(36, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(37, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(41, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(42, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(43, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(44, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(45, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(46, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(47, curses.COLOR_BLACK, curses.COLOR_WHITE)


def _ESCtoRGB(ESC: str | int):
    """
    Takes a 8-bit colour escape code, as a string or integer.
    Returns three ints: r, g, b, representing a 24-bit RGB value.
    """
    ESC = int(ESC)
    r = (ESC - 16) // 36
    b = (ESC - 16) % 6
    g = ((ESC - 16) % 36) // 6
    return (r, g, b)


def print3(
    win: curses.window,
    text: str,
    colorcode: int = 0,
    delay: float = 0.01,
    pauseAtNewline: float = 0.0,
    speedUp: bool = True,
) -> None:
    r"""Function to print string `text` to the provided curses window using a
    typewriter effect. Also handles control and escape codes.

    Supported control characters:
    - `\f` - clear the window
    - `\n` - start a new line
    - `\r` - moves the cursor to column 0
    - `\t` - creates a tab by printing spaces (usually set at 4, configurable)
    - `\v` - creates new line but keeps the column coordinate constant
    - `\033` - escape sequences, seperated by `;` and terminated by `m`

    Supported escape sequences:
    - `0` - clear all formatting
    - `1` - create bold text with A_STANDOUT
    - `30`-`37` - change foreground colour
    - `40`-`47` - change background colour
    """
    i = 0
    ansi = int(colorcode)
    fg = curses.COLOR_WHITE
    bg = curses.COLOR_BLACK
    while i < len(text):
        char = text[i]
        if char == "\f":
            win.clear()
        elif char == "\n":
            newline(win)
            if pauseAtNewline:
                time.sleep(pauseAtNewline)
        elif char == "\r":
            y, x = win.getyx()
            win.move(y, 0)
        elif char == "\t":
            spaces = " " * _TAB_SIZE
            win.addstr(spaces)
        elif char == "\v":
            x = win.getyx()[1]
            newline(win)
            y = win.getyx()[0]
            win.move(y, x)
        elif char == "\033" and text[i + 1] == "[":
            i, ansi, fg, bg = handleCSI(win, text, ansi, fg, bg, textPos=i + 2)
        else:
            win.addstr(char, curses.color_pair(ansi))
            if delay:
                win.refresh()
                time.sleep(delay)
        i += 1
    win.refresh()


def handleCSI(
    win: curses.window, text: str, ansiCode: int, fg: int, bg: int, textPos: int
):
    r"""
    Handles Control Sequence Introducer (CSI) characters ("\x1b[" or "\033[").
    Send the text to this function and the position after the "[" character.
    Handles 3-bit, 4-bit and 8-bit Select Graphic Rendition (SGR) colours.

    """
    # textPos is the start of the escape code
    code = []
    i = textPos - 1
    while (
        text[i] != "m"
        and i < len(text)
        and (text[i] not in _ENDBYTE_CHARS or i == textPos - 1)
    ):
        i += 1
        if text[i] == ";" or text[i] == ":" or text[i] == "m":
            code.append(text[textPos:i])
            textPos = i + 1
    textPos = i
    i = 0
    while i < len(code):
        item = code[i]
        if item == "0":
            win.addstr("", curses.A_NORMAL)
            ansiCode = 0
            fg = curses.COLOR_WHITE
            bg = curses.COLOR_BLACK
        elif item == "1":
            win.addstr("", curses.A_BOLD)
        elif len(item) == 2 and item[0] == "3" and item[1] < "8":
            fg = int(item[1])
        elif item == "38" and code[i + 2 :] and code[i + 1] == "5":
            fg = int(code[i + 2])
            i += 2
        elif len(item) == 2 and item[0] == "4" and item[1] < "8":
            bg = int(item[1])
        elif item == "48" and code[i + 2 :] and code[i + 1] == "5":
            bg = int(code[i + 2])
            i += 2
        elif len(item) == 2 and item[0] == "9" and item[1] < "8":
            fg = int(item[1]) + 8
        elif len(item) == 3 and item[0:2] == "10" and item[2] < "8":
            bg = int(item[2]) + 8
        ansiCode = int(str(fg) + str(bg)) % min((curses.COLOR_PAIRS), 255) + 1
        # On the above line, I use the magic number 255.
        # I would use a descriptive name, but I actually have no idea what it
        # does or why it works but everything breaks without it for some reason
        # despite the fact that it should actually break at 65536 on my machine
        curses.init_pair(ansiCode, fg, bg)
        i += 1
    return (textPos, ansiCode, fg, bg)


def newline(win: curses.window) -> None:
    """Move the cursor to the next line, automatically scrolling if needed,
    to prevent ERR."""
    win.scrollok(True)
    max_y, max_x = win.getmaxyx()
    y, x = win.getyx()
    y += 1
    x = 0
    if y >= max_y:
        win.scroll()
        y = max_y - 1
    if y >= max_y - 1:
        win.move(max_y - 1, x)
    else:
        win.move(y, x)
    win.refresh()


def option(win: curses.window, text: str, options: list) -> int | str:
    value = 0
    win.nodelay(False)
    while 1:
        win.clear()
        newline(win)
        max_y, max_x = win.getmaxyx()
        y, x = win.getyx()
        new_x = max((max_x - len(text) - 1) // 2, 0)
        win.move(y, new_x)
        curses.curs_set(0)
        win.scrollok(True)
        print3(win, text, delay=0)
        newline(win)
        win.refresh()
        fullLen = max(len(str(option)) for option in options)
        new_x = max((max_x - fullLen - 1) // 2 - 1, 0)
        for option in options:
            max_y, max_x = win.getmaxyx()
            newline(win)
            y, x = win.getyx()
            win.move(y, new_x)
            padding = (fullLen - len(str(option))) / 2
            padding += 1
            # printstr
            strToPrint = (
                " " * math.floor(padding) + str(option) + " " * math.ceil(padding)
            )
            win.addstr(" ")
            if options.index(option) == value:
                win.move(y, new_x - 1)
                win.addstr("> ")
                win.addstr(strToPrint, curses.A_STANDOUT)
            else:
                win.addstr(strToPrint)
        try:
            curses.flushinp()
            key = win.getkey()
        except Exception:
            key = "KEY_UP"
        if key == os.linesep:
            return value
        finalOption = len(options) - 1
        if key == "KEY_UP" and value > 0:
            value -= 1
        elif key == "KEY_UP" and value <= 0:
            value = finalOption
        elif key == "KEY_DOWN" and value < finalOption:
            value += 1
        elif key == "KEY_DOWN" and value >= finalOption:
            value = 0
        elif isinstance(key, str) and len(key) == 1 and not key.isnumeric():
            return key
        elif key.isnumeric() and int(key) < len(options) + 1 and int(key) > 0:
            value = int(key) - 1
        win.refresh()


def draw_titlebar(
    win: curses.window, title: str, leftString: str = "", rightString: str = ""
) -> None:
    # curses.init_pair(253, 252, curses.COLOR_BLACK)
    # curses.init_pair(226, curses.COLOR_BLACK, 252)
    win.scrollok(False)
    max_y, max_x = win.getmaxyx()
    win.move(0, 0)
    for y in range(0, max_y - 1):
        win.move(y, 0)
        win.addstr("║")
    for y in range(0, max_y - 1):
        win.move(y, max_x - 1)
        win.addstr("║")
    for x in range(0, max_x):
        win.move(max_y - 2, x)
        win.addstr("═")
    for x in range(0, max_x):
        win.move(0, x)
        win.addstr("═")
    win.move(0, 0)
    win.addstr("╔")
    win.move(0, max_x - 1)
    win.addstr("╗")
    win.move(max_y - 2, 0)
    win.addstr("╚")
    win.move(max_y - 2, max_x - 1)
    win.addstr("╝")
    centre = (max_x - len(title)) // 2
    win.move(0, centre)
    win.addstr(title, curses.color_pair(47))
    win.move(0, 1)
    win.addstr(leftString, curses.color_pair(47))
    win.move(0, max_x - len(rightString) - 1)
    win.addstr(rightString, curses.color_pair(47))
    win.scrollok(True)
    win.refresh()


def create_newwin(
    win: curses.window,
    padding: int = 1,
    padx1: int = 0,
    padx2: int = 0,
    pady1: int = 0,
    pady2: int = 0,
) -> curses.window:
    max_y, max_x = win.getmaxyx()
    if max_y < 5 or max_x < 5:
        return win
    begin_x = padx1 + padding
    begin_y = pady1 + padding
    height = max_y - (1 + pady2 + padding) - begin_y
    width = max_x - (1 + padx2 + padding) - begin_x
    newwin = curses.newwin(height, width, begin_y, begin_x)
    newwin.scrollok(True)
    newwin.keypad(True)
    colorsetup(newwin)
    return newwin

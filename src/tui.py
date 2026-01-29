import curses
import os
import time
import sys

def colorsetup(win):
  curses.start_color() #curses.A_NORMAL | curses.A_BOLD
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

def print3(win: curses.window, text: str, colorcode: int = 0, delay: float = 0.01, pauseAtNewline: float = 0.0, speedUp: bool = True) -> None:
  y, x = win.getyx()
  if y == 0:
    win.move(0, 0)
  i = 0
  ansi = int(colorcode)
  while i < len(text):
    char = text[i]
    if char == "\n":
      newline(win)
      if pauseAtNewline:
        time.sleep(pauseAtNewline)
    elif char == "\033":
      if text[i+1] == "[" and text[i+3].isdigit():
        ansi = int(text[i+2] + text[i+3])
        i += 4
      elif text[i+1] == "[" and text[i+3] == "m":
        if text[i+2] == "0":
          win.addstr("", curses.A_NORMAL)
          ansi = 0
        elif text[i+2] == "1":
          win.addstr("", curses.A_BOLD)
        i += 3
    else:
      win.addstr(char, curses.color_pair(ansi))
      if delay:
        win.refresh()
        time.sleep(delay)
    i += 1
  win.refresh()


def newline(win: curses.window) -> None:
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
  while (1):
    win.clear()
    win.move(0, 0)
    curses.curs_set(0)
    win.scrollok(True)
    print3(win, text, 0, 0)
    win.refresh()
    for option in options:
      newline(win)
      win.addstr(" ")
      if options.index(option) == value:
        win.addstr("> ")
        win.addstr(str(option), curses.A_STANDOUT)
      else:
        win.addstr(str(option))
    try:
      curses.flushinp()
      key = win.getkey()
    except Exception:
      key = "KEY_UP"
    if key == os.linesep:
      return (value)
    finalOption = (len(options) - 1)
    if key == "KEY_UP" and value > 0:
      value -= 1
    elif key == "KEY_UP" and value <= 0:
      value = finalOption
    elif key == "KEY_DOWN" and value < finalOption:
      value += 1
    elif key == "KEY_DOWN" and value >= finalOption:
      value = 0
    elif isinstance(key, str) and len(key) == 1 and not key.isnumeric():
      return(key)
    elif key.isnumeric() and int(key) < len(options) + 1 and int(key) > 0:
      value = (int(key) - 1)
    win.refresh()

def draw_titlebar(win: curses.window, title: str, leftString: str = "", rightString: str = "") -> None:
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
    pady2: int = 0
    ) -> curses.window:
    max_y, max_x = win.getmaxyx()
    if max_y < 5 or max_x < 5:
        return(win)
    begin_x = (padx1 + padding)
    begin_y = (pady1 + padding)
    height = (max_y - (1 + pady2 + padding) - begin_y)
    width = (max_x - (1 + padx2 + padding) - begin_x)
    newwin = curses.newwin(height, width, begin_y, begin_x)
    newwin.scrollok(True)
    newwin.keypad(True)
    colorsetup(newwin)
    return(newwin)

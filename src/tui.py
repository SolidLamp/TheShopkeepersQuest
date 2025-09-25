import curses
import os
import time
#import math
import sys

value = 0

#def uutime(win):
#while 1:
#win.clear()
#win.addstr(str(math.floor(time.time())))
#win.refresh()


def print3(win, text, colorcode=0, speed=0.01):
  for char in text:
    if char == "\n":
      newline(win)
    elif char == "\033":
      win.addstr("DD")
    else:
      win.addstr(char, curses.color_pair(colorcode))
      win.refresh()
      time.sleep(speed)


def newline(win):
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


def option(win, text, options):
  value = 0
  win.nodelay(False)
  while (1):
    win.clear()
    win.move(0, 0)
    curses.curs_set(0)
    win.scrollok(True)
    win.addstr(text)
    win.refresh()
    for option in options:
      newline(win)
      win.addstr(" ")
      if options.index(option) == value:
        win.addstr("> ")
        win.addstr(str(option), curses.color_pair(8))
      else:
        win.addstr(str(option))
    #win.getch()
    try:
      key = win.getkey()
    except Exception:
      key = "KEY_UP"
    if key == os.linesep:
      return (value)
    if key == "KEY_UP" and value > 0:
      value -= 1
    elif key == "KEY_DOWN" and value < (len(options) - 1):
      value += 1
    elif key == "q":
      sys.exit()
    win.refresh()


#def main(win):
#  #win.nodelay(False)
#  key = ""
#  while 1:
#    try:
#      key = win.getkey()
#      win.clear()
#      win.addstr("\n")
#      win.addstr("Detected key:")
#      win.addstr(str(key))
#      value = option(win, key, ["Option 0","Option 1"])
#      if key == os.linesep:
#        return(value)
#    except Exception:
#      pass

#value = curses.wrapper(main)
#print(value)

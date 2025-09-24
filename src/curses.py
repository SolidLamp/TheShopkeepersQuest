import curses
import os
value = 0

def option(win,key,options):
  curses.curs_set(0)
  global value
  if value is None:
    value = 0
  win.addstr(str(value))
  if key == "KEY_UP" and value > 0:
    value -= 1
  elif key == "KEY_DOWN" and value < (len(options) - 1):
    value += 1
  for option in options:
    win.addstr("\n ")
    if options.index(option) == value:
      win.addstr(">")
    win.addstr(str(option))
  if key == os.linesep:
    return(value)

def main(win):
  win.nodelay(False)
  key = ""
  while 1:
    try:
      key = win.getkey()
      win.clear()
      win.addstr("\n")
      win.addstr("Detected key:")
      win.addstr(str(key))
      value = option(win, key, ["Option 0","Option 1"])
      if key == os.linesep:
        return(value)
    except Exception:
      pass


value = curses.wrapper(main)
print(value)

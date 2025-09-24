import curses
import os
value = 0

def newline(win):
  max_y, max_x = win.getmaxyx()
  y, x = win.getyx()
  y += 1
  x = 0
  if y >= max_y:
      win.scroll()
      y = max_y - 1
  if y >= max_y - 1:
    win.move(max_y - 2, x)
  else:
    win.move(y, x)
  win.refresh()

def option(win,options):
  while 1:
    try:
      key = win.getkey()
    except Exception:
      key = "KEY_UP"
    curses.curs_set(0)
    global value
    if value is None:
      value = 0
    if key == "KEY_UP" and value > 0:
      value -= 1
    elif key == "KEY_DOWN" and value < (len(options) - 1):
      value += 1
    for option in options:
      newline(win)
      win.addstr(" ")
      if options.index(option) == value:
        win.addstr(">")
      win.addstr(str(option))
    win.getch()
    if key == os.linesep:
      return(value)

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

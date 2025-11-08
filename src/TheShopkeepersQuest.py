#!/usr/bin/env python3
import platform
import sys
import os
import title

if platform.system() != "Windows" and os.getuid() == 0:
  print("\033[31mCritical Error: root should not be running user processes")
  sys.exit(1)

if len(sys.argv) > 1:
  for arg in sys.argv:
    #print(arg)
    match arg:
      case "--about" | "--help" | "-h":
        print("The Shopkeeper's Quest - 1.1\n2025-11-07\nMIT License\nCreated by SolidLamp\nhttps://github.com/solidlamp\n\n-h | --help | --about  --  opens this menu\n[no args]  --  runs the game")
  #print(sys.argv[1])
  sys.exit(0)

title.title()

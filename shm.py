import time
from dataclasses import dataclass
import random

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        sys.argv[1]
    else:
        print(
            "SHM Engine 0.6\n2025-09-11\nhttps://github.com/solidlamp\nThis release: The Shopkeeper's Quest Experimental - 2025-09-11"
        )


def print2(text, newline=True, pauseAtNewline=0.0, endingChar=False):
    for char in text:
        if char == "\n":
            time.sleep(pauseAtNewline)
        print(char, end="", flush=True)
        time.sleep(0.01)
    if newline:
        print()

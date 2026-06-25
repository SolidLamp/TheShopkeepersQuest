import curses
from typing import Literal


class RestrictedWindow:
    """A restricted version of a curses window for public API usage."""

    def __init__(self, raw_window: curses.window) -> None:
        self._raw_window: curses.window = raw_window
        self.encoding: str = self._raw_window.encoding

    def addch(self, ch, *args, **kwargs) -> None:
        self._raw_window.addch(ch, *args, **kwargs)

    def addnstr(self, string: str, n: int, *args, **kwargs) -> None:
        self._raw_window.addnstr(string, n, *args, **kwargs)

    def addstr(self, string: str, *args, **kwargs) -> None:
        self._raw_window.addstr(string, *args, **kwargs)

    def attroff(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def attron(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def attrset(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def bkgd(self, ch, *args, **kwargs) -> None:
        self._raw_window.bkgd(ch, *args, **kwargs)

    def bkgdset(self, ch, *args, **kwargs) -> None:
        self._raw_window.bkgdset(ch, *args, **kwargs)

    def border(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def box(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def chgat(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def clear(self) -> None:
        self._raw_window.clear()

    def clearok(self, flag: bool) -> None:
        yes: int = int(flag)
        self._raw_window.clearok(yes)

    def clrtobot(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def clrtoeol(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def cursyncup(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def delch(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def deleteln(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def derwin(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def echochar(self, ch, *args, **kwargs) -> None:
        self._raw_window.echochar(ch, *args, **kwargs)

    def enclose(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def erase(self) -> None:
        self._raw_window.erase()

    def getbegyx(self, *args, **kwargs) -> tuple[bool, bool]:
        # Restricted function
        return (False, False)

    def getbkgd(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def getch(self, *args, **kwargs) -> int:
        char: int = self._raw_window.getch(*args, **kwargs)
        return char

    def get_wch(self) -> int | str:
        char: int | str = self._raw_window.get_wch()
        return char

    def getkey(self, *args, **kwargs) -> int | str:
        char: int | str = self._raw_window.getkey(*args, **kwargs)
        return char

    def getmaxyx(self) -> tuple[int, int]:
        maxyx: tuple[int, int] = self._raw_window.getmaxyx()
        return maxyx

    def getparyx(self) -> tuple[int, int]:
        paryx: tuple[int, int] = self._raw_window.getparyx()
        return paryx

    def getstr(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def getyx(self) -> tuple[int, int]:
        yx: tuple[int, int] = self._raw_window.getyx()
        return yx

    def hline(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def idcok(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def idlok(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def immedok(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def inch(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def insch(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def insdelln(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def insertln(self) -> None:
        """Creates a newline for a curses window, automatically scrolling."""
        self._raw_window.scrollok(True)
        max_y, max_x = self._raw_window.getmaxyx()
        y, x = self._raw_window.getyx()
        y += 1
        x = 0
        if y >= max_y:
            self._raw_window.scroll()
            y = max_y - 1
        if y >= max_y - 1:
            self._raw_window.move(max_y - 1, x)
        else:
            self._raw_window.move(y, x)
        self._raw_window.refresh()

    def insnstr(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def insstr(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def instr(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def is_linetouched(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def is_wintouched(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def keypad(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def leaveok(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def move(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def mvderwin(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def mvwin(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def nodelay(self, flag: bool) -> None:
        self._raw_window.nodelay(flag)

    def notimeout(self, flag: bool) -> None:
        self._raw_window.notimeout(flag)

    def noutrefresh(self, *args, **kwargs) -> None:
        self._raw_window.noutrefresh()

    def overlay(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def overwrite(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def putwin(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def redrawln(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def redrawwin(self) -> None:
        self._raw_window.redrawwin()

    def refresh(self, *args, **kwargs) -> None:
        self._raw_window.refresh()

    def resize(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def scroll(self, lines: int = 1) -> None:
        """Scroll the screen."""
        if not isinstance(lines, int):
            raise TypeError("Lines must be int.")
        for i in range(lines):
            try:
                self._raw_window.scroll()
            except curses.error:
                pass

    def scrollok(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def setscrreg(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def standend(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def standout(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def subpad(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def subwin(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def syncdown(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def syncok(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def syncup(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def timeout(self, delay: int) -> None:
        if not isinstance(delay, int):
            raise TypeError("delay must be int")
        self._raw_window.timeout(delay)

    def touchline(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

    def touchwin(self) -> None:
        self._raw_window.touchwin()

    def untouchwin(self) -> None:
        self._raw_window.untouchwin()

    def vline(self, *args, **kwargs) -> Literal[False]:
        # Restricted function
        return False

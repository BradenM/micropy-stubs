# make_stub_files: Wed 17 Jul 2019 at 02:33:02

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
def _wr(s: str) -> None: ...
def _move(row: Any, col: Any) -> None: ...
def _clear_num_pos(num: Any) -> None: ...
def _draw_box(left: Any, top: Any, width: Any, height: Any) -> None: ...
class error(Exception): ...
class Window:
    def __init__(self, lines: Any, cols: Any, y: Any, x: Any) -> None: ...
    def _goto(self, row: Any, col: Any) -> None: ...
    def move(self, y: Any, x: Any) -> None: ...
    def getmaxyx(self) -> Tuple[Any, Any]: ...
    def addstr(self, y: Any, x: Any, str: Any, attr: Any=A_NORMAL) -> None: ...
    def addnstr(self, y: Any, x: Any, str: Any, n: int, attr: Any=A_NORMAL) -> None: ...
    def addch(self, y: Any, x: Any, ch: Any, attr: Any=A_NORMAL) -> None: ...
    def attron(self, attr: Any) -> None: ...
    def attroff(self, attr: Any) -> None: ...
    def attrset(self, attr: Any) -> None: ...
    def bkgdset(self, ch: Any, attr: Any=A_NORMAL) -> None: ...
    def erase(self) -> None: ...
    def border(self) -> None: ...
    def hline(self, y: Any, x: Any, ch: Any, n: int) -> None: ...
    def vline(self, y: Any, x: Any, ch: Any, n: int) -> None: ...
    def refresh(self) -> None: ...
    def redrawwin(self) -> None: ...
    def keypad(self, yes: Any) -> None: ...
    def timeout(self, delay: Any) -> None: ...
    def nodelay(self, yes: Any) -> None: ...
    def getch(self) -> Union[Any, number]: ...
        #   0: return c
        # ? 0: return c
        #   1: return -1
        #   1: return number
        #   2: return key
        # ? 2: return key
def wrapper(func: Any) -> Any: ...
    #   0: return res
    # ? 0: return res
def initscr() -> Any: ...
    #   0: return SCREEN
    # ? 0: return SCREEN
def doupdate() -> None: ...
def endwin() -> None: ...
def raw() -> None: ...
def cbreak() -> None: ...
def nocbreak() -> None: ...
def echo() -> None: ...
def noecho() -> None: ...
def meta(yes: Any) -> None: ...
def mousemask(mask: Any) -> None: ...
def has_colors() -> bool: ...
def can_change_color() -> bool: ...
def curs_set(visibility: Any) -> None: ...
def beep() -> None: ...
def newwin(lines: Any, cols: Any, y: Any=0, x: Any=0) -> Any: ...
    #   0: return Window(lines,cols,y,x)
    # ? 0: return Window(lines, cols, y, x)

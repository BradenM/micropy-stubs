# make_stub_files: Tue 03 Sep 2019 at 17:05:43

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class Gameboy:
    def __init__(self, addr: Any=8) -> None: ...
    def _monitor(self) -> None: ...
    def getStatus(self, num: Any) -> bool: ...
    def getPressed(self, num: Any) -> bool: ...
    def getReleased(self, num: Any) -> bool: ...
    def _available(self) -> None: ...
    def _update(self) -> None: ...
    def deinit(self) -> None: ...

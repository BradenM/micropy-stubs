# make_stub_files: Tue 20 Aug 2019 at 15:53:52

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class NeoPixel:
    def __init__(self, pin: machine.Pin.pin, n: int, bpp: Any=3, timing: Any=1) -> None: ...
    def __setitem__(self, index: Any, val: Any) -> None: ...
    def __getitem__(self, index: Any) -> Tuple[Any]: ...
    def fill(self, color: Any) -> None: ...
    def write(self) -> None: ...

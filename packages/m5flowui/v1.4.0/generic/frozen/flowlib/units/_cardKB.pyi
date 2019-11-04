
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class CardKB:
    def __init__(self, port: Any, addr: Any=95) -> None: ...
    def _available(self) -> None: ...
    def keyString(self) -> Any: ...
        #   0: return self.string[:]
        # ? 0: return self.string[:]
    def keyData(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return data[0]
        # ? 1: return data[number]
    def isNewKeyPress(self) -> bool: ...
    def _monitor(self) -> None: ...
    def deinit(self) -> None: ...

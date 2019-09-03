# make_stub_files: Tue 03 Sep 2019 at 17:05:43

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class Env:
    def __init__(self, port: Any) -> None: ...
    def _available(self) -> None: ...
    def deinit(self) -> None: ...
    def pressure(self) -> Any: ...
        #   0: return round(self.data[1],2)
        # ? 0: return round(self.data[number], number)
    def temperature(self) -> Any: ...
        #   0: return round(self.data[0],2)
        # ? 0: return round(self.data[number], number)
    def humidity(self) -> Any: ...
        #   0: return round(self.data[2],2)
        # ? 0: return round(self.data[number], number)
    def values(self) -> Union[Any, Tuple[Any, Any, Any]]: ...
        #   0: return self.data
        # ? 0: return self.data
        #   1: return (t, p, h)
        #   1: return Tuple[t, p, h]
        #   2: return self.data
        # ? 2: return self.data

# make_stub_files: Mon 22 Jul 2019 at 22:33:18

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class Lock:
    def __init__(self) -> None: ...
    def release(self) -> None: ...
    def acquire(self) -> bool: ...

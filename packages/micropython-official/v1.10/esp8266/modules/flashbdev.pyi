# make_stub_files: Fri 21 Jun 2019 at 00:44:04

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class FlashBdev:
    def __init__(self, blocks: Any=NUM_BLK) -> None: ...
    def readblocks(self, n: int, buf: Any) -> None: ...
    def writeblocks(self, n: int, buf: Any) -> None: ...
    def ioctl(self, op: Any, arg: Any) -> Any: ...
        #   0: return self.blocks
        # ? 0: return self.blocks
        #   1: return self.SEC_SIZE
        # ? 1: return self.SEC_SIZE


from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
def try_remove(fn: str) -> None: ...
def get_filesize(fn: str) -> Any: ...
    #   0: return os.stat(fn)[]
    # ? 0: return os.stat(str)[]
class RotatingFileHandler(Handler):
    def __init__(self, filename: str, maxBytes: Any=, backupCount: Any=) -> None: ...
    def emit(self, record: Any) -> None: ...

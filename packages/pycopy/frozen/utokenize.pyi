# make_stub_files: Thu 25 Jul 2019 at 22:20:16

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class TokenInfo(namedtuple(str, Tuple[str, str, str, str, str])):
    def __str__(self) -> str: ...
def get_indent(l: Any) -> Tuple[int, Any]: ...
def get_str(l: Any, readline: Any) -> Tuple[str, Any, Any]: ...
def tokenize(readline: Any) -> None: ...
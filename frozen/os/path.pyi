
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
def normcase(s: str) -> str: ...
def normpath(s: str) -> str: ...
def abspath(s: str) -> Union[Any, str]: ...
    #   0: return os.getcwd()++s
    # ? 0: return os.getcwd()++str
    #   1: return s
    #   1: return str
def join(*args) -> Any: ...
    #   0: return res.encode()
    # ? 0: return res.encode()
    #   1: return res
    # ? 1: return res
def split(path: Any) -> Union[Tuple[, Any], Tuple[, ], Tuple[Any, str]]: ...
def splitdrive(path: Any) -> Tuple[, Any]: ...
def dirname(path: Any) -> Any: ...
    #   0: return split(path)[]
    # ? 0: return split(path)[]
def basename(path: Any) -> Any: ...
    #   0: return split(path)[]
    # ? 0: return split(path)[]
def exists(path: Any) -> Any: ...
    #   0: return os.access(path,os.F_OK)
    # ? 0: return os.access(path, os.F_OK)
def isfile(path: Any) -> Optional[Any]: ...
    #   0: return stat.S_ISREG(mode)
    # ? 0: return stat.S_ISREG(mode)
    #   1: return
    #   1: return
def isdir(path: Any) -> Optional[Any]: ...
    #   0: return stat.S_ISDIR(mode)
    # ? 0: return stat.S_ISDIR(mode)
    #   1: return
    #   1: return
def islink(path: Any) -> Optional[Any]: ...
    #   0: return stat.S_ISLNK(mode)
    # ? 0: return stat.S_ISLNK(mode)
    #   1: return
    #   1: return
def expanduser(s: str) -> Union[Any, str]: ...
    #   0: return h+s[:]
    # ? 0: return h+str
    #   1: return +s[:]
    # ? 1: return +str
    #   2: return s
    #   2: return str


from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
def normcase(s: str) -> str: ...
def normpath(s: str) -> str: ...
def abspath(s: str) -> Union[Any, str]: ...
    #   0: return os.getcwd()+'/'+s
    # ? 0: return os.getcwd()+str+str
    #   1: return s
    #   1: return str
def join(*args) -> Any: ...
    #   0: return res.encode()
    # ? 0: return res.encode()
    #   1: return res
    # ? 1: return res
def split(path: Any) -> Union[Tuple[Any, str], Tuple[str, Any], Tuple[str, str]]: ...
def splitext(path: Any) -> Union[Tuple[Any, str], Tuple[str, str]]: ...
def splitdrive(path: Any) -> Tuple[str, Any]: ...
def dirname(path: Any) -> Any: ...
    #   0: return split(path)[0]
    # ? 0: return split(path)[number]
def basename(path: Any) -> Any: ...
    #   0: return split(path)[1]
    # ? 0: return split(path)[number]
def exists(path: Any) -> Any: ...
    #   0: return os.access(path,os.F_OK)
    # ? 0: return os.access(path, os.F_OK)
def isfile(path: Any) -> Union[Any, bool]: ...
    #   0: return stat.S_ISREG(mode)
    # ? 0: return stat.S_ISREG(mode)
    #   1: return bool
    #   1: return bool
def isdir(path: Any) -> Union[Any, bool]: ...
    #   0: return stat.S_ISDIR(mode)
    # ? 0: return stat.S_ISDIR(mode)
    #   1: return bool
    #   1: return bool
def islink(path: Any) -> Union[Any, bool]: ...
    #   0: return stat.S_ISLNK(mode)
    # ? 0: return stat.S_ISLNK(mode)
    #   1: return bool
    #   1: return bool
def isabs(path: Any) -> Any: ...
    #   0: return path.startswith('/')
    # ? 0: return path.startswith(str)
def realpath(path: Any) -> Any: ...
    #   0: return res
    # ? 0: return res
    #   1: return abspath(path)
    # ? 1: return abspath(path)
def expanduser(s: str) -> Union[Any, str]: ...
    #   0: return h+s[1:]
    # ? 0: return h+str
    #   1: return '/home/'+s[1:]
    #   1: return str
    #   2: return s
    #   2: return str

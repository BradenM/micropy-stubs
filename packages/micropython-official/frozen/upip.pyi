# make_stub_files: Wed 10 Jul 2019 at 03:41:51

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class NotFoundError(Exception): ...
def op_split(path: Any) -> Union[Tuple[Any, str], Tuple[str, Any], Tuple[str, str]]: ...
def op_basename(path: Any) -> Any: ...
    #   0: return op_split(path)[1]
    # ? 0: return op_split(path)[number]
def _makedirs(name: str, mode: Any=511) -> Any: ...
    #   0: return ret
    # ? 0: return ret
def save_file(fname: Any, subf: Any) -> None: ...
def install_tar(f: Any, prefix: Any) -> Any: ...
    #   0: return meta
    # ? 0: return meta
def expandhome(s: str) -> str: ...
def url_open(url: Any) -> str: ...
def get_pkg_metadata(name: str) -> Any: ...
    #   0: return json.load(f)
    # ? 0: return json.load(f)
def fatal(msg: Any, exc: Any=None) -> None: ...
def install_pkg(pkg_spec: Any, install_path: Any) -> Any: ...
    #   0: return meta
    # ? 0: return meta
def install(to_install: Any, install_path: Any=None) -> None: ...
def get_install_path() -> Any: ...
    #   0: return install_path
    # ? 0: return install_path
def cleanup() -> None: ...
def help() -> None: ...
def main() -> None: ...

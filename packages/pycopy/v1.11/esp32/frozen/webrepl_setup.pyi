# make_stub_files: Wed 17 Jul 2019 at 02:38:14

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
def input_choice(prompt: Any, choices: Any) -> Any: ...
    #   0: return resp
    # ? 0: return resp
def getpass(prompt: Any) -> Any: ...
    #   0: return input(prompt)
    # ? 0: return input(prompt)
def input_pass() -> Any: ...
    #   0: return passwd1
    # ? 0: return passwd1
def exists(fname: Any) -> bool: ...
def get_daemon_status() -> Optional[bool]: ...
def change_daemon(action: Any) -> None: ...
def main() -> None: ...

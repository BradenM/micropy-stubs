
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
def md5_concat(arg1: Any, arg2: Any, arg3: Any) -> Any: ...
    #   0: return ubinascii.hexlify(h.digest()).decode()
    # ? 0: return ubinascii.hexlify(h.digest()).decode()
def make_digest_ha1(a1: Any, method: Any, uri: Any, nonce: Any) -> Any: ...
    #   0: return digest
    # ? 0: return digest
def make_digest(realm: Any, username: Any, passwd: Any, method: Any, uri: Any, nonce: Any) -> Any: ...
    #   0: return make_digest_ha1(a1,method,uri,nonce)
    # ? 0: return make_digest_ha1(a1, method, uri, nonce)
def parse_auth_req(line: Any) -> Any: ...
    #   0: return d
    # ? 0: return d
def format_resp(resp_d: Any) -> Any: ...
    #   0: return resp_auth
    # ? 0: return resp_auth
def _digest_resp(auth_d: Any, username: Any, passwd: Any, method: Any, URL: Any) -> Any: ...
    #   0: return format_resp(resp_d)
    # ? 0: return format_resp(resp_d)
def basic_resp(username: Any, passwd: Any) -> str: ...
def auth_resp(auth_line: Any, username: Any, passwd: Any, method: Any=None, URL: Any=None) -> Any: ...
    #   0: return basic_resp(username,passwd)
    # ? 0: return basic_resp(username, passwd)
    #   1: return _digest_resp(auth_d,username,passwd,method,URL)
    # ? 1: return _digest_resp(auth_d, username, passwd, method, URL)
class WWWAuth:
    def __init__(self, username: Any, passwd: Any) -> None: ...
    def resp(self, auth_line: Any, method: Any, URL: Any) -> Any: ...
        #   0: return basic_resp(self.username,self.passwd)
        # ? 0: return basic_resp(self.username, self.passwd)
        #   1: return format_resp(auth_d)
        # ? 1: return format_resp(auth_d)


from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
def write_fqdn(buf: Any, name: str) -> None: ...
def skip_fqdn(buf: Any) -> None: ...
def make_req(buf: Any, fqdn: Any, is_ipv6: Any, unicast: Any=bool) -> None: ...
def parse_resp(buf: Any, is_ipv6: Any) -> Any: ...
    #   0: return rval
    # ? 0: return rval

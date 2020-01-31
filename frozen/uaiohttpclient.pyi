
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class ClientResponse:
    def __init__(self, reader: Any) -> None: ...
    def read(self, sz: Any=-) -> Any: ...
        #   0: return yield from self.content.read(sz)
        # ? 0: return yield from self.content.read(sz)
    def __repr__(self) -> Any: ...
        #   0: return %(self.status, self.headers)
        # ? 0: return %Tuple[self.status, self.headers]
class ChunkedClientResponse(ClientResponse):
    def __init__(self, reader: Any) -> None: ...
    def read(self, sz: Any=**) -> Optional[Any]: ...
        #   0: return
        #   0: return 
        #   1: return data
        # ? 1: return data
    def __repr__(self) -> Any: ...
        #   0: return %(self.status, self.headers)
        # ? 0: return %Tuple[self.status, self.headers]
def request_raw(method: Any, url: Any) -> Any: ...
    #   0: return reader
    # ? 0: return reader
def request(method: Any, url: Any) -> Any: ...
    #   0: return resp
    # ? 0: return resp

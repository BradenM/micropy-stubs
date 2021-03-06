
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class MQTTException(Exception): ...
class MQTTClient:
    def __init__(self, client_id: Any, server: Any, port: Any=0, user: Any=None, password: Any=None, keepalive: Any=0, ssl: Any=bool, ssl_params: Any={}) -> None: ...
    def _send_str(self, s: str) -> None: ...
    def _recv_len(self) -> int: ...
    def set_callback(self, f: Any) -> None: ...
    def set_last_will(self, topic: Any, msg: Any, retain: Any=bool, qos: Any=0) -> None: ...
    def connect(self, clean_session: Any=bool) -> Any: ...
        #   0: return resp[2]&1
        # ? 0: return resp[number]&number
    def disconnect(self) -> None: ...
    def ping(self) -> None: ...
    def publish(self, topic: Any, msg: Any, retain: Any=bool, qos: Any=0) -> None: ...
    def subscribe(self, topic: Any, qos: Any=0) -> None: ...
    def wait_msg(self) -> Optional[Any]: ...
        #   0: return None
        #   0: return None
        #   1: return None
        #   1: return None
        #   2: return op
        # ? 2: return op
    def check_msg(self) -> Any: ...
        #   0: return self.wait_msg()
        # ? 0: return self.wait_msg()

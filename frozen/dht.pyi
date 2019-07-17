# make_stub_files: Wed 17 Jul 2019 at 02:40:01

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class DHTBase:
    def __init__(self, pin: machine.Pin.pin) -> None: ...
    def measure(self) -> None: ...
class DHT11(DHTBase):
    def humidity(self) -> Any: ...
        #   0: return self.buf[0]
        # ? 0: return self.buf[number]
    def temperature(self) -> Any: ...
        #   0: return self.buf[2]
        # ? 0: return self.buf[number]
class DHT22(DHTBase):
    def humidity(self) -> Any: ...
        #   0: return self.buf[0]<<8|self.buf[1]*0.1
        # ? 0: return self.buf[number]<<number|self.buf[number]*number
    def temperature(self) -> Any: ...
        #   0: return t
        # ? 0: return t

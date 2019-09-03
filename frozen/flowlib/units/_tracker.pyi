# make_stub_files: Tue 03 Sep 2019 at 17:05:43

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class Tracker:
    def __init__(self, port: Any) -> None: ...
    def _available(self) -> None: ...
    def _register_char(self, register: Any, value: Any=None, buf: Any=bytearray(1)) -> Any: ...
        #   0: return buf[0]
        # ? 0: return buf[number]
        #   1: return self._i2c.writeto_mem(self._addr,register,buf)
        # ? 1: return self._i2c.writeto_mem(self._addr, register, buf)
    def _register_short(self, register: Any, value: Any=None, buf: Any=bytearray(2)) -> Any: ...
        #   0: return ustruct.unpack('>h',buf)[0]
        # ? 0: return ustruct.unpack(str, buf)[number]
        #   1: return self._i2c.writeto_mem(self._addr,register,buf)
        # ? 1: return self._i2c.writeto_mem(self._addr, register, buf)
    def getAnalogValue(self, pos: Any) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self._register_short(0|pos)
        # ? 1: return self._register_short(number|pos)
    def setAnalogValue(self, pos: Any, value: Any) -> number: ...
    def getDigitalValue(self, pos: Any) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self._register_char(0)&1<<pos-1
        # ? 1: return self._register_char(number)&number<<pos-number
    def deinit(self) -> None: ...

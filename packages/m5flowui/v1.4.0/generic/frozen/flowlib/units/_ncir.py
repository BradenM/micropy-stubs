import i2c_bus, unit
from micropython import const
import ustruct

_ADDR = const(0x5a)
_TOBJ1 = const(0x07)

class Ncir:

    def __init__(self, port):
        self.i2c = i2c_bus.get(port)
        self._available()
    
    def _available(self):
        if self.i2c.is_ready(_ADDR) or self.i2c.is_ready(_ADDR):
            pass
        else:
            raise unit.Unit("NCIR unit maybe not connect")
    
    @property
    def temperature(self):
        data = bytearray(2)

        self.i2c.begin(256)
        self.i2c.start()
        self.i2c.address(_ADDR, 0)
        self.i2c.write_byte(_TOBJ1)
        self.i2c.start()
        self.i2c.write_byte(_ADDR << 1 | 1)
        self.i2c.read_bytes(2)
        self.i2c.stop()
        res = self.i2c.end()
        tmp = res[0] + res[1]*256
        tmp = tmp*0.02 - 273.15
        return round(tmp, 2)

    def deinit(self):
        pass

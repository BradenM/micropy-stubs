import unit, i2c_bus
import ustruct
class Tracker:
    def __init__(self, port):
        self._addr = 0x5a
        self._i2c = i2c_bus.get(port)
        self._available()

    def _available(self):
        if self._i2c.is_ready(self._addr) or self._i2c.is_ready(self._addr):
            pass
        else:
            raise unit.Unit("Tracker unit maybe not connect")

    def _register_char(self, register, value=None, buf=bytearray(1)):
        if value is None:
            self._i2c.readfrom_mem_into(self._addr, register, buf)
            return buf[0]

        ustruct.pack_into("<b", buf, 0, value)
        return self._i2c.writeto_mem(self._addr, register, buf)

    def _register_short(self, register, value=None, buf=bytearray(2)):
        if value is None:
            self._i2c.readfrom_mem_into(self._addr, register, buf)
            return ustruct.unpack(">h", buf)[0]

        ustruct.pack_into(">h", buf, 0, value)
        return self._i2c.writeto_mem(self._addr, register, buf)

    def getAnalogValue(self, pos):
        if pos > 4 or pos < 0:
            return 0
        
        return self._register_short(0x00 | pos)

    def setAnalogValue(self, pos, value):
        if pos > 4 or pos < 0:
            return 0
        
        self._register_short(0x10 | pos, value)

    def getDigitalValue(self, pos):
        if pos > 4 or pos < 0:
            return 0

        return self._register_char(0x00) & (1 << (pos - 1))
    
    def deinit(self):
        pass
import i2c_bus, unit
import ustruct
from micropython import const
import machine
from m5stack import timEx

_MODEL_ID = const(0xc0)
_REVISION_ID = const(0xc2)
_START = const(0x00)
_RANGE_STATUS = const(0x14)
_SCL_SDA__EXTSUP_HV = const(0x89)
_MSRC_CONFIG_CONTROL = const(0x60)
_ADDR = const(0x29)

class Tof:        
    def __init__(self, port):
        self.i2c = i2c_bus.get(port)
        self._available()
        self.timer = timEx.addTimer(70, timEx.PERIODIC, self._update)
        self.state = 0
        self.distance = 0

    def _register_char(self, register, value=None, buf=bytearray(1)):
        if value is None:
            self.i2c.readfrom_mem_into(_ADDR, register, buf)
            return buf[0]

        ustruct.pack_into("<b", buf, 0, value)
        return self.i2c.writeto_mem(_ADDR, register, buf)

    def _register_short(self, register, value=None, buf=bytearray(2)):
        if value is None:
            self.i2c.readfrom_mem_into(_ADDR, register, buf)
            return ustruct.unpack(">h", buf)[0]

        ustruct.pack_into(">h", buf, 0, value)
        return self.i2c.writeto_mem(_ADDR, register, buf)
   
    def _available(self):
        if self.i2c.is_ready(_ADDR) or self.i2c.is_ready(_ADDR):
            pass
        else:
            raise unit.Unit("TOF unit maybe not connect")

    def _update(self):
        try:
            if self.state == 0:
                self._register_char(_START, 0x01)
                self.state = 1
            elif self.state == 1:
                data = self._register_char(0x14)
                if data & 0x01:
                    self.state = 0
                    distance = self._register_short(0x14 + 10)
                    if distance != 20:
                        self.distance = distance
        except:
            pass

    def deinit(self):
        self.timer.deinit()
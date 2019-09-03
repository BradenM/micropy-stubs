import i2c_bus, unit
from micropython import const

class Dac:
    portMethod = unit.PORT_I2C 
    WRITE = const(0x40)
    WRITE_EEPROM = const(0x60)

    def __init__(self, port, addr=0x60):
        self.i2c = i2c_bus.get(port)
        self.addr = addr
        self._available()

    def _available(self):
        if self.i2c.is_ready(self.addr) or self.i2c.is_ready(self.addr):
            pass
        else:
            raise unit.Unit("DAC unit maybe not connect")
    
    def writeData(self, data, save=False):
        data = int(min(4096, data))
        buf=bytearray(2)
        reg_addr = Dac.WRITE_EEPROM if save else Dac.WRITE
        buf[0] = (data & 0x0ff0) >> 4
        buf[1] = (data & 0x000f) << 4

        self.i2c.writeto_mem(self.addr, reg_addr, buf)

    def setVoltage(self, vol, save=False):
        vol = min(3.3, vol)
        vol = int(vol / 3.3 * 2640)
        reg_addr = 0
        buf=bytearray(2)

        reg_addr = Dac.WRITE_EEPROM if save else Dac.WRITE
        buf[0] = (vol & 0x0ff0) >> 4
        buf[1] = (vol & 0x000f) << 4

        self.i2c.writeto_mem(self.addr, reg_addr, buf)
    
    def deinit(self):
        pass

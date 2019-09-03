import i2c_bus, unit
from micropython import const
import ustruct

_ADDR = const(0x27)
_INPUT_REG = const(0x00)
_OUTPUT_REG = const(0x01)
_POLINV_REG = const(0x02)
_CONFIG_REG = const(0x03)

class Ext_io:
    ALL_OUTPUT = const(0x00)
    ALL_INPUT = const(0xff)

    OUTPUT = const(0x00)
    INPUT = const(0x01)

    def __init__(self, port):
        self.i2c = i2c_bus.get(port)
        self._available()
        self.config = Ext_io.ALL_INPUT
        self.setPortMode(self.config)

    def _available(self):
        if self.i2c.is_ready(_ADDR) or self.i2c.is_ready(_ADDR):
            pass
        else:
            raise unit.Unit("Ext IO unit maybe not connect")

    def _get_mode(self):
        return self.i2c.readfrom_mem(_ADDR, _CONFIG_REG, 1)[0]

    def setPortMode(self, mode):
        buf = bytearray(1)
        buf[0] = mode
        self.i2c.writeto_mem(_ADDR, _CONFIG_REG, buf)

    def setPinMode(self, pin, mode):
        config = self._get_mode()
        if (config >> pin) & 0x01 != mode:
            config ^= 1 << pin
            self.setPortMode(config)
        self.config = config
    
    def digitReadPort(self):
        return self.i2c.readfrom_mem(_ADDR, _INPUT_REG, 1)[0]     

    def digitWritePort(self, state):
        buf = bytearray(1)
        buf[0] = state
        self.i2c.writeto_mem(_ADDR, _OUTPUT_REG, buf)

    def digitRead(self, pin):
        if (self.config >> pin) & 0x01 != Ext_io.INPUT:
            return (self.i2c.readfrom_mem(_ADDR, _OUTPUT_REG, 1)[0] >> pin) & 0x01
        
        return (self.digitReadPort() >> pin) & 0x01

    def digitWrite(self, pin, value):
        if (self.config >> pin) & 0x01 != Ext_io.OUTPUT:
            self.setPinMode(pin, Ext_io.OUTPUT)

        old_value = self.i2c.readfrom_mem(_ADDR, _OUTPUT_REG, 1)[0]
        if (old_value >> pin) & 0x01 != value:
            old_value ^= 1 << pin
            self.digitWritePort(old_value)

    def deinit(self):
        pass
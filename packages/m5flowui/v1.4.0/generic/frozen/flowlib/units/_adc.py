import i2c_bus, unit
from micropython import const
import struct

ADDRESS = const(0x48)

MODE_CONTIN = const(0x00)
MODE_SINGLE = const(0x10)

RATE_240 = const(0x00)
RATE_60 = const(0x04)
RATE_30 = const(0x08)
RATE_15 = const(0x0C)

GAIN_ONE = const(0x00)
GAIN_TWO = const(0x01)
GAIN_FOUR = const(0x02)
GAIN_EIGHT = const(0x03)

OSMODE_STATE = const(0x80)

class Adc:
    def __init__(self, port):
        self.i2c = i2c_bus.get(port)
        self._available()
        self.offset = 0.25
        self.mode = MODE_CONTIN
        self.rate = RATE_15
        self.gain = GAIN_ONE
        self.mini_code = {RATE_15: 16, RATE_30:15, RATE_60:14, RATE_240:12}
        self.gain_code = {GAIN_ONE: 1, GAIN_TWO:2, GAIN_FOUR:4, GAIN_EIGHT:8}
        # self.measure_set()
    
    def _write_u8(self, value=None):
        buf=bytearray(1)
        struct.pack_into("<b", buf, 0, value)
        return self.i2c.writeto(ADDRESS, buf)

    def _read_u16(self, value=None, buf=bytearray(2)):
        self.i2c.readfrom_into(ADDRESS, buf)
        return struct.unpack(">h", buf)[0]
    
    def _available(self):
        if self.i2c.is_ready(ADDRESS) or self.i2c.is_ready(ADDRESS):
            pass
        else:
            raise unit.Unit("ADC unit maybe not connect")

    def measure_set(self, mode=None, rate=None, gain=None):
        config = 0x00
        
        if mode:
            self.mode = mode
        if rate:
            self.rate = rate
        if gain:
            self.gain = gain

        config |= self.gain | self.rate | self.mode

        self._register_char(value = config)

    @property
    def voltage(self):
        data = self._read_u16() 
        # vol = data * 2.048 / 2**(self.mini_code[self.rate] - 1) / self.gain_code[self.gain] / self.offset
        vol = data * 3.993 / 10228.206 
        # vol = data * 2.048 / 32768
        return round(vol, 3)
    
    def deinit(self):
        pass
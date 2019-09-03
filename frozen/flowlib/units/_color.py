
import utime as time
import i2c_bus, unit
from micropython import const
import ustruct

# Register and command constants:
_COMMAND_BIT       = const(0x80)
_REGISTER_ENABLE   = const(0x00)
_REGISTER_ATIME    = const(0x01)
_REGISTER_AILT     = const(0x04)
_REGISTER_AIHT     = const(0x06)
_REGISTER_ID       = const(0x12)
_REGISTER_APERS    = const(0x0c)
_REGISTER_CONTROL  = const(0x0f)
_REGISTER_SENSORID = const(0x12)
_REGISTER_STATUS   = const(0x13)
_REGISTER_CDATA    = const(0x14)
_REGISTER_RDATA    = const(0x16)
_REGISTER_GDATA    = const(0x18)
_REGISTER_BDATA    = const(0x1a)
_ENABLE_AIEN       = const(0x10)
_ENABLE_WEN        = const(0x08)
_ENABLE_AEN        = const(0x02)
_ENABLE_PON        = const(0x01)
_GAINS  = (1, 4, 16, 60)
_CYCLES = (0, 1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60)
_INT_2_4MS  = const(0xFF)   #  2.4ms - 1 cycle    - Max Count: 1024
_INT_24MS   = const(0xF6)   # 24ms  - 10 cycles  - Max Count: 10240
_INT_50MS   = const(0xEB)   #  50ms  - 20 cycles  - Max Count: 20480
_INT_101MS  = const(0xD5)   #  101ms - 42 cycles  - Max Count: 43008
_INT_154MS  = const(0xC0)   #  154ms - 64 cycles  - Max Count: 65535
_INT_700MS  = const(0x00)   #  700ms - 256 cycles - Max Count: 65535

INT_TIME_DELAY = {
    0xFF: 0.0024,  # 2.4ms - 1 cycle    - Max Count: 1024
    0xF6: 0.024,   # 24ms  - 10 cycles  - Max Count: 10240
    0xEB: 0.050,   # 50ms  - 20 cycles  - Max Count: 20480
    0xD5: 0.101,   # 101ms - 42 cycles  - Max Count: 43008
    0xC0: 0.154,   # 154ms - 64 cycles  - Max Count: 65535
    0x00: 0.700    # 700ms - 256 cycles - Max Count: 65535
}
_INTEGRATION_TIME_THRESHOLD_LOW = 2.4
_INTEGRATION_TIME_THRESHOLD_HIGH = 614.4


class Color:
    """Driver for the TCS34725 color sensor."""
    portMethod = unit.PORT_I2C 

    def __init__(self, port, address=0x29):
        self.i2c = i2c_bus.get(port)
        self.addr = address
        self._active = False
        self.integration_time = 0
        self.time = 0
        self._raw = (0, 0, 0, 0)
        self._available()
        
        self.setIntegrationTime(_INT_154MS)
        self.setGains(0x02)
        self.enable()
    
    def _available(self):
        if self.i2c.is_ready(self.addr) or self.i2c.is_ready(self.addr):
            pass
        else:
            raise unit.Unit("Color unit maybe not connect")

    @property
    def rawData(self):
        if time.ticks_ms() - self.time > 200:
            self.time = time.ticks_ms()
            c = self._read_u16(_REGISTER_CDATA)
            r = self._read_u16(_REGISTER_RDATA)
            g = self._read_u16(_REGISTER_GDATA)
            b = self._read_u16(_REGISTER_BDATA)
            self._raw = tuple([c, r, g, b])
        return self._raw

    @property
    def red(self):
        self.getRGB()
        return int(self._r)

    @property
    def green(self):
        self.getRGB()
        return int(self._g)

    @property
    def blue(self):
        self.getRGB()
        return int(self._b)

    def getRGB(self):
        s, red, green, blue = self.rawData
        if s == 0:
            return tuple([0, 0, 0])
    
        self._r = -262.5725 + 0.6841019*red - 0.0003426566*red*red + (5.791691e-8)*red*red*red
        self._r = self._r if self._r < 255 else 255
        self._r = int(self._r)
        self._g = -80.78389 + 0.465045*green - 0.0002646261*green*green + (5.152172e-8)*green*green*green
        self._g = self._g if self._g < 255 else 255
        self._g = int(self._g)
        self._b = -69.27075 + 0.4896213*blue - 0.0003063964*blue*blue + (6.570448e-8)*blue*blue*blue
        self._b = self._b if self._b < 255 else 255
        self._b = int(self._b)

        return tuple([int(self._r), int(self._g), int(self._b)]) 

    def setIntegrationTime(self, it):
        self._write_u8(_REGISTER_ATIME, it)
        self.integration_time = it

    def setGains(self, gain):
        self._write_u8(_REGISTER_CONTROL, gain)

    def enable(self):
        self._write_u8(_REGISTER_ENABLE, _ENABLE_PON)
        time.sleep(0.003)
        self._write_u8(_REGISTER_ENABLE, _ENABLE_PON | _ENABLE_AEN)
        time.sleep(0.154)

    # def color_near(self):
    #     pass

    def _valid(self):
        # Check if the status bit is set and the chip is ready.
        return bool(self._read_u8(_REGISTER_STATUS) & 0x01)

    def _register_char(self, register, value=None, buf=bytearray(1)):
        if value is None:
            self.i2c.readfrom_mem_into(self.addr, register, buf)
            return buf[0]

        ustruct.pack_into("<b", buf, 0, value)
        return self.i2c.writeto_mem(self.addr, register, buf)

    def _register_short(self, register, value=None, buf=bytearray(2)):
        if value is None:
            self.i2c.readfrom_mem_into(self.addr, register, buf)
            return buf[1]*256 + buf[0]

        ustruct.pack_into(">h", buf, 0, value)
        return self.i2c.writeto_mem(self.addr, register, buf)

    def _read_u8(self, address):
        # Read an 8-bit unsigned value from the specified 8-bit address.
        return self._register_char(_COMMAND_BIT | address)

    def _read_u16(self, address):
        # Read a 16-bit unsigned value from the specified 8-bit address.
        return self._register_short(_COMMAND_BIT | address)

    def _write_u8(self, address, val):
        # Write an 8-bit unsigned value to the specified 8-bit address.
        return self._register_char(_COMMAND_BIT | address, value=val)

    def _write_u16(self, address, val):
        # Write a 16-bit unsigned value to the specified 8-bit address.
        return self._register_short(_COMMAND_BIT | address, value=val)
    
    def deinit(self):
        pass
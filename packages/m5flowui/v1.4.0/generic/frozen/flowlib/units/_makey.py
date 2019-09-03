import unit, i2c_bus

MAKEY_I2C_ADDR = const(0x51)
class Makey:

    def __init__(self, port):
        self.i2c = i2c_bus.get(port)
        self._available()
        self.sing_map = [261, 293, 329, 349, 392, 440, 494, 294]

    def _available(self):
        if self.i2c.is_ready(MAKEY_I2C_ADDR) or self.i2c.is_ready(MAKEY_I2C_ADDR):
            pass
        else:
            raise unit.Unit("Makey unit maybe not connect")

    def _updateValue(self):
        value = 0
        data = self.i2c.readfrom(MAKEY_I2C_ADDR, 2)
        value = data[0]|(data[1] << 8)
        return value
    
    @property    
    def valueAll(self):
        return self._updateValue()

    @property
    def value(self):
        value = self._updateValue()
        for i in range(16):
            if (value >> i) & 0x01:
                return i
        return -1

    # def playPiano(self, beat):
    #     key_value = self.get_value()
    #     time.sleep_ms(1)
    #     for i in range(8):
    #         if (key_value >> i) & 0x01:
    #             speaker.sing(self.sing_map[i], beat)
    #             break
    
    def deinit(self):
        pass
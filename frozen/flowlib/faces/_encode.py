import i2c_bus
import time

class Encode:
    def __init__(self, addr = 0x5e):
        self._addr = addr
        self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        self._available()
        self.encode_value = 0
        self.press = 0
        self.time = 0
        self.dir = 0

    def _available(self):
        if self.i2c.is_ready(self._addr) or self.i2c.is_ready(self._addr):
            pass
        else:
            raise ImportError("Encode Face maybe not connect")
    
    def _update(self):
        if time.ticks_ms() - self.time > 100:
            self.time = time.ticks_ms()
            try:
                data = self.i2c.readfrom(self._addr, 2)
                if data[0] == 0:
                    pass
                elif data[0] > 127:
                    self.encode_value += data[0] - 256
                    self.dir = 1
                else:
                    self.encode_value += data[0]
                    self.dir = 0
                self.press = data[1]
            except:
                pass

    def deinit(self):
        pass

    def setLed(self, pos, color):
        pos = max(min(pos, 11), 0)
        try:
            self.i2c.writeto_mem(self._addr, pos, color.to_bytes(3, 'big'))
            time.sleep_ms(1)
        except:
            pass

    def clearValue(self):
        self.encode_value = 0

    def getValue(self):
        self._update()
        return self.encode_value

    def getDir(self):
        self._update()
        return self.dir
    
    def getPress(self):
        self._update()
        return self.press
        
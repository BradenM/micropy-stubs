import i2c_bus
import time

class Joystick:
    def __init__(self, addr = 0x5e):
        self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        self._addr = addr
        self._available()
        self.time = 0
        self.value = None

    def _available(self):
        if self.i2c.is_ready(self._addr) or self.i2c.is_ready(self._addr):
            pass
        else:
            raise ImportError("Joystick Face maybe not connect")
    
    @property    
    def X(self):
        self._update()
        return self.value[2] | (self.value[3] << 8)

    @property    
    def Y(self):
        self._update()
        return self.value[0] | (self.value[1] << 8)
    
    @property
    def InvertX(self):
        return 1024 - self.X
    
    @property    
    def InvertY(self):
        return 1024 - self.Y

    @property        
    def Press(self):
        self._update()
        return self.value[4] if self.value[4] < 2 else 0
    
    def _update(self):
        if time.ticks_ms() - self.time > 100:
            self.time = time.ticks_ms()
            try:
                self.value = self.i2c.readfrom(self._addr, 5)
            except:
                pass

    def setLed(self, num, color):
        num = max(min(num, 3), 0)
        try:
            self.i2c.writeto_mem(self._addr, num, color.to_bytes(3, 'big'))
        except:
            pass

    def deinit(self):
        pass
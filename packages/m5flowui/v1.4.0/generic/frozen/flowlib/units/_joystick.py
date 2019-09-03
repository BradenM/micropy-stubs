import i2c_bus, time
import unit

class Joystick():
    portMethod = unit.PORT_I2C 

    def __init__(self, port):
        self.i2c = i2c_bus.get(port)
        self._available()
        self.time = 0
        self.value = None

    def _available(self):
        if self.i2c.is_ready(0x52) or self.i2c.is_ready(0x52):
            pass
        else:
            raise unit.Unit("Joystick unit maybe not connect")
    
    @property    
    def X(self):
        self._update()
        return self.value[0]

    @property    
    def Y(self):
        self._update()
        return self.value[1]
    
    @property
    def InvertX(self):
        return 255 - self.X
    
    @property    
    def InvertY(self):
        return 255 - self.Y

    @property        
    def Press(self):
        self._update()
        return self.value[2] if self.value[2] < 2 else 0
    
    def _update(self):
        if time.ticks_ms() - self.time > 100:
            self.time = time.ticks_ms()
            try:
                self.value = self.i2c.readfrom(0x52, 3)
            except:
                pass

    def deinit(self):
        pass
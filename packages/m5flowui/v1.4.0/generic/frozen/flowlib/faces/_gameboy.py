import i2c_bus
from m5stack import timEx

class Gameboy:
    def __init__(self, addr = 0x08):
        self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        self.addr = addr
        self._available()
        self.press_status = 0x00
        self.release_status = 0x00
        self._timer = timEx.addTimer(100, timEx.PERIODIC, self._monitor)
        self.status_hold = 0xff
        
    def _monitor(self):
        try:
            data = self.i2c.readfrom(self.addr, 1)[0]
        except:
            return

        if data != self.status_hold:
            self.release_status |= data & (data ^ self.status_hold)
            self.press_status |= (~data) & (data ^ self.status_hold)
            self.status_hold = data

    def getStatus(self, num):
        return (self.status_hold & (0x01 << num)) == 0

    def getPressed(self, num):
        status = self.press_status & (0x01 << num)
        self.press_status &= ~(0x01 << num)
        return status > 0
    
    def getReleased(self, num):
        status = self.release_status & (0x01 << num)
        self.release_status &= ~(0x01 << num)
        return status > 0

    def _available(self):
        if self.i2c.is_ready(self.addr) or self.i2c.is_ready(self.addr):
            pass
        else:
            raise ImportError('FACE not connect')

    def _update(self):
        value = self.readfrom(self.addr, 1)[0]
        if value ^ self.last_value:
            print(bin(value ^ self.last_value))

    def deinit(self):
        self._timer.deinit()
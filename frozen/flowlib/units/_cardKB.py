import i2c_bus, unit
import machine
from m5stack import timEx

class CardKB:

    def __init__(self, port, addr=0x5f):
        self.i2c = i2c_bus.get(port)
        self.addr = addr
        self._available()
        self.key = b''
        self.string = ''
        self._timer = timEx.addTimer(150, timEx.PERIODIC, self._monitor)
    
    def _available(self):
        if self.i2c.is_ready(self.addr) or self.i2c.is_ready(self.addr):
            pass
        else:
            raise unit.Unit("CardKB unit maybe not connect")

    @property
    def keyString(self):
        return self.string[:]
    
    @property
    def keyData(self):
        data = self.key
        self.key = b''
        if data == b'':
            return 0
        else:
            return data[0]

    def isNewKeyPress(self):
        return self.key != b'' 

    def _monitor(self):
        try:
            data = self.i2c.readfrom(self.addr, 1)
            if data != b'\x00':
                self.key = data
            if 0x20 <= data[0] <= 0x7f and len(self.string) < 50:
                self.string += data.decode()
            elif data == b'\x08':
                self.string = self.string[:-1]
            elif data == b'\x1b':
                self.string = ''
        except:
            pass
        
    def deinit(self):
        self._timer.deinit()
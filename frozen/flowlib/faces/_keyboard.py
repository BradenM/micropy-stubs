import i2c_bus
import time

class Keyboard:
    def __init__(self, addr=0x08):
        self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        self.addr = addr
        self._available()
        self._str = ''
        self.key = b''
    
    def _available(self):
        if self.i2c.is_ready(self.addr) or self.i2c.is_ready(self.addr):
            pass
        else:
            raise ImportError('FACE not connect')

    def _update(self):
        try:
            data = self.i2c.readfrom(self.addr, 1)
            if data != b'\x00' and 0x20 <= data[0] <= 0x7f:
                self._str += data.decode()
        except:
            data = b''

        if data != b'\x00':
            self.key = data

    def deinit(self):
        pass
        
    def readStr(self):
        self._update()
        return self._str
    
    def clearStr(self):
        self._str = ''
    
    def deleteStrLast(self):
        self._str = self._str[:-1]

    def readKey(self):
        self._update()
        if self.key == b'':
            return 0
        data = self.key[0]
        self.key = b''
        return data
    
    def isNewKeyPress(self):
        self._update()
        return self.key != b'' 
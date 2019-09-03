import i2c_bus

class Calc:
    def __init__(self, addr=0x08):
        self.i2c = i2c_bus.get(i2c_bus.M_BUS)
        self.addr = addr
        self._available()
        self.key = b''
        self.string = ''
    
    def _available(self):
        if self.i2c.is_ready(self.addr) or self.i2c.is_ready(self.addr):
            pass
        else:
            raise ImportError('FACE Calc not connect')

    def _update(self):
        try:
            data = self.i2c.readfrom(self.addr, 1)
            if data and 0x20 <= data[0] <= 0x7f:
                self.string += data.decode()
        except:
            data = b''

        if data != b'\x00':
            self.key = data

    def readStr(self):
        self._update()
        return self.string[:]
    
    def readKey(self):
        self._update()
        data = self.key
        self.key = b''
        if data == b'':
            return 0
        else:
            return data[0]
    
    def clearStr(self):
        self.string = ''
    
    def deleteStrLast(self):
        self.string = self.string[:-1]

    def isNewKeyPress(self):
        self._update()
        return self.key != b'' 
        
    def deinit(self):
        pass
import i2c_bus
import unit

hub_addr = [0x40, 0x50, 0x60, 0x70, 0x80, 0xA0]

class Pbhub:
    def __init__(self, port, addr=0x61):
        self.addr = addr
        self.i2c = i2c_bus.easyI2C(port, self.addr)
        self._available()
    
    def _available(self):
        if self.i2c.available() or self.i2c.available():
            pass
        else:
            raise unit.Unit("Pb.hub unit maybe not connect")

    def digitalRead(self, num, pos):
        num = max(min(num, 5), 0)
        offset = 0x04 if pos else 0x05
        try:
            data = self.i2c.read_u8(hub_addr[num] | offset) > 0
        except:
            data = 0
        return data

    def digitalWrite(self, num, pos, value):
        num = max(min(num, 5), 0)
        value = 1 if value > 0 else 0
        offset = 0x00 if pos else 0x01
        try:
            self.i2c.write_u8(hub_addr[num] | offset, value)
        except:
            pass
    
    def analogRead(self, num):
        num = max(min(num, 5), 0)
        offset = 0x06
        try:
            data = self.i2c.read_u16(hub_addr[num] | offset, byteorder='little')
        except:
            data = 0
        return data

    # default: 16
    def setRgbNum(self, num, length):
        num = max(min(num, 5), 0)
        try:
            self.i2c.write_u16(hub_addr[num] | 0x08, length, 'little')
        except:
            pass        
    
    def setColorPos(self, num, pos, color_in):
        num = max(min(num, 5), 0)
        out_buf =  pos.to_bytes(2, 'little') + color_in.to_bytes(3, 'big')
        try:
            self.i2c.i2c.writeto_mem(self.addr, hub_addr[num] | 0x09, out_buf)
        except:
            pass

    def setColor(self, num, begin, count, color_in):
        num = max(min(num, 5), 0)
        out_buf = begin.to_bytes(2, 'little') + count.to_bytes(2, 'little') + color_in.to_bytes(3, 'big')
        try:
            self.i2c.i2c.writeto_mem(self.addr, hub_addr[num] | 0x0a, out_buf)
        except:
            pass

    def setBrightness(self, num, value):
        num = max(min(num, 5), 0)
        try:
            self.i2c.write_u8(hub_addr[num] | 0x0b, value)
        except:
            pass

    def deinit(self):
        pass
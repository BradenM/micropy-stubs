import i2c_bus
from micropython import const
import module

_addr = const(0x53)
_us_addr = const(0x00)
_angle_addr = const(0x10)

class Servo:
    def __init__(self, min_us=500, max_us=2500):
        self.i2c = i2c_bus.get(i2c_bus.PORTA)
        self._available()
        self.min_us = min_us
        self.max_us = max_us
    
    def _available(self):
        if self.i2c.is_ready(_addr) or self.i2c.is_ready(_addr):
            pass
        else:
            raise module.Module('module Servo maybe not connect')

    def write_us(self, pos, us):
        msc = 0
        if us == 0:
            msc = 0
        msc = int(min(self.max_us, max(self.min_us, us)))
        pos = min(11, max(0, pos))
        us_byte = bytearray(2)
        us_byte[0] = msc & 0x00ff
        us_byte[1] = msc >> 8 & 0x00ff
        self.i2c.writeto_mem(_addr, _us_addr | pos, us_byte)
        
    def write_angle(self, pos, angle):
        angle = min(180, max(0, angle))
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * angle // 180
        self.write_us(pos, us)
    
    def deinit(self):
        pass
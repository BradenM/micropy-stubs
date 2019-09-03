from machine import Pin
import unit
class Pir(): # 1 OUT
    def __init__(self, port):
        self.pin = Pin(port[1], Pin.IN)

    @property
    def state(self):
        return self.pin.value()

    def deinit(self):
        pass
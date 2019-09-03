import machine, unit

class Relay:
    def __init__(self, port):
        self.pin = machine.Pin(port[0])
        self.pin.init(mode=machine.Pin.OUT, pull=machine.Pin.PULL_DOWN,value = 0)
    
    def on(self):
        self.pin.value(1)

    def off(self):
        self.pin.value(0)

    def deinit(self):
        pass
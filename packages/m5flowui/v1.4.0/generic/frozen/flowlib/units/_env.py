import i2c_bus, unit
import time
class Env():

    def __init__(self, port):
        from dht12 import DHT12
        from bmp280 import BMP280
        self.i2c = i2c_bus.get(port)
        self._available()
        self.dht12 = DHT12(self.i2c)
        self.bmp280 = BMP280(self.i2c) 
        self.time = 0
        self.data = None

    def _available(self):
        if self.i2c.is_ready(92) or self.i2c.is_ready(92):
            pass
        else:
            raise unit.Unit("ENV unit maybe not connect")

    def deinit(self):
        self.dht12 = None
        self.bmp280 = None

    @property
    def pressure(self):
        self.data = self.values
        return round(self.data[1], 2)

    @property
    def temperature(self):
        self.data = self.values
        return round(self.data[0], 2)
    
    @property
    def humidity(self):
        self.data = self.values
        return round(self.data[2], 2)

    @property
    def values(self):
        """ readable values """
        if time.ticks_ms() - self.time > 100:
            self.time = time.ticks_ms()
            try:
                self.dht12.measure()
                h = self.dht12.humidity()
                t, p = self.bmp280.read_compensated_data()
            except:
                return self.data
            t /= 100
            p /= 25600
            return t, p, h
        else:
            return self.data
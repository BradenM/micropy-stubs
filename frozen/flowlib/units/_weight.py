from machine import Pin
import time

class Weight:

    def __init__(self, port):
        self.pinclk = Pin(port[0], Pin.OUT)
        self.pindata = Pin(port[1], Pin.IN)
        self.zero_value = 0
        self.gap_value = 250
        self.pinclk.value(0)

    def zero(self):
        self.zero_value = self._rawWeight()

    @property
    def rawData(self):
        pinclk = self.pinclk
        pindata = self.pindata
        val, times, count = 1, 0, 0
        pinclk.value(0)

        while val:
            val = pindata.value()
            if val:
                times += 1
                time.sleep_ms(10)
                if times > 20: 
                    return 0
        
        for i in range(0, 24):
            pinclk.value(1)
            count = count << 1;
            pinclk.value(0)
            
            val = pindata.value()
            if val == 1:
                count = count + 1

        pinclk.value(1)
        a = 1
        pinclk.value(0)
        count = count ^ 0x800000
        return count
    
    @property        
    def weight(self):
        countdata = self._rawWeight() - self.zero_value
        return countdata
    
    def _rawWeight(self):
        return int(self.rawData / self.gap_value)
    
    def deinit(self):
        pass
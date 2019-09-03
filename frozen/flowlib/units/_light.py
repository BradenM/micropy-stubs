import unit

class Light:

    def __init__(self, port):
        from machine import ADC, Pin
        self.adc = ADC(port[1])
        self.adc.atten(ADC.ATTN_11DB)
        self.d_pin = Pin(port[0], Pin.IN, Pin.PULL_UP)

    @property
    def analogValue(self):
        data = 0
        max = 0
        min = 4096
        for i in range(0, 10):
            newdata = 4095 - self.adc.readraw()
            data += newdata
            if newdata > max:
                max = newdata
            if newdata < min:
                min = newdata
        data -= (max + min)
        data >>= 3
        return round(1024 * data / 4095, 2)
    
    @property
    def digitalValue(self):
        return self.d_pin.value()
    
    def deinit(self):
        self.adc.deinit()
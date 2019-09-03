class Angle:
    def __init__(self, port):
        from machine import ADC
        self.adc = ADC(port[1])
        self.adc.atten(ADC.ATTN_11DB)

    def deinit(self):
        self.adc.deinit()

    def readraw(self):
        return 4095 - self.adc.readraw()

    def read(self):
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
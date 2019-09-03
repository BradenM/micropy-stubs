import machine
import i2c_bus
from m5stack import timEx

class Pm25:
    def __init__(self):
        self.uart = machine.UART(1, tx=17, rx=16)
        self.uart.init(9600, bits=8, parity=None, stop=1)
        self._timer = timEx.addTimer(200, timEx.PERIODIC, self._monitor)
        self.data_save = b''

    def _monitor(self):
        data = self.uart.read()
        if data and len(data) == 32:
            self.data_save = data
        else:
            pass

    def get_pm1_0_factory(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[4] << 8) | self.data_save[5]
    
    def get_pm2_5_factory(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[6] << 8) | self.data_save[7]
    
    def get_pm10_factory(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[8] << 8) | self.data_save[9]
    
    def get_pm1_0_air(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[10] << 8) | self.data_save[11]        
    
    def get_pm2_5_air(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[12] << 8) | self.data_save[13]
    
    def get_pm10_air(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[14] << 8) | self.data_save[15]
    
    def get_num_above_0_3(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[16] << 8) | self.data_save[17]
    
    def get_num_above_0_5(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[18] << 8) | self.data_save[19]
    
    def get_num_above_1(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[20] << 8) | self.data_save[21]
    
    def get_num_above_2_5(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[22] << 8) | self.data_save[23]
    
    def get_num_above_5(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[24] << 8) | self.data_save[25]
    
    def get_num_above_10(self):
        if len(self.data_save) != 32:
            return 0
        return (self.data_save[26] << 8) | self.data_save[27]

    def deinit(self):
        self._timer.deinit()
        try:
            self.uart.deinit()
        except:
            pass
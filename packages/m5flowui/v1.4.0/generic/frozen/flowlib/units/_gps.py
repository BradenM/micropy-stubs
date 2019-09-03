import machine, unit
import time
from m5stack import timEx

class Gps:
    def __init__(self, port):
        self.uart_data = ''
        self.gps_time = '00:00:00'
        self.gps_pos_state = ''
        self.latitude = ''
        self.longitude = ''
        self.satellite_num = ''
    
        self.uart = machine.UART(1, tx=port[0], rx=port[1])
        self.uart.init(9600, bits=0, parity=None, stop=1)
        self._timer = timEx.addTimer(100, timEx.PERIODIC, self._monitor)
    
    def _monitor(self):
        if self.uart.any() == 0:
            return 
        
        try:
            self.uart_data += self.uart.read().decode()
        except:
            pass

        data_cache = self.uart_data
        while True:
            pos = data_cache.find('\r\n')
            if pos < 0:
                break 

            gps_data = data_cache[:pos]
            data_cache = data_cache[pos + 2:]
            
            if gps_data[0] == '$':
                if gps_data[3:6] == 'GGA':
                    gps_list = gps_data.split(',')
                    self.satellite_num = gps_list[7]
                    if gps_list[1]:
                        nowTime = gps_list[1]
                        gps_hour = int(nowTime[:2]) + 8
                        if gps_hour > 23:
                            gps_hour = gps_hour - 24
                        self.gps_time = '{:0>2d}'.format(gps_hour) + ':' + nowTime[2:4] + ':' + nowTime[4:6]
                elif gps_data[3:6] == 'GLL':
                    gps_list = gps_data.split(',')
                    self.gps_pos_state = gps_list[6]
                    if self.gps_pos_state == 'A':
                        self.latitude = gps_list[1] + gps_list[2]
                        self.longitude = gps_list[3] + gps_list[4]
        
        self.uart_data =data_cache

    def deinit(self):
        self._timer.deinit()
        try:
            self.uart.deinit()
        except:
            pass
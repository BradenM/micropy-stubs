import machine
import time
from m5stack import timEx

# ACK State
ACK_SUCCESS = const(0)
ACK_FAIL = const(1)
ACK_FULL = const(4)
ACK_NOUSER = const(5)
ACK_USER_OCCUPIED = const(6) 
ACK_USER_EXIST = const(7) 
ACK_TIMEOUT = const(8)

class Finger:

    def __init__(self):

        self.uart = machine.UART(1, tx=17, rx=16)
        self.uart.init(19600, bits=0, parity=None, stop=1)
        self._timer = timEx.addTimer(100, timEx.PERIODIC, self._monitor)
        self._times = 0
        self.cb = None
        self.unknownCb = None
        self.access_add = 0
        self.user_id_add = 0
        
        self.state = ''
        time.sleep_ms(100)
        self.readUser()

    def _monitor(self):
        if self._times <= 5:
            self._times += 1

        if self._times == 5:
            self.readUser()

        if self.uart.any() < 8:
            return

        data = self.uart.read(8)
        self.uart.read()
        
        if data[0] != 0xf5 or data[-1] != 0xf5:
            return 

        chk = 0
        for i in data[1:-2]:
            chk = chk ^ i
        if chk != data[-2]:
            return 

        if data[1] == 0x01 or data[1] == 0x02:
            if data[4] == ACK_SUCCESS:
                self.addUser(self.user_id_add, self.access_add, data[1] + 0x01)
            else:
                self.state = 'Add user fail'
        else:
            if data[1] == 0x03:
                if data[4] == ACK_SUCCESS:
                    self.state = 'Add user success'
                else:
                    self.state = 'Add user fail'
                    self._times = 0
            elif data[1] == 0x04 or data[1] == 0x05:
                if data[4] == ACK_SUCCESS:
                    self.state = 'Delete user finish'
                else:
                    self.state = 'Delete user fail'
            elif data[1] == 0x0c:
                self.state = 'Got a fingerprint'
                if data[4] == 0x01 or data[4] == 0x02 or data[4] == 0x03:
                    self.state = 'Got a known finger'
                    u_id = data[2] * 256 + data[3]
                    access = data[4]
                    if self.cb:
                        self.cb(u_id, access)
                else:
                    self.state = 'Got a unknown finger'
                    if self.unknownCb:
                        self.unknownCb()
                self._times = 6

            self.readUser()
        # print(self.state)
    
    def addUser(self, user_id, access, state=0x01):
        self._write(state, user_id >> 8, user_id & 0x00ff, access)
        self.access_add = access
        self.user_id_add = user_id
        self.state = 'Wait add finger'
    
    def readUser(self):
        self._write(0x0c, 0, 0 , 0)

    def readFingerCb(self, callback):
        self.cb = callback

    def getUnknownCb(self, callback):
        self.unknownCb = callback

    def removeUser(self, user_id):
        self._write(0x04, user_id >> 8, user_id & 0x00ff, 0x00)
    
    def removeAllUser(self):
        self._write(0x05, 0, 0, 0)

    def _write(self, cmd, q1, q2, q3):
        chk = cmd ^ q1 ^ q2 ^ q3 ^ 00
        data = bytes([0xf5, cmd, q1, q2, q3, 0x00, chk, 0xf5])
        self.uart.read()
        self.uart.write(data)

    def deinit(self):
        self._timer.deinit()
        try:
            self.uart.deinit()
        except:
            pass
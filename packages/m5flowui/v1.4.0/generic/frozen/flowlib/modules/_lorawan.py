import utime as time
import machine
import module
from m5stack import timEx

class Lorawan:
    def __init__(self):
        self.uart = machine.UART(1, tx=17, rx=16)
        self.uart.init(9600, bits=8, parity=None, stop=1)
        self.callback = None
        if self._reset() == 1:
            raise module.Module('Module lorawan not connect')
        self._timer = None
        self.uartString = ''
        time.sleep(2)        

    def _monitor(self):
        data = self.uart.read()
        if data:
            self.uartString = self.uartString + data.decode()
        while True:
            pos = self.uartString.find('\r\n')
            if pos == -1:
                break
            strLine = self.uartString[:pos]
            self.uartString = self.uartString[pos + 2:]
            if ' RX ' in strLine:
                self._uart_cb(strLine)

    def _uart_cb(self, res):
        data = res[:-1]
        seek = data.find('"')
        if seek > 0:
            data = data[seek+1:]
        dataStr = ''

        for i in range(0, len(data), 2):
            dataStr += chr(int(data[i:i+2], 16))
        if self.callback:
            self.callback(dataStr)

    def _reset(self):
        self.uart.read()
        self._write(b'AT+RESET\r\n')
        self._waitTimeout(1000)
        if self.uart.read() == b'+RESET: OK\r\n':
            return 0
        else:
            return 1

    def _write(self, data):
        self.uart.write(data)

    def _setMode(self, mode):
        self.uart.read()
        self._write(b'AT+Mode=' + mode.encode() + b'\r\n')
        self._waitTimeout(200)
    
    def _waitTimeout(self, t):
        t1 = time.ticks_ms()
        while True:
            time.sleep(0.01)
            if self.uart.any():
                return 0
            if time.ticks_ms() - t1 > t:
                return 1

    def initP2PMode(self, frq, sp=12, bw=500, preTx=8, preRx=8, power=17):
        if 433<=frq<=470 or 868<=frq<=915:
            pass
        else:
            raise ValueError("Lorawan frq need in 433-470 868-915")
        self._setMode('TEST')
        data = 'AT+TEST=RFCFG,{},{},{},{},{},{}\r\n'.format(frq, sp, bw, preTx, preRx, power)
        self.uart.read()
        self._write(data.encode())
        self._waitTimeout(200)
        self.uart.read()
            
    def initRxMode(self, callback=None):
        self._write(b'AT+TEST=RXLRPKT\r\n')
        self._waitTimeout(200)
        self.uart.read()
        self._timer = timEx.addTimer(20, timEx.PERIODIC, self._monitor)
        if callback:
            self.callback=callback

    def txStr(self, sr):
        if self._timer:
            self._timer.deinit()
            self._timer = None
        self.uart.read()
        data = 'AT+TEST=TXLRSTR,"{}"\r\n'.format(sr)
        self._write(data.encode())
        self._waitTimeout(300)
        self.uart.read()
        self._waitTimeout(300)
        self.uart.read()
        self.initRxMode()

    def deinit(self):
        try:
            self._timer.deinit()
            self.uart.deinit()
        except:
            pass
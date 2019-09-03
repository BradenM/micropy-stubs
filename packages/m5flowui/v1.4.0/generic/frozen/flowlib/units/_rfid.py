import i2c_bus, unit
from micropython import const
import utime as time

OK = const(0)
NOTAGERR = const(1)
ERR = const(2)

REQIDL = const(0x26)
REQALL = const(0x52)
AUTHENT1A = const(0x60)
AUTHENT1B = const(0x61)

class Rfid:
    def __init__(self, port, addr=0x28):
        self.addr = addr
        self.i2c = i2c_bus.get(port)
        self._available()
        self.init()

        
    def _available(self):
        if self.i2c.is_ready(self.addr) or self.i2c.is_ready(self.addr):
            pass
        else:
            raise unit.Unit("RFID unit maybe not connect")

    def readBlock(self, block, keyA=None, keyB=None):
        stat, code = self._get_access(block, keyA, keyB)
        if stat != OK:
            return ERR, code
        data = self._read(block)
        self._stop_crypto1()
        return OK, data

    def readBlockStr(self, block, keyA=None, keyB=None):
        stat, code = self.readBlock(block, keyA, keyB)
        data = ''
        if stat == OK:
            for i in code:
                if i:
                    data += chr(i)
                else:
                    break
        
        return data

    def writeBlock(self, block, data, keyA=None, keyB=None):
        if ((block + 1) % 4) == 0 or block == 0:
            raise ImportError("rfid block {} can`t be write".format(block))

        stat, code = self._get_access(block, keyA, keyB)
        if stat != OK:
            return ERR, code

        if type(data) == int or type(data) == float:
            data = str(data)

        try:
            data = data.encode()
        except:
            pass

        if len(data) < 16:
            data += b'\x00' * (16 - len(data))
        
        stat = self._write(block, data)
        self._stop_crypto1()
        return stat
    
    def isCardOn(self):
        if self._request(0x26)[0] != OK:
            time.sleep(0.005)
            if self._request(0x26)[0] != OK:
                return False
        return True
    
    def readUid(self):
        if self._request(0x26)[0] != OK:
            time.sleep(0.005)
            if self._request(0x26)[0] != OK:
                return ''
        
        data_str = ''
        data = self._anticoll()[1]
        for i in data:
            data_str += str(hex(i))[2:]
        
        return data_str
        
    def init(self):
        self._reset()
        time.sleep(0.05)
        self._wreg(0x2A, 0x80)
        self._wreg(0x2B, 0xA9)
        self._wreg(0x2C, 0x03)
        self._wreg(0x2D, 0xE8)
        self._wreg(0x15, 0x40)
        self._wreg(0x11, 0x3D)
        self._antenna_on()

    def _wreg(self, reg, val):
        buf = bytearray(1)
        buf[0] = val
        self.i2c.writeto_mem(self.addr, reg, buf)

    def _rreg(self, reg):
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def _sflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) | mask)

    def _cflags(self, reg, mask):
        self._wreg(reg, self._rreg(reg) & (~mask))

    def _tocard(self, cmd, send):
        recv = []
        bits = irq_en = wait_irq = n = 0
        stat = ERR

        if cmd == 0x0E:
            irq_en = 0x12
            wait_irq = 0x10
        elif cmd == 0x0C:
            irq_en = 0x77
            wait_irq = 0x30

        self._wreg(0x02, irq_en | 0x80)
        self._cflags(0x04, 0x80)
        self._sflags(0x0A, 0x80)
        self._wreg(0x01, 0x00)

        for c in send:
            self._wreg(0x09, c)
        self._wreg(0x01, cmd)

        if cmd == 0x0C:
            self._sflags(0x0D, 0x80)

        i = 25
        while True:
            n = self._rreg(0x04)
            i -= 1
            if ~((i != 0) and ~(n & 0x01) and ~(n & wait_irq)):
                break

        self._cflags(0x0D, 0x80)

        if i:
            if (self._rreg(0x06) & 0x1B) == 0x00:
                stat = OK

                if n & irq_en & 0x01:
                    stat = NOTAGERR
                elif cmd == 0x0C:
                    n = self._rreg(0x0A)
                    lbits = self._rreg(0x0C) & 0x07
                    if lbits != 0:
                        bits = (n - 1) * 8 + lbits
                    else:
                        bits = n * 8

                    if n == 0:
                        n = 1
                    elif n > 16:
                        n = 16

                    for _ in range(n):
                        recv.append(self._rreg(0x09))
            else:
                stat = ERR
        return stat, recv, bits

    def _crc(self, data):

        self._cflags(0x05, 0x04)
        self._sflags(0x0A, 0x80)

        for c in data:
            self._wreg(0x09, c)

        self._wreg(0x01, 0x03)

        i = 0xFF
        while True:
            n = self._rreg(0x05)
            i -= 1
            if not ((i != 0) and not (n & 0x04)):
                break

        return [self._rreg(0x22), self._rreg(0x21)]

    def _reset(self):
        self._wreg(0x01, 0x0F)

    def _antenna_on(self, on=True):

        if on and ~(self._rreg(0x14) & 0x03):
            self._sflags(0x14, 0x03)
        else:
            self._cflags(0x14, 0x03)

    def _request(self, mode):

        self._wreg(0x0D, 0x07)
        (stat, recv, bits) = self._tocard(0x0C, [mode])

        if (stat != OK) | (bits != 0x10):
            stat = ERR

        return stat, bits

    def _anticoll(self):

        ser_chk = 0
        ser = [0x93, 0x20]

        self._wreg(0x0D, 0x00)
        (stat, recv, bits) = self._tocard(0x0C, ser)

        if stat == OK:
            if len(recv) == 5:
                for i in range(4):
                    ser_chk = ser_chk ^ recv[i]
                if ser_chk != recv[4]:
                    stat = ERR
            else:
                stat = ERR

        return stat, recv

    def _selectTag(self, ser):

        buf = [0x93, 0x70] + ser[:5]
        buf += self._crc(buf)
        (stat, recv, bits) = self._tocard(0x0C, buf)
        return OK if (stat == OK) and (bits == 0x18) else ERR

    def _auth(self, mode, addr, sect, ser):
        return self._tocard(0x0E, [mode, addr] + sect + ser[:4])[0]

    def _stop_crypto1(self):
        self._cflags(0x08, 0x08)

    def _read(self, addr):

        data = [0x30, addr]
        data += self._crc(data)
        (stat, recv, _) = self._tocard(0x0C, data)
        return recv if stat == OK else None

    def _write(self, addr, data):

        buf = [0xA0, addr]
        buf += self._crc(buf)
        (stat, recv, bits) = self._tocard(0x0C, buf)

        if not (stat == OK) or not (bits == 4) or not ((recv[0] & 0x0F) == 0x0A):
            stat = ERR
        else:
            buf = []
            for i in range(16):
                buf.append(data[i])
            buf += self._crc(buf)
            (stat, recv, bits) = self._tocard(0x0C, buf)
            if not (stat == OK) or not (bits == 4) or not ((recv[0] & 0x0F) == 0x0A):
                stat = ERR

        return stat
    
    def _get_access(self, block, keyA=None, keyB=None):
        if self._request(0x26)[0] != OK:
            time.sleep(0.005)
            if self._request(0x26)[0] != OK:
                return None, 1
        
        stat, uid = self._anticoll()
        if stat == ERR:
            return None, 2

        if self._selectTag(uid) == ERR:
            return None, 3

        key = [0xff] * 6
        mode = AUTHENT1A

        if keyA:
            key = keyA
            mode = AUTHENT1A
        elif keyB:
            key = keyB
            mode = AUTHENT1B

        if self._auth(mode, block, key, uid) == ERR:
            return None, 4
        
        return OK, 0

    def deinit(self):
        pass
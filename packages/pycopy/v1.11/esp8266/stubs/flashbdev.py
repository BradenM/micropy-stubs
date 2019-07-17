"""
Module: 'flashbdev' on esp8266 v1.11
"""
# MCU: (sysname='esp8266', nodename='esp8266', release='2.2.0-dev(9422289)', version='v1.11-324-g40844fd on 2019-07-17', machine='ESP module with ESP8266')
# Stubber: 1.2.0

class FlashBdev:
    ''
    NUM_BLK = 106
    RESERVED_SECS = 1
    SEC_SIZE = 4096
    START_SEC = 153
    def ioctl():
        pass

    def readblocks():
        pass

    def writeblocks():
        pass

bdev = None
esp = None
size = 4194304

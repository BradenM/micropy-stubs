"""
Module: 'flashbdev' on esp32 3.0.0
"""
# MCU: (sysname='esp32', nodename='esp32', release='3.0.0', version='v3.0.0 on 2020-01-29', machine='ESP32 module with ESP32')
# Stubber: 1.3.2

class Partition:
    ''
    BOOT = 0
    RUNNING = 1
    TYPE_APP = 0
    TYPE_DATA = 1
    def find():
        pass

    def get_next_update():
        pass

    def info():
        pass

    def ioctl():
        pass

    def readblocks():
        pass

    def set_boot():
        pass

    def writeblocks():
        pass

bdev = None

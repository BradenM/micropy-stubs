"""
Module: 'network' on WiPy 07a52e4
"""
# MCU: (sysname='WiPy', nodename='WiPy', release='1.18.2', version='07a52e4-dirty on 2019-07-26', machine='WiPy with ESP32')
# Stubber: 1.2.0

class Bluetooth:
    ''
    ADV_128SERVICE_DATA = 33
    ADV_128SRV_CMPL = 7
    ADV_128SRV_PART = 6
    ADV_16SRV_PART = 2
    ADV_32SERVICE_DATA = 32
    ADV_32SRV_CMPL = 5
    ADV_32SRV_PART = 4
    ADV_ADV_INT = 26
    ADV_APPEARANCE = 25
    ADV_DEV_CLASS = 13
    ADV_FLAG = 1
    ADV_MANUFACTURER_DATA = 255
    ADV_NAME_CMPL = 9
    ADV_NAME_SHORT = 8
    ADV_SERVICE_DATA = 22
    ADV_T16SRV_CMPL = 3
    ADV_TX_PWR = 10
    CHAR_CONFIG_INDICATE = 2
    CHAR_CONFIG_NOTIFY = 1
    CHAR_NOTIFY_EVENT = 32
    CHAR_READ_EVENT = 8
    CHAR_SUBSCRIBE_EVENT = 128
    CHAR_WRITE_EVENT = 16
    CLIENT_CONNECTED = 2
    CLIENT_DISCONNECTED = 4
    CONN_ADV = 0
    CONN_DIR_ADV = 1
    DISC_ADV = 2
    EXT_ANT = 1
    INT_ANT = 0
    NEW_ADV_EVENT = 1
    NON_CONN_ADV = 3
    PROP_AUTH = 64
    PROP_BROADCAST = 1
    PROP_EXT_PROP = 128
    PROP_INDICATE = 32
    PROP_NOTIFY = 16
    PROP_READ = 2
    PROP_WRITE = 8
    PROP_WRITE_NR = 4
    PUBLIC_ADDR = 0
    PUBLIC_RPA_ADDR = 2
    RANDOM_ADDR = 1
    RANDOM_RPA_ADDR = 3
    SCAN_RSP = 4
    def advertise():
        pass

    def callback():
        pass

    def connect():
        pass

    def deinit():
        pass

    def disconnect_client():
        pass

    def events():
        pass

    def get_adv():
        pass

    def get_advertisements():
        pass

    def init():
        pass

    def isscanning():
        pass

    def resolve_adv_data():
        pass

    def service():
        pass

    def set_advertisement():
        pass

    def start_scan():
        pass

    def stop_scan():
        pass


class Server:
    ''
    def deinit():
        pass

    def init():
        pass

    def isrunning():
        pass

    def timeout():
        pass


class WLAN:
    ''
    AP = 2
    EXT_ANT = 1
    INT_ANT = 0
    STA = 1
    STA_AP = 3
    WEP = 1
    WPA = 2
    WPA2 = 3
    WPA2_ENT = 5
    def antenna():
        pass

    def auth():
        pass

    def bssid():
        pass

    def channel():
        pass

    def connect():
        pass

    def deinit():
        pass

    def disconnect():
        pass

    def ifconfig():
        pass

    def init():
        pass

    def isconnected():
        pass

    def mac():
        pass

    def mode():
        pass

    def scan():
        pass

    def ssid():
        pass


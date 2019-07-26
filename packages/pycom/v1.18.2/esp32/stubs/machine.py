"""
Module: 'machine' on WiPy 07a52e4
"""
# MCU: (sysname='WiPy', nodename='WiPy', release='1.18.2', version='07a52e4-dirty on 2019-07-26', machine='WiPy with ESP32')
# Stubber: 1.2.0

class ADC:
    ''
    ATTN_0DB = 0
    ATTN_11DB = 3
    ATTN_2_5DB = 1
    ATTN_6DB = 2
    def channel():
        pass

    def deinit():
        pass

    def init():
        pass

    def vref():
        pass

    def vref_to_pin():
        pass

BROWN_OUT_RESET = 5

class CAN:
    ''
    FILTER_LIST = 0
    FILTER_MASK = 2
    FILTER_RANGE = 1
    FORMAT_BOTH = 3
    FORMAT_EXT = 2
    FORMAT_STD = 1
    NORMAL = 0
    RX_FIFO_NOT_EMPTY = 2
    RX_FIFO_OVERRUN = 4
    RX_FRAME = 1
    SILENT = 1
    def callback():
        pass

    def deinit():
        pass

    def events():
        pass

    def init():
        pass

    def recv():
        pass

    def send():
        pass

    def soft_filter():
        pass


class DAC:
    ''
    def deinit():
        pass

    def init():
        pass

    def tone():
        pass

    def write():
        pass

DEEPSLEEP_RESET = 3
HARD_RESET = 1

class I2C:
    ''
    MASTER = 0
    def deinit():
        pass

    def init():
        pass

    def readfrom():
        pass

    def readfrom_into():
        pass

    def readfrom_mem():
        pass

    def readfrom_mem_into():
        pass

    def scan():
        pass

    def writeto():
        pass

    def writeto_mem():
        pass

PIN_WAKE = 1

class PWM:
    ''
    def channel():
        pass

    def init():
        pass

PWRON_RESET = 0
PWRON_WAKE = 0

class Pin:
    ''
    IN = 1
    IRQ_FALLING = 2
    IRQ_HIGH_LEVEL = 5
    IRQ_LOW_LEVEL = 4
    IRQ_RISING = 1
    OPEN_DRAIN = 7
    OUT = 2
    PULL_DOWN = 2
    PULL_UP = 1
    def callback():
        pass

    exp_board = None
    def hold():
        pass

    def id():
        pass

    def init():
        pass

    def mode():
        pass

    module = None
    def pull():
        pass

    def toggle():
        pass

    def value():
        pass


class RMT:
    ''
    HIGH = 1
    LOW = 0
    def deinit():
        pass

    def init():
        pass

    def pulses_get():
        pass

    def pulses_send():
        pass


class RTC:
    ''
    INTERNAL_RC = 0
    XTAL_32KHZ = 1
    def init():
        pass

    def now():
        pass

    def ntp_sync():
        pass

    def synced():
        pass

RTC_WAKE = 2

class SD:
    ''
    def deinit():
        pass

    def init():
        pass

SOFT_RESET = 4

class SPI:
    ''
    LSB = 1
    MASTER = 0
    MSB = 0
    def deinit():
        pass

    def init():
        pass

    def read():
        pass

    def readinto():
        pass

    def write():
        pass

    def write_readinto():
        pass


class Timer:
    ''
    Alarm = None
    Chrono = None
    def sleep_us():
        pass


class UART:
    ''
    EVEN = 2
    ODD = 3
    def any():
        pass

    def deinit():
        pass

    def init():
        pass

    def read():
        pass

    def readall():
        pass

    def readinto():
        pass

    def readline():
        pass

    def sendbreak():
        pass

    def wait_tx_done():
        pass

    def write():
        pass

ULP_WAKE = 3
WAKEUP_ALL_LOW = 0
WAKEUP_ANY_HIGH = 1

class WDT:
    ''
    def feed():
        pass

    def init():
        pass

WDT_RESET = 2
def deepsleep():
    pass

def disable_irq():
    pass

def enable_irq():
    pass

def flash_encrypt():
    pass

def freq():
    pass

def idle():
    pass

def info():
    pass

def main():
    pass

mem16 = None
mem32 = None
mem8 = None
def pin_deepsleep_wakeup():
    pass

def remaining_sleep_time():
    pass

def reset():
    pass

def reset_cause():
    pass

def rng():
    pass

def secure_boot():
    pass

def sleep():
    pass

def temperature():
    pass

def unique_id():
    pass

def wake_reason():
    pass


from machine import PWM, Pin, Timer
import peripheral, unit

class Ir:
    portMethod = unit.PORT0 | unit.PORT1

    def __init__(self, port):
        self.tx = PWM(port[0], freq=38000, duty=0, timer=1)
        self.rx = Pin(port[1], Pin.IN)
        self.rx.init(Pin.IN)
        self.rx.irq(handler=self._irq_cb, trigger=Pin.IRQ_FALLING)
        self.rx_value = 0
        self.times = 0
        self.status = 0
        self.tx_en = 0
        self.duty = 0
        self.time_num = peripheral.get_timer()
        if self.time_num == None:
            raise unit.Unit('ir application time fail')
        self.timer = Timer(self.time_num)
        self.timer.init(period=50, mode=self.timer.PERIODIC, callback=self._update)

    def _irq_cb(self, pin):
        self.times = 0
    
    def _update(self, arg):
        if self.tx_en:
            self.duty = 0 if self.duty else 10
        else:
            self.duty = 0
        self.tx.duty(self.duty)
        self.times += 1

    def rxStatus(self):
        return 1 if self.times < 5 else 0

    def txOn(self):
        self.tx_en = 1
    
    def txOff(self):
        self.tx_en = 0

    def deinit(self):
        self.timer.deinit()
        if self.time_num is not None:
            peripheral.free_timer(self.time_num)
        self.rx.deinit()
from m5stack import btn
import unit

class Dual_button:
    portMethod = unit.PORT1 | unit.PORT0

    def __init__(self, port):
        self.btnRed = btn.attach(port[0])
        self.btnBlue = btn.attach(port[1])

    def deinit(self):
        btn.detach(self.btnRed)
        btn.detach(self.btnBlue)

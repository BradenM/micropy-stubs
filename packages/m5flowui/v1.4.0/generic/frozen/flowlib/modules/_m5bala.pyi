
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
def constrain(amt: Any, low: Any, high: Any) -> Any: ...
    #   0: return low
    # ? 0: return low
    #   1: return high
    # ? 1: return high
    #   2: return amt
    # ? 2: return amt
class M5bala:
    def __init__(self, i2c: Any=None) -> None: ...
    def stop(self) -> None: ...
    def move(self, speed: Any, duration: Any=5) -> None: ...
    def turn(self, speed: Any, duration: Any=5) -> None: ...
    def rotate(self, speed: Any, duration: Any=2) -> None: ...
    def set_motor(self, m0_pwm: Any, m1_pwm: Any) -> None: ...
    def read_encoder(self) -> Any: ...
        #   0: return return_value
        # ? 0: return return_value
    def balance(self) -> None: ...
    def run(self, blocking: Any=bool) -> None: ...
    def start(self, thread: Any=bool) -> None: ...

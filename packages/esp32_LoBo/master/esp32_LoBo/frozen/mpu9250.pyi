
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class MPU9250:
    def __init__(self, i2c: Any, mpu6500: Any=None, ak8963: Any=None) -> None: ...
    def acceleration(self) -> Any: ...
        #   0: return self.mpu6500.acceleration
        # ? 0: return self.mpu6500.acceleration
    def gyro(self) -> Any: ...
        #   0: return self.mpu6500.gyro
        # ? 0: return self.mpu6500.gyro
    def magnetic(self) -> Any: ...
        #   0: return self.ak8963.magnetic
        # ? 0: return self.ak8963.magnetic
    def whoami(self) -> Any: ...
        #   0: return self.mpu6500.whoami
        # ? 0: return self.mpu6500.whoami
    def __enter__(self) -> Any: ...
        #   0: return self
        # ? 0: return self
    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None: ...

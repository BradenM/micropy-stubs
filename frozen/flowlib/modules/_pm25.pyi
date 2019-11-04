
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class Pm25:
    def __init__(self) -> None: ...
    def _monitor(self) -> None: ...
    def get_pm1_0_factory(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[4]<<8|self.data_save[5]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_pm2_5_factory(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[6]<<8|self.data_save[7]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_pm10_factory(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[8]<<8|self.data_save[9]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_pm1_0_air(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[10]<<8|self.data_save[11]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_pm2_5_air(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[12]<<8|self.data_save[13]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_pm10_air(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[14]<<8|self.data_save[15]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_num_above_0_3(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[16]<<8|self.data_save[17]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_num_above_0_5(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[18]<<8|self.data_save[19]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_num_above_1(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[20]<<8|self.data_save[21]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_num_above_2_5(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[22]<<8|self.data_save[23]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_num_above_5(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[24]<<8|self.data_save[25]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def get_num_above_10(self) -> Union[Any, number]: ...
        #   0: return 0
        #   0: return number
        #   1: return self.data_save[26]<<8|self.data_save[27]
        # ? 1: return self.data_save[number]<<number|self.data_save[number]
    def deinit(self) -> None: ...

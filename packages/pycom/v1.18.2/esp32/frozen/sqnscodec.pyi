
from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class encode:
    def u32(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return array.array(struct.pack(endian+,value))
        # ? 0: return array.array(struct.pack(endian+, value))
    def s32(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return encode.u32(value,endian)
        # ? 0: return encode.u32(value, endian)
    def u16(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return array.array(struct.pack(endian+,value))
        # ? 0: return array.array(struct.pack(endian+, value))
    def u8(value: Any, endian: Any=) -> Any: ...
        #   0: return array.array(chr(value))
        # ? 0: return array.array(smallint(value))
    def string(value: Any, endian: Any=) -> Any: ...
        #   0: return array.array(value+)
        # ? 0: return array.array(value+)
class decode:
    def u32(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return struct.unpack(endian+,value)[]
        # ? 0: return struct.unpack(endian+, value)[]
    def s32(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return v-
        # ? 0: return v-
        #   1: return v
        # ? 1: return v
    def u16(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return struct.unpack(endian+,value)[]
        # ? 0: return struct.unpack(endian+, value)[]
    def u8(value: Any, endian: Any=) -> Any: ...
        #   0: return ord(value)
        # ? 0: return ord(value)
    def string(value: Any, endian: Any=) -> str: ...

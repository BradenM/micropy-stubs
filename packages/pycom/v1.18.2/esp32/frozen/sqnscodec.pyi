# make_stub_files: Fri 26 Jul 2019 at 02:36:14

from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class encode:
    def u32(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return array.array('c',struct.pack(endian+'I',value))
        # ? 0: return array.array(str, struct.pack(endian+str, value))
    def s32(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return encode.u32(value,endian)
        # ? 0: return encode.u32(value, endian)
    def u16(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return array.array('c',struct.pack(endian+'H',value))
        # ? 0: return array.array(str, struct.pack(endian+str, value))
    def u8(value: Any, endian: Any=None) -> Any: ...
        #   0: return array.array('c',chr(value))
        # ? 0: return array.array(str, smallint(value))
    def string(value: Any, endian: Any=None) -> Any: ...
        #   0: return array.array('c',value+'\x00')
        # ? 0: return array.array(str, value+str)
class decode:
    def u32(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return struct.unpack(endian+'I',value)[0]
        # ? 0: return struct.unpack(endian+str, value)[number]
    def s32(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return v-4294967296
        # ? 0: return v-number
        #   1: return v
        # ? 1: return v
    def u16(value: Any, endian: Any=BIG_ENDIAN) -> Any: ...
        #   0: return struct.unpack(endian+'H',value)[0]
        # ? 0: return struct.unpack(endian+str, value)[number]
    def u8(value: Any, endian: Any=None) -> Any: ...
        #   0: return ord(value)
        # ? 0: return ord(value)
    def string(value: Any, endian: Any=None) -> str: ...


from typing import Any, Dict, Optional, Sequence, Tuple, Union
Node = Any
class Buffer(object):
    def __init__(self, w: Any, h: Any) -> None: ...
    def pixel(self, x: Any, y: Any, color: Any) -> None: ...
    def save(self, filename: str) -> None: ...
def get_template(font: Any, size: Any, characters: Any=) -> None: ...
def pack(font: Any, w: Any, h: Any) -> Any: ...
    #   0: return font_
    # ? 0: return font_
def text(buffer: Any, string: Any, font: Any, x0: Any=, y0: Any=, color: Any=(, , ), bgcolor: Any=(, , ), colors: Any=) -> None: ...
def generate_font(font: Any, size: Any, file: Any=, characters: Any=, font_name: Any=) -> Tuple[Any, Any, Any]: ...
def generate_oled_font(font: Any, size: Any, characters: Any=) -> Any: ...
    #   0: return out
    # ? 0: return out

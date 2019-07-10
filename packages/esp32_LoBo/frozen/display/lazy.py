from machine import Pin, I2C, SPI
from display import Write, GFX, SSD1306_I2C
from display import ST7735R as ST7735R_
from display.fonts import ubuntu_mono_15, ubuntu_mono_20


########################################################################
class GFX_:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, pixel, size):
        """Constructor"""

        self.gfx = GFX(size[0], size[1], pixel)
        self.fonts = {}

    # ----------------------------------------------------------------------
    def write(self, text, pos, font=ubuntu_mono_15, *args, **kwargs):
        """"""

        if font.__name__ in self.fonts:
            self.fonts[font.__name__].text(text, pos[0], pos[1], *args, **kwargs)
        else:
            self.fonts[font.__name__] = Write(self.display, font)
            self.fonts[font.__name__].text(text, pos[0], pos[1], *args, **kwargs)

    # ----------------------------------------------------------------------
    def char(self, text, pos, font=ubuntu_mono_15, *args, **kwargs):
        """"""

        if font.__name__ in self.fonts:
            self.fonts[font.__name__].char(text, pos[0], pos[1], *args, **kwargs)
        else:
            self.fonts[font.__name__] = Write(self.display, font)
            self.fonts[font.__name__].char(text, pos[0], pos[1], *args, **kwargs)

    # ----------------------------------------------------------------------
    def __getattr__(self, attr):
        """"""

        if hasattr(self.display, attr):
            return getattr(self.display, attr)

        elif hasattr(self.gfx, attr):
            return getattr(self.gfx, attr)


########################################################################
class SSD1306(GFX_):

    # ----------------------------------------------------------------------
    def __init__(self, scl, sda, rst=16, size=(128, 64)):
        """"""

        i2c = I2C(scl=Pin(scl), sda=Pin(sda))
        Pin(rst, Pin.OUT, value=1)
        self.display = SSD1306_I2C(size[0], size[1], i2c)

        super().__init__(self.display.pixel, size)


########################################################################
class ST7735R(GFX_):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, dc, cs, rst, sclk, mosi, miso, size=(128, 128), offset=(0, 3)):
        """"""

        self.spi = SPI(2)
        self.spi.init(mosi=Pin(mosi), sck=Pin(sclk), miso=Pin(miso), baudrate=32000000)
        self.display = ST7735R_(self.spi, dc=Pin(dc), cs=Pin(cs), rst=Pin(rst), width=size[0], height=size[1], ofx=offset[0], ofy=offset[1])

        super().__init__(self.display.pixel, size)

    # ----------------------------------------------------------------------
    def close(self):
        """"""

        self.spi.deinit()






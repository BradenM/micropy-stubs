import ustruct
import utime
import gc

_NOP = const(0x00)
_SWRESET = const(0x01)
_RDDID = const(0x04)
_RDDST = const(0x09)

_SLPIN = const(0x10)
_SLPOUT = const(0x11)
_PTLON = const(0x12)
_NORON = const(0x13)

_INVOFF = const(0x20)
_INVON = const(0x21)
_DISPOFF = const(0x28)
_DISPON = const(0x29)
_CASET = const(0x2A)
_RASET = const(0x2B)
_RAMWR = const(0x2C)
_RAMRD = const(0x2E)

_PTLAR = const(0x30)
_COLMOD = const(0x3A)
_MADCTL = const(0x36)

_FRMCTR1 = const(0xB1)
_FRMCTR2 = const(0xB2)
_FRMCTR3 = const(0xB3)
_INVCTR = const(0xB4)
_DISSET5 = const(0xB6)

_PWCTR1 = const(0xC0)
_PWCTR2 = const(0xC1)
_PWCTR3 = const(0xC2)
_PWCTR4 = const(0xC3)
_PWCTR5 = const(0xC4)
_VMCTR1 = const(0xC5)

_RDID1 = const(0xDA)
_RDID2 = const(0xDB)
_RDID3 = const(0xDC)
_RDID4 = const(0xDD)

_PWCTR6 = const(0xFC)

_GMCTRP1 = const(0xE0)
_GMCTRN1 = const(0xE1)


########################################################################
class ST7735R:

    _COLUMN_SET = _CASET
    _PAGE_SET = _RASET
    _RAM_WRITE = _RAMWR
    _RAM_READ = _RAMRD

    _ENCODE_PIXEL = ">H"
    _ENCODE_POS = ">HH"
    _DECODE_PIXEL = ">BBB"

    _INIT = (
        (_SWRESET, None),
        (_SLPOUT, None),

        (_MADCTL, b"\xc8"),
        (_COLMOD, b"\x05"),  # 16bit color
        (_INVCTR, b"\x07"),

        (_FRMCTR1, b"\x01\x2c\x2d"),
        (_FRMCTR2, b"\x01\x2c\x2d"),
        (_FRMCTR3, b"\x01\x2c\x2d\x01\x2c\x2d"),

        (_PWCTR1, b"\x02\x02\x84"),
        (_PWCTR2, b"\xc5"),
        (_PWCTR3, b"\x0a\x00"),
        (_PWCTR4, b"\x8a\x2a"),
        (_PWCTR5, b"\x8a\xee"),

        (_VMCTR1, b"\x0e"),
        (_INVOFF, None),

        (_GMCTRP1, b"\x02\x1c\x07\x12\x37\x32\x29\x2d"
                   b"\x29\x25\x2B\x39\x00\x01\x03\x10"),  # Gamma
        (_GMCTRN1, b"\x03\x1d\x07\x06\x2E\x2C\x29\x2D"
                   b"\x2E\x2E\x37\x3F\x00\x00\x02\x10"),
    )

    # ----------------------------------------------------------------------
    def __init__(self, spi, dc, cs, rst=None, width=128, height=128, ofx=0, ofy=0):
        """"""
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst

        self.cs.init(self.cs.OUT, value=1)
        self.dc.init(self.dc.OUT, value=0)
        self.rst.init(self.rst.OUT, value=1)
        self.reset()

        self.width = width
        self.height = height
        self.ofx = ofx
        self.ofy = ofy

        self.width += self.ofx
        self.height += self.ofy

        for command, data in self._INIT:
            self._write(command, data)

        cols = ustruct.pack(">HH", 0, self.width - 1)
        rows = ustruct.pack(">HH", 0, self.height - 1)
        for command, data in (
            (_CASET, cols),
            (_RASET, rows),
            (_NORON, None),
            (_DISPON, None),
        ):
            self._write(command, data)

    # ----------------------------------------------------------------------
    def _block(self, x0, y0, x1, y1, data=None):
        """Read or write a block of data."""
        self._write(self._COLUMN_SET, self._encode_pos(x0, x1))
        self._write(self._PAGE_SET, self._encode_pos(y0, y1))
        if data is None:
            size = ustruct.calcsize(self._DECODE_PIXEL)
            return self._read(self._RAM_READ,
                              (x1 - x0 + 1) * (y1 - y0 + 1) * size)
        self._write(self._RAM_WRITE, data)

    # ----------------------------------------------------------------------
    def _encode_pos(self, a, b):
        """Encode a postion into bytes."""
        return ustruct.pack(self._ENCODE_POS, a, b)

    # ----------------------------------------------------------------------
    def _encode_pixel(self, color):
        """Encode a pixel color into bytes."""
        return ustruct.pack(self._ENCODE_PIXEL, self.color565(color))

    # ----------------------------------------------------------------------
    def _decode_pixel(self, data):
        """Decode bytes into a pixel color."""
        return color565(*ustruct.unpack(self._DECODE_PIXEL, data))

    # ----------------------------------------------------------------------
    def pixel(self, x, y, color=None):
        """Read or write a pixel."""
        x += self.ofx
        y += self.ofy
        if color is None:
            return self._decode_pixel(self._block(x, y, x, y))
        if not 0 <= x < self.width or not 0 <= y < self.height:
            return
        self._block(x, y, x, y, self._encode_pixel(color))

    # ----------------------------------------------------------------------
    def fill_rectangle(self, x, y, width, height, color, N=1):
        """Draw a filled rectangle."""
        x = min(self.width - 1, max(0, x)) + self.ofx
        y = min(self.height - 1, max(0, y)) + self.ofy
        w = min(self.width - x, max(1, width))  # + self.ofx
        h = min(self.height - y, max(1, height))  # + self.ofy

        for i in range(N):
            buffer = ustruct.pack(">H", self.color565(color)) * (w * (h // N))
            self.blit_buffer(buffer, x, y + (h // N) * i, w, (h // N))
            gc.collect()

    # ----------------------------------------------------------------------

    def fill(self, color=0, N=16):
        """Fill whole screen."""
        self.fill_rectangle(0, 0, self.width, self.height, color, N)

    # ----------------------------------------------------------------------
    def hline(self, x, y, width, color, N=1):
        """Draw a horizontal line."""
        self.fill_rectangle(x, y, width, 1, color, N)

    # ----------------------------------------------------------------------
    def vline(self, x, y, height, color, N=1):
        """Draw a vertical line."""
        self.fill_rectangle(x, y, 1, height, color, N)

    # ----------------------------------------------------------------------
    def blit_buffer(self, buffer, x, y, width, height):
        """Copy pixels from a buffer."""
        if (not 0 <= x < self.width or
            not 0 <= y < self.height or
            not 0 < x + width <= self.width or
                not 0 < y + height <= self.height):
                raise ValueError("out of bounds")
        self._block(x, y, x + width - 1, y + height - 1, buffer)

    # ----------------------------------------------------------------------
    def reset(self):
        self.rst(0)
        utime.sleep_ms(50)
        self.rst(1)
        utime.sleep_ms(50)

    # ----------------------------------------------------------------------
    def _write(self, command=None, data=None):
        if command is not None:
            self.dc(0)
            self.cs(0)
            self.spi.write(bytearray([command]))
            self.cs(1)
        if data is not None:
            self.dc(1)
            self.cs(0)
            self.spi.write(data)
            self.cs(1)

    # ----------------------------------------------------------------------
    def _read(self, command=None, count=0):
        self.dc(0)
        self.cs(0)
        if command is not None:
            self.spi.write(bytearray([command]))
        if count:
            data = self.spi.read(count)
        self.cs(1)
        return data

    # ----------------------------------------------------------------------
    def color565(self, r, g=None, b=None):
        """"""
        if isinstance(r, int):
            if r is None:
                r = 0
            pass
        elif isinstance(r, str):
            if r.startswith("#"):
                r, g, b = [int("0x{}".format(_), 16) for _ in (r[1:3], r[3:5], r[5:])]

        return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3










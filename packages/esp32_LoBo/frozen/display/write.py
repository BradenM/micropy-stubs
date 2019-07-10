"""
Write
=====


"""

import struct
from espresso import print_ as print
import gc

########################################################################


class Write:
    """"""
    # ----------------------------------------------------------------------

    def __init__(self, buffer, font):
        """Initialize a writer for custom font.
                
        Parameters
        ----------
        buffer : oled handler object
            This object must have the `.pixel` object.
        font : str
            The python module with the font.
        
        """

        self.buffer = buffer
        self.font = font._FONT

    # ----------------------------------------------------------------------
    def text(self, string, x0=0, y0=0, color="#ffffff", bgcolor=None, colors=None):
        """Write a string win position x0, y0.
        
        Load from bitmat font and write character by character using
        `buffer.pixel`.
        
        Parameters
        ----------
        string : str
            The message to write.
        x0 : int
            X possition.
        y0 : int
            Y possition.
    
        """

        # buffer = self.buffer
        # font = self.font

        if colors is None:
            colors = (color, color, bgcolor, bgcolor)

        x = x0
        for c in string:
            buffer = []
            if not ord(c) in self.font.keys():
                c = "?"

            row = y0
            _w, * _font = self.font[ord(c)]
            for byte in _font:
                unsalted = byte
                for col in range(x, x + _w):
                    color = colors[unsalted & 0x03]
                    # if color is not None:
                        #buffer.pixel(col, row, color)
                    buffer.append(color)
                    unsalted >>= 2
                row += 1
            print("BUFFER: ", len(buffer))
            self.draw(x, y0, col - x0, row - y0, buffer)
            x += _w

    # ----------------------------------------------------------------------

    def char(self, c, x0=0, y0=0, color="#ffffff", bgcolor=None, colors=None):
        """"""
        buffer = []

        if colors is None:
            colors = (color, color, bgcolor, bgcolor)

        if not c in self.font.keys():
            return 0

        row = y0
        _w, * _font = self.font[c]
        for byte in _font:
            unsalted = byte
            for col in range(x0, x0 + _w):
                color = colors[unsalted & 0x03]
                # if color is not None:
                #     self.buffer.pixel(col, row, color)
                buffer.append(color)
                unsalted >>= 2
            row += 1
        self.draw(x0, y0, col - x0, row - y0, buffer)
        # x += _w

    # ----------------------------------------------------------------------

    def draw(self, X, Y, col, row, buffer):
        """"""

        # for y in range(Y, row + 1):
            # for x in range(X, col + 1):
                # if buffer:
                    #self.buffer.pixel(x, y, buffer.pop(0))
                # else:
                    # return
        # print("BUFFER: ", len(buffer))

        gc.collect()
        buffer = b"".join([struct.pack(">H", self.buffer.color565(c)) for c in buffer])

        self.buffer.blit_buffer(buffer, X, Y, len(buffer) // (2 * row), row)
        gc.collect()






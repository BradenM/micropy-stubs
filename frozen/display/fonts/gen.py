"""
Generator
=========

"""

import pygame
pygame.init()

SIZES = [12, 15, 20]
FAMILIES = (

    "Ubuntu",
    "Ubuntu Condensed",
    "Ubuntu Mono",

    "Bookerly",

    "Press Start 2P",

   )


FONTS = []
for font in FAMILIES:
    for size in SIZES:

        FONTS.append((font, size))


SAMPLE_TEXT = "micropython-oled by @yeisoneng"
CHARACTERS = ''.join(chr(i) for i in range(32, 127))


COLORS = {
    (0, 0, 0, 0xff): 0,
    (0x66, 0x66, 0x66, 0xff): 1,
    (0x99, 0x99, 0x99, 0xff): 2,
    (0xff, 0xff, 0xff, 0xff): 3,
}


COLORS_ = [tuple(k) for k in COLORS]


########################################################################
class Buffer(object):
    """Fake OLED module."""

    # ----------------------------------------------------------------------
    def __init__(self, w, h):
        """Create a virtual oled display.
        
        Parameters
        ----------
        w : int
            The width of the screeen.
        h : str
            The height of the screeen.
        
        """
        self.surface = pygame.Surface((w, h))
        self.surface.fill((0, 0, 0))

    # ----------------------------------------------------------------------
    def pixel(self, x, y, color):
        """Draw a pixel in (`x`, `y`) with the respective `color`.
        
        Parameters
        ----------
        x : int
            The X coordinate of a point.
        y : str
            The Y coordinate of a point.
        color : int
        
        """
        self.surface.set_at((x, y), color)

    # ----------------------------------------------------------------------
    def save(self, filename):
        """Save the simulation on a png file.
        
        Parameters
        ----------
        filename : str
            Filename for save the simulation.
        
        """
        pygame.image.save(self.surface, filename)


# ----------------------------------------------------------------------
def get_template(font, size, characters=None):
    """Create a dictionary of surfaces with each character.
    
    Parameters
    ----------
    font : str
        Font family.
    size : int
        Font size.
    
    Returns
    -------
    dict
        Dictionary of pygame surfaces with characters as keys.
        
    """

    if characters:
        font_ = pygame.font.SysFont(font, size)
        return {char: font_.render(characters[char], False, (0, 0, 0), (255, 255, 255)) for char in characters}

    else:
        font_ = pygame.font.SysFont(font, size)
        return {char: font_.render(char, False, (0, 0, 0), (255, 255, 255)) for char in CHARACTERS}


# ----------------------------------------------------------------------
def pack(font, w, h):
    """Each row is coded in one integer.
    
    Parameters
    ----------
    w : int
        Character width.
    h : str
        Character height.
    
    Returns
    -------
    dict
        Dictionary of list of integers with characters as keys.
    
    """

    font_ = []
    for character in font:
        font_.extend((sum(COLORS[tuple(character.get_at((x, y)))] << (x * 2) for x in range(w))) for y in range(h))
    return font_


# ----------------------------------------------------------------------
def text(buffer, string, font, x0=0, y0=0, color=(255, 255, 255), bgcolor=(0, 0, 0), colors=None):
    """Simultate write on an oled display.
    
    Parameters
    ----------
    buffer : oled handler object
        The first parameter.
    string : str
        The message to write.
    font : str
        sss
    x0 : int
        X possition.
    y0 : int
        Y possition.
    color : tuple
        h
    bgcolor : tuple
        h
    colors : tuple
        h

    """

    if colors is None:
        colors = (color, color, bgcolor, bgcolor)

    x = x0
    for c in string:

        if not ord(c) in font.keys():
            c = "?"

        row = y0
        _w, * _font = font[ord(c)]
        for byte in _font:
            unsalted = byte
            for col in range(x, x + _w):
                color = colors[unsalted & 0x03]
                if color is not None:
                    buffer.pixel(col, row, color)
                unsalted >>= 2
            row += 1
        x += _w


# ----------------------------------------------------------------------
def generate_font(font, size, file=True, characters=None, font_name=None):
    """Generate a font file in form of a Python module.
    
    Parameters
    ----------
    font: str
        Font family.
    size: int
        Font size.
    file: bool
        Generate font file or not.
    characters: dict
           Custom characters set.
    
    Returns
    -------
    dict
        Dictionary of bitmaps with the gerated font.
    int
        Size of font.
    str
        Name of module generated.

    """
    template = get_template(font, size - 1, characters)

    if max([len(k) for k in characters.keys()]) > 1:
        oled_font = {char: [template[char].get_size()[0]] + pack([template[char]], *template[char].get_size()) for char in template}
    else:
        oled_font = {ord(char): [template[char].get_size()[0]] + pack([template[char]], *template[char].get_size()) for char in template}

    if not font_name:
        font_name = f"{font_name}_{size}.py"

    if not font_name.endswith("py"):
        font_name += ".py"

    if file:
        with open(font_name, 'w') as file:
            file.write("_FONT = {\n")
            for k in oled_font:
                if isinstance(k, int):
                    file.write(f"{k}: {oled_font[k]},\n")
                else:
                    file.write(f"'{k}': {oled_font[k]},\n")
            file.write("}\n")

    return oled_font, size, font_name


# ----------------------------------------------------------------------
def generate_oled_font(font, size, characters=None):
    """Generate a font file.
    
    Parameters
    ----------
    font: str
        Font family.
    size: int
        Font size.
    characters: dict
           Custom characters set.
    
    Returns
    -------
    str
        String ready to write in MicroPython file system.

    """
    oled_font, _, _ = generate_font(font, size, file=False, characters=characters)

    out = ""
    out += "_FONT = {\n"
    for k in oled_font:
        if isinstance(k, int):
            out += f"{k}: {oled_font[k]},\n"
        else:
            out += f"'{k}': {oled_font[k]},\n"
    out += "}\n"

    return out


if __name__ == "__main__":
    buffer = Buffer(1000, 500)
    l = 0
    for font_ in FONTS:
        oled_font, size, name = generate_font(*font_)

        text(buffer, f"{name}: {SAMPLE_TEXT}", oled_font, 5, l)
        l += (size + 10)

    buffer.save("sample.png")



from pybricks.parameters import Align, Button, Color, ImageFile, SoundFile
from typing import List, Tuple, Union


class sound:
    @staticmethod
    def beep(frequency: int = 500, duration: int = 100, volume: int = 30):
        """
        Play a beep/tone.

        ----------
        frequency : int - Frequency of the beep in Hertz (Default: 500).

        duration : int - Duration of the beep in milliseconds (Default: 100).

        volume : int - Volume of the beep as a percentage (Default: 30).
        """
        ...

    @staticmethod
    def beeps(number: int):
        """
        Play a number of default beeps with a brief pause in between.

        ----------
        number : int – Number of beeps.
        """
        ...

    @staticmethod
    def file(file_name: Union[str, SoundFile], volume: int = 100):
        """
        Play a sound file.

        ----------
        file_name : str – Path to the sound file, including extension. Paths can also be one of the SoundFile values.

        volume : int - Volume of the sound as a percent. (Default: 100).
        """
        ...


class display:
    @staticmethod
    def clear():
        """
        Clear everything on the display.
        """

    @staticmethod
    def image(file_name: Union[str, ImageFile], alignment: Align = Align.CENTER, coordinate: Tuple[int, int] = None, clear: bool = True):
        """
        Show an image file. You can specify its placement either using alignmentor by specifying a coordinate, 
        but not both.

        ----------
        file_name : str or ImageFile – Path to the image file. Paths may be absolute or relative from the project folder. Paths can also be one of the ImageFile values.

        alignment : Align – Where to place the image (Default: Align.CENTER).

        coordinate : Tuple[int, int] – (x, y) coordinate tuple. It is the top-left corner of the image (Default: None).

        clear : bool – Whether to clear the screen before showing the image (Default:True).
        """
        ...

    @staticmethod
    def text(text: str, coordinate: Tuple[int, int] = None):
        """
        Display text.

        ----------
        text : str – The text to display.

        coordinate : Tuple[int, int] – (x, y) coordinate tuple (Default: None). It is the top-left corner of the first character. If no coordinate is specified, it is printed on the next line.
        """
        ...


class battery:
    @staticmethod
    def current() -> int:
        """
        Get the current supplied by the battery.

        ----------
        Returns - Battery current (mA).
        """
        return 0

    @staticmethod
    def voltage() -> int:
        """
        Get the voltage of the battery.

        ----------
        Returns - Battery voltage (mV).
        """
        return 0


def buttons() -> List[Button]:
    """
    Check which buttons on the EV3 Brick are currently pressed.

    ----------
    Returns - List of pressed buttons.
    """
    return []


def light(color: Color):
    """
    Set the color of the brick light.

    ----------
    color : Color – Color of the light.  Choose Color.BLACK or None to turn the light off.
    """
    ...

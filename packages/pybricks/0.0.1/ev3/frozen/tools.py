def print(*value, sep: str = ' ', end: str = '\n', file=sys.stdout, flush: bool = False):
    """
    Print values on the terminal or a stream

    ----------
    value - Things to print (see Python print() docs).

    sep : str - The string that separates the arguments in value (Default: space).

    end : str - The string that ends the print (Default: new line).

    file - an object with a write(string) method (Default: sys.stdout).

    flush : bool - True to forcibly flush the stream.
    """
    ...


def wait(time: int):
    """
    Pause the user program for a specified amount of time.

    ----------
    time : int - How long to wait in milliseconds
    """
    ...


class StopWatch:
    """
    A stopwatch to measure time intervals. Similar to the stopwatch feature on your phone.
    """

    def time(self) -> int:
        """
        Get the current time of the stopwatch.

        ----------
        Returns - Elapsed time in milliseconds.
        """
        ...

    def pause(self):
        """
        Pause the stopwatch.
        """
        ...

    def resume(self):
        """
        Resume the stopwatch.
        """
        ...

    def reset(self):
        """
        Reset the stopwatch time to 0. The run state is unaffected:
        - If it was paused, it stays paused (but now at 0).
        - If it was running, it stays running (but starting again from 0)
        """
        ...

import cv2


class Coordinate:
    """ 
    Class Coordinate contains X and Y coordinates.
    x: x coordinate.
    y: y coordinate.
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if isinstance(value, bool):
            raise TypeError(
                "The x attribute must be of type int, "
                f"not {type(value).__name__}.")

        elif isinstance(value, int):
            if value >= 0:
                self._x = value
            else:
                raise ValueError(f"The x attribute must be positive.")

        else:
            raise TypeError(
                "The x attribute must be of type int, "
                f"not {type(value).__name__}.")

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if isinstance(value, bool):
            raise TypeError(
                "The y attribute must be of type int, "
                f"not {type(value).__name__}")

        elif isinstance(value, int):
            if value >= 0:
                self._y = value
            else:
                raise ValueError("The y attribute must be positive.")

        else:
            raise TypeError(
                "The y attribute must be of type int, "
                f"not {type(value).__name__}")


def get_coordinate(
        event, x: int, y: int, flags: list, params: list) -> Coordinate:
    """
    When you double click the left mouse button on an image, the function
    will return a Coordinate object with a click's location.

    Parameters
    ----------
    event:
        Expected event (e.g. left mouse button pressed).
    x:
        The event's x-coordinate.
    y:
        The event's y-coordinate.
    flags:
        Any relevant flags.
    params:
        Extra parameters

    Returns
    -------
    None
    """
    if event == cv2.EVENT_LBUTTONDBLCLK:
        return (Coordinate(x=x, y=y))

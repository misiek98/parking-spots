import numpy as np

from images.coordinate import Coordinate


class LinearFunction:
    """
    Stores information about the line - its slope, the a & b parameters 
    and the point the line passes through.

    Attributes:
    ----------
    angle: int
        The angle at which the line is to be sloped.

    point: Coordinate
        The point through which the straight line passes.

    a: float
        Coefficient 'a' of the straight line.

    b: float
        Coefficient 'b' of the straight line.

    Methods:
    -------
    calculate_distance
    """

    def __init__(self, angle: int, point: Coordinate):
        self.angle = angle
        self.point = point

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                "The angle parameter must be of type int, not "
                f"{type(value).__name__}.")

        if not value != 90:
            raise ValueError(
                "Because the tangent of the 90-degree angle does not "
                "exist, this value cannot be set to the angle parameter.")

        if not 180 >= value >= 0:
            raise ValueError(
                "The angle parameter must be greater than or equal to "
                "0 but less than or equal to 180.")

        self._angle = value

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, value: Coordinate):
        if not isinstance(value, Coordinate):
            raise TypeError(
                "The point parameter must be of type Coordinate, "
                f"not {type(value).__name__}.")

        self._point = value

    @property
    def a(self):
        return round(np.tan(np.deg2rad(self.angle)), 5)

    @property
    def b(self):
        return round((self.point.y - self.a*self.point.x), 5)

    def calculate_distance(self, point):
        """
        Allows to calculate the distance from a point to the line.

        Attributes:
        -----------
        point: Coordinate
            A point from which you want to calculate distance to line.
        """
        return (
            abs(-self.a*point.x + point.y + - self.b)
            / np.sqrt((-self.a)**2 + (1)**2)
        )

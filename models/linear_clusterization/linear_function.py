from collections import namedtuple

import numpy as np

from images.coordinate import Coordinate
from images.bounding_box import BoundingBox


class LinearFunction:
    """
    Stores information about the line - its slope, the a & b parameters 
    and the point the line passes through.

    Attributes:
    ----------
    angle: int
        The angle at which the line is to be sloped.

    list_of_bounding_boxes: list
        dasdasd

    seed: int
        dasdasdasdasd

    list_of_distances: list
        dasdasdasd

    point: Coordinate
        The point through which the straight line passes.

    a: float
        Coefficient 'a' of the straight line.

    b: float
        Coefficient 'b' of the straight line.


    """

    def __init__(self, angle: int, list_of_bounding_boxes: list,
                 seed=np.random.randint(0, 43)):
        self.angle = angle
        self.list_of_bounding_boxes = list_of_bounding_boxes
        self.seed = seed

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
    def list_of_bounding_boxes(self):
        return self._list_of_bounding_boxes

    @list_of_bounding_boxes.setter
    def list_of_bounding_boxes(self, value):
        if not isinstance(value, list):
            raise TypeError(
                "The list_of_bounding_boxes parameter must be of type list, "
                f"not {type(value).__name__}.")

        for bbox in value:
            if not isinstance(bbox, BoundingBox):
                raise TypeError(
                    "Elements in the list_of_bounding_boxes must be of type "
                    f"BoundingBox, not {type(bbox).__name__}.")

        self._list_of_bounding_boxes = value

    @property
    def seed(self):
        return self._seed

    @seed.setter
    def seed(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "The seed parameter must be of type int, not "
                f"{type(value).__name__}.")

        self._seed = value

    @property
    def point(self):
        np.random.seed(self.seed)
        point = np.random.choice(self.list_of_bounding_boxes)
        return Coordinate(x=point.x_center,
                          y=point.y_center)

    @property
    def a(self):
        return round(np.tan(np.deg2rad(self.angle)), 5)

    @property
    def b(self):
        return round((self.point.y - self.a*self.point.x), 5)

    def __calculate_distance(self, point):
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

    @property
    def list_of_distances(self):
        bbox_centers = [Coordinate(bbox.x_center, bbox.y_center)
                        for bbox in self.list_of_bounding_boxes]

        distance = namedtuple("distance", "point_index point_to_line_distance")
        return [
            distance(index, int(self.__calculate_distance(bbox_center)))
            for index, bbox_center in enumerate(bbox_centers)
        ]

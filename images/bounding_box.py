import numpy as np

from images.coordinate import Coordinate


class BoundingBox:
    """
    Contains an information about the object's localization.

    Attributes:
    ----------
    group_of_coords: list or np.ndarray
        List of 2 coordinates based on which other attributes are 
        determined.

    top_left_x: int
        The x axis-value of the top left corner of the bounding box.

    top_left_y: int
        The y axis-value of the top left corner of the bounding box.

    width: int
        Width of the bounding box

    height: int
        height of the bounding box
    """

    def __init__(self, group_of_coords):
        self.group_of_coords = group_of_coords

    @property
    def group_of_coords(self):
        return self._group_of_coords

    @group_of_coords.setter
    def group_of_coords(self, value):
        if isinstance(value, (list, np.ndarray)):
            if len(value) == 2:
                for coord in value:
                    if not isinstance(coord, Coordinate):
                        raise TypeError(
                            "The coord parameter must be of type Coordinate, "
                            f"not {type(value).__name__}.")
                self._group_of_coords = value
            else:
                raise ValueError(
                    "The group_of_coords must consist of 2 elements, not "
                    f"{len(value)}.")

        else:
            raise TypeError(
                "The group_of_coords parameter must be of type list, "
                f"not {type(value).__name__}.")

    @property
    def top_left_x(self):
        return min(self.group_of_coords[0].x, self.group_of_coords[1].x)

    @property
    def top_left_y(self):
        return min(self.group_of_coords[0].y, self.group_of_coords[1].y)

    @property
    def bbox_width(self):
        return (self.group_of_coords[0] - self.group_of_coords[1]).x

    @property
    def bbox_height(self):
        return (self.group_of_coords[0] - self.group_of_coords[1]).y

    @property
    def x_center(self):
        return int(self.top_left_x + self.bbox_width/2)

    @property
    def y_center(self):
        return int(self.top_left_y + self.bbox_height/2)

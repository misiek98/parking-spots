import numpy as np

from images.bounding_box import BoundingBox
from images.coordinate import Coordinate
from models.linear_clusterization.linear_function import LinearFunction


class LinearClusterization:
    """
    ABCDEF

    Attributes:
    ----------
    list_of_bounding_boxes: list
        abcdef

    angle_step: int
        abcdef
    """

    def __init__(self, list_of_bounding_boxes: list, angle_step: int,
                 seed: int):
        self.list_of_bounding_boxes = list_of_bounding_boxes
        self.angle_step = angle_step

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
    def angle_step(self):
        return self._angle_step

    @angle_step.setter
    def angle_step(self, value):
        if not isinstance(value, int):
            raise TypeError(
                "The angle_step parameter must be of type int, not "
                f"{type(value).__name__}.")

        if not 180 >= value > 0:
            raise ValueError(
                "The angle_step parameter must be greater than 0 but less than"
                " or equal 180.")

        self._angle_step = value

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
    def __list_of_distances_different_angles(self):
        angles = [angle
                  for angle in range(0, 181, self.angle_step)
                  if angle != 90]

        return [
            LinearFunction(angle=angle,
                           list_of_bounding_boxes=self.list_of_bounding_boxes,
                           seed=self.seed)
            for angle in angles
        ]

    def __sort_distances(self, line):
        return sorted(line.list_of_distances,
                      key=lambda x: x.point_to_line_distance)

    def __only_distances(self, line):
        return [distance.point_to_line_distance
                for distance in line.list_of_distances]

    # def __temporary_areas(self):
    # def __determine_areas(self):
    # def __areas_length(self):
    # def __max_area_length(self):
    # def __get_areas_max_length(self):
    # def __choose_best_area(self):
